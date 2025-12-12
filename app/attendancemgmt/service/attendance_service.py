# dojo-attendance-mgmt-lambda/app/attendancemgmt/service/attendance_service.py
from typing import List, Dict
from datetime import date, datetime
from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.service.base_service import BaseService
from dojocommons.exception.business_exception import BusinessException
from attendancemgmt.model.attendance import Attendance
from attendancemgmt.repository.attendance_repository import AttendanceRepository


class AttendanceService(BaseService[Attendance]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, AttendanceRepository)
    
    def create(self, entity: Attendance) -> Attendance:
        """Cria um novo registro de presença com validações"""
        # Valida se já não existe registro para esse atleta/aula/data
        existing = self._repository.find_by_athlete_class_date(
            entity.athlete_id,
            entity.class_id,
            entity.attendance_date
        )
        
        if existing:
            raise BusinessException(
                f"Attendance already recorded for athlete {entity.athlete_id} "
                f"in class {entity.class_id} on {entity.attendance_date}",
                status_code=409
            )
        
        # Define recorded_at se não foi informado
        if not entity.recorded_at:
            entity.recorded_at = datetime.now()
        
        return super().create(entity)
    
    def mark_attendance(
        self, 
        athlete_id: int, 
        class_id: int, 
        attendance_date: date, 
        status: str,
        recorded_by: str = "",
        notes: str = ""
    ) -> Attendance:
        """Método facilitador para registrar presença/falta"""
        attendance = Attendance(
            athlete_id=athlete_id,
            class_id=class_id,
            attendance_date=attendance_date,
            status=status,
            recorded_by=recorded_by,
            notes=notes,
            recorded_at=datetime.now()
        )
        return self.create(attendance)
    
    def get_athlete_attendance_rate(
        self, 
        athlete_id: int, 
        class_id: int, 
        start_date: date, 
        end_date: date
    ) -> Dict:
        """Calcula taxa de frequência do atleta em uma aula no período"""
        attendances = self._repository.find_by_athlete_and_period(
            athlete_id, class_id, start_date, end_date
        )
        
        total = len(attendances)
        if total == 0:
            return {
                "athlete_id": athlete_id,
                "class_id": class_id,
                "period": {"start": start_date, "end": end_date},
                "total_classes": 0,
                "present": 0,
                "absent": 0,
                "justified": 0,
                "late": 0,
                "attendance_rate": 0.0
            }
        
        present = sum(1 for a in attendances if a.status == 'present')
        absent = sum(1 for a in attendances if a.status == 'absent')
        justified = sum(1 for a in attendances if a.status == 'justified')
        late = sum(1 for a in attendances if a.status == 'late')
        
        # Taxa de frequência (presentes / total)
        attendance_rate = round((present / total) * 100, 2)
        
        return {
            "athlete_id": athlete_id,
            "class_id": class_id,
            "period": {"start": str(start_date), "end": str(end_date)},
            "total_classes": total,
            "present": present,
            "absent": absent,
            "justified": justified,
            "late": late,
            "attendance_rate": attendance_rate
        }
    
    def get_class_attendance_by_date(
        self, 
        class_id: int, 
        attendance_date: date
    ) -> List[Attendance]:
        """Lista todos os registros de uma aula em uma data específica"""
        return self._repository.find_by_class_and_date(class_id, attendance_date)
    
    def get_athlete_absences(self, athlete_id: int, class_id: int) -> List[Attendance]:
        """Retorna todas as faltas de um atleta em uma aula"""
        return self._repository.find_absences_by_athlete_and_class(athlete_id, class_id)
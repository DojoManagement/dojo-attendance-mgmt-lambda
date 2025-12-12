from typing import List
from datetime import date
from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.repository.base_repository import BaseRepository
from attendancemgmt.model.attendance import Attendance


class AttendanceRepository(BaseRepository[Attendance]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, Attendance, "attendance")
    
    def find_by_athlete_id(self, athlete_id: int) -> List[Attendance]:
        """Busca todos os registros de presença de um atleta"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE athlete_id = ?
            ORDER BY attendance_date DESC
        """
        rows = self._db.execute_query(query, (athlete_id,)).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
    
    def find_by_class_id(self, class_id: int) -> List[Attendance]:
        """Busca todos os registros de presença de uma aula"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE class_id = ?
            ORDER BY attendance_date DESC
        """
        rows = self._db.execute_query(query, (class_id,)).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
    
    def find_by_athlete_and_period(
        self, 
        athlete_id: int, 
        class_id: int, 
        start_date: date, 
        end_date: date
    ) -> List[Attendance]:
        """Busca registros de presença de um atleta em um período"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE athlete_id = ?
            AND class_id = ?
            AND attendance_date BETWEEN ? AND ?
            ORDER BY attendance_date DESC
        """
        rows = self._db.execute_query(
            query, 
            (athlete_id, class_id, start_date, end_date)
        ).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
    
    def find_by_class_and_date(self, class_id: int, attendance_date: date) -> List[Attendance]:
        """Busca todos os registros de uma aula em uma data específica"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE class_id = ?
            AND attendance_date = ?
            ORDER BY athlete_id
        """
        rows = self._db.execute_query(query, (class_id, attendance_date)).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
    
    def find_by_athlete_class_date(
        self, 
        athlete_id: int, 
        class_id: int, 
        attendance_date: date
    ) -> List[Attendance]:
        """Verifica se já existe registro de presença para atleta/aula/data específicos"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE athlete_id = ?
            AND class_id = ?
            AND attendance_date = ?
        """
        rows = self._db.execute_query(
            query, 
            (athlete_id, class_id, attendance_date)
        ).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
    
    def find_absences_by_athlete_and_class(
        self, 
        athlete_id: int, 
        class_id: int
    ) -> List[Attendance]:
        """Busca todas as faltas de um atleta em uma aula específica"""
        query = f"""
            SELECT * FROM {self._table_name}
            WHERE athlete_id = ?
            AND class_id = ?
            AND status IN ('absent', 'justified')
            ORDER BY attendance_date DESC
        """
        rows = self._db.execute_query(query, (athlete_id, class_id)).fetchall()
        return [
            Attendance.model_validate(
                dict(zip(Attendance.__annotations__.keys(), row))
            )
            for row in rows
        ]
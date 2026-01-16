from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AttendanceBase(BaseModel):
    """Modelo de Presença/Frequência - registro de presença ou falta em aulas"""
    athlete_id: int = Field(..., description="ID do atleta")
    class_id: int = Field(..., description="ID da aula")
    attendance_date: date = Field(..., description="Data da aula")
    status: str = Field(..., description="Status: 'present', 'absent', 'justified', 'late'")
    notes: Optional[str] = Field(default="", description="Observações (motivo da falta, etc)")
    recorded_by: Optional[str] = Field(default="", description="Quem registrou (professor/sistema)")
    recorded_at: Optional[datetime] = Field(default=None, description="Data/hora do registro")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Valida se o status é válido"""
        valid_statuses = ['present', 'absent', 'justified', 'late']
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v
    
class AttendanceCreate(AttendanceBase):
    """✅ Modelo para criação (sem ID)"""
    pass


class Attendance(AttendanceBase):
    """Modelo completo com ID"""
    id: str = Field(default="", description="UUID único (gerado automaticamente)")

    class Config:
        from_attributes = True
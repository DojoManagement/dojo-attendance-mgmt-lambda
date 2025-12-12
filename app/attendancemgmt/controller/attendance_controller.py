from dojocommons.controller.base_controller import BaseController
from dojocommons.model.app_configuration import AppConfiguration
from attendancemgmt.model.attendance import Attendance
from attendancemgmt.model.resource import Resource
from attendancemgmt.service.attendance_service import AttendanceService


class AttendanceController(BaseController[Attendance]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, AttendanceService, Resource.ATTENDANCES.value, Attendance)
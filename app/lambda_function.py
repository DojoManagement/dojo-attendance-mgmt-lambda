import json
from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.model.base_event import BaseEvent
from dojocommons.model.response import Response
from dojocommons.exception.business_exception import BusinessException
from attendancemgmt.controller.attendance_controller import AttendanceController


def lambda_handler(event: dict, context) -> dict:
    """Lambda handler para Attendance Management"""
    print(f"[DEBUG][Lambda] Evento recebido: {json.dumps(event)}")
    
    try:
        cfg = AppConfiguration()
        base_event = BaseEvent(**event)
        controller = AttendanceController(cfg)
        response = controller.dispatch(base_event)
        return response.model_dump(by_alias=True, exclude_none=True)
 
    except BusinessException as e:
        print(f"Business exception: {e.message}")
        return Response(
            status_code=e.status_code,
            body={"error": e.message}
        ).model_dump(by_alias=True, exclude_none=True)
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return Response(
            status_code=500,
            body={"error": f"Internal server error: {str(e)}"}
        ).model_dump(by_alias=True, exclude_none=True)
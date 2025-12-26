from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.model.base_event import BaseEvent
from attendancemgmt.controller.attendance_controller import AttendanceController
from attendancemgmt.utils.cors_helper import CORSHelper
import json
import traceback

def lambda_handler(event, _):
    print("[DEBUG][Lambda] Evento recebido:", json.dumps(event))
    try:
        if event.get('httpMethod') == 'OPTIONS':
            print("[DEBUG][Lambda] Requisição OPTIONS detectada (CORS preflight)")
            response = CORSHelper.create_preflight_response()
            return response.model_dump(by_alias=True, exclude_none=True)
        
        event_obj = BaseEvent.model_validate(event)
        cfg = AppConfiguration()  # type: ignore
        controller = AttendanceController(cfg)
        response = controller.dispatch(event_obj)
        response = CORSHelper.add_cors_headers(response)
        print(f"[DEBUG][Lambda] Resposta: {response.status_code}")
    
    except ValueError as err:
        print(f"[ERROR][Lambda] Erro de validação: {str(err)}")
        response = CORSHelper.create_error_response(
            status_code=400,
            error_message=str(err),
            error_type="ValidationError"
        )

    except Exception as err:
        print(f"[ERROR][Lambda] Erro inesperado: {str(err)}")
        print(f"[ERROR][Lambda] Traceback: {traceback.format_exc()}")
        response = CORSHelper.create_error_response(
            status_code=500,
            error_message="Internal server error",
            error_type="InternalError"
        )

    response_dict = response.model_dump(by_alias=True, exclude_none=True)
    print(f"[DEBUG][Lambda] Response dict: {json.dumps(response_dict)}")

    return response_dict

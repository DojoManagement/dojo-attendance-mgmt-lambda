from dojocommons.model.base_resource import BaseResource

class Resource(BaseResource):
    """Definição de rotas para Attendance"""
    ATTENDANCES = "/attendances"
    ATTENDANCES_ID = "/attendances/{id}"
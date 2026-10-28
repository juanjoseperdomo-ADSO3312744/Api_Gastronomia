from typing import Optional, Dict, Any
from app.repositories.j_base_repository import JBaseRepository


class JClientesRepository(JBaseRepository):
    def __init__(self):
        super().__init__("clientes")

    def j_buscar_por_identificacion(self, identificacion: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"identificacion": identificacion.strip()})


j_clientes_repo = JClientesRepository()

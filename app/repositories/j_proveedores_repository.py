from typing import Optional, Dict, Any
from app.repositories.j_base_repository import JBaseRepository


class JProveedoresRepository(JBaseRepository):
    def __init__(self):
        super().__init__("proveedores")

    def j_buscar_por_nit(self, nit: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"nit": nit.strip()})


j_proveedores_repo = JProveedoresRepository()

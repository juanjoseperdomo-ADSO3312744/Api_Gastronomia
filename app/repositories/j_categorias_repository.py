from typing import Optional, Dict, Any
from app.repositories.j_base_repository import JBaseRepository


class JCategoriasRepository(JBaseRepository):
    def __init__(self):
        super().__init__("categorias")

    def j_buscar_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"nombre": {"$regex": f"^{nombre.strip()}$", "$options": "i"}})


j_categorias_repo = JCategoriasRepository()

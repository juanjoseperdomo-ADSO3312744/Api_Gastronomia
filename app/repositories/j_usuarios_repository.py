from typing import Optional, Dict, Any
from app.repositories.j_base_repository import JBaseRepository


class JUsuariosRepository(JBaseRepository):
    def __init__(self):
        super().__init__("usuarios")

    def j_buscar_por_correo(self, correo: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"correo": correo.strip().lower()})

    def j_buscar_por_identificacion(self, identificacion: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"identificacion": identificacion.strip()})


j_usuarios_repo = JUsuariosRepository()

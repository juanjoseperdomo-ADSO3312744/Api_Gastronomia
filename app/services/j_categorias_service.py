from typing import List, Dict, Any
from fastapi import HTTPException, status
from app.repositories.j_categorias_repository import j_categorias_repo
from app.repositories.j_productos_repository import j_productos_repo
from app.schemas.j_categorias_schema import JCategoriaCreate, JCategoriaUpdate


class JCategoriasService:
    def j_crear_categoria(self, datos: JCategoriaCreate) -> Dict[str, Any]:
        if j_categorias_repo.j_buscar_por_nombre(datos.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría registrada con el nombre '{datos.nombre}'."
            )
        doc = datos.model_dump()
        doc["nombre"] = datos.nombre.strip()
        return j_categorias_repo.j_crear(doc)

    def j_obtener_por_id(self, id_categoria: str) -> Dict[str, Any]:
        cat = j_categorias_repo.j_obtener_por_id(id_categoria)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID '{id_categoria}' no encontrada."
            )
        return cat

    def j_listar_categorias(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        return j_categorias_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("nombre", 1)])

    def j_actualizar_categoria(self, id_categoria: str, datos: JCategoriaUpdate) -> Dict[str, Any]:
        cat_existente = j_categorias_repo.j_obtener_por_id(id_categoria)
        if not cat_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID '{id_categoria}' no encontrada."
            )

        datos_act = datos.model_dump(exclude_unset=True)
        if "nombre" in datos_act and datos_act["nombre"]:
            nuevo_nombre = datos_act["nombre"].strip()
            encontrado = j_categorias_repo.j_buscar_por_nombre(nuevo_nombre)
            if encontrado and encontrado["id"] != id_categoria:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe otra categoría con el nombre '{nuevo_nombre}'."
                )
            datos_act["nombre"] = nuevo_nombre

        return j_categorias_repo.j_actualizar(id_categoria, datos_act)

    def j_eliminar_categoria(self, id_categoria: str) -> Dict[str, Any]:
        cat = j_categorias_repo.j_obtener_por_id(id_categoria)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID '{id_categoria}' no encontrada."
            )

        # Verificar si tiene productos asociados (RN04)
        productos = j_productos_repo.j_buscar_por_categoria(id_categoria)
        if productos:
            j_categorias_repo.j_cambiar_estado(id_categoria, "INACTIVO")
            return {
                "mensaje": f"La categoría tiene {len(productos)} productos asociados. Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_categoria
            }
        else:
            j_categorias_repo.j_eliminar_fisico(id_categoria)
            return {
                "mensaje": "Categoría eliminada físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_categoria
            }


j_categorias_service = JCategoriasService()

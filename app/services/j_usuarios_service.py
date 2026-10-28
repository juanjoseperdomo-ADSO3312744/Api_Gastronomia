from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.core.j_security import j_hashear_password
from app.repositories.j_usuarios_repository import j_usuarios_repo
from app.repositories.j_compras_repository import j_compras_repo
from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.schemas.j_usuarios_schema import JUsuarioCreate, JUsuarioUpdate


class JUsuariosService:
    def j_crear_usuario(self, datos: JUsuarioCreate) -> Dict[str, Any]:
        # Validar duplicados de correo
        if j_usuarios_repo.j_buscar_por_correo(datos.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario registrado con el correo '{datos.correo}'."
            )

        # Validar duplicados de identificación
        if j_usuarios_repo.j_buscar_por_identificacion(datos.identificacion):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con la identificación '{datos.identificacion}'."
            )

        doc = datos.model_dump()
        # RN06: Cifrado con bcrypt y nunca devolver contraseña
        doc["password"] = j_hashear_password(datos.password)
        doc["correo"] = datos.correo.strip().lower()
        usuario_creado = j_usuarios_repo.j_crear(doc)
        usuario_creado.pop("password", None)
        return usuario_creado

    def j_obtener_por_id(self, id_usuario: str) -> Dict[str, Any]:
        usuario = j_usuarios_repo.j_obtener_por_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID '{id_usuario}' no encontrado."
            )
        usuario.pop("password", None)
        return usuario

    def j_listar_usuarios(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        usuarios = j_usuarios_repo.j_obtener_todos(salto=salto, limite=limite)
        for u in usuarios:
            u.pop("password", None)
        return usuarios

    def j_actualizar_usuario(self, id_usuario: str, datos: JUsuarioUpdate) -> Dict[str, Any]:
        usuario_existente = j_usuarios_repo.j_obtener_por_id(id_usuario)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID '{id_usuario}' no encontrado."
            )

        datos_actualizar = datos.model_dump(exclude_unset=True)

        # Si actualiza correo, verificar duplicado
        if "correo" in datos_actualizar and datos_actualizar["correo"]:
            nuevo_correo = datos_actualizar["correo"].strip().lower()
            encontrado = j_usuarios_repo.j_buscar_por_correo(nuevo_correo)
            if encontrado and encontrado["id"] != id_usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El correo '{nuevo_correo}' ya está en uso por otro usuario."
                )
            datos_actualizar["correo"] = nuevo_correo

        # Si actualiza identificación, verificar duplicado
        if "identificacion" in datos_actualizar and datos_actualizar["identificacion"]:
            nueva_id = datos_actualizar["identificacion"].strip()
            encontrado = j_usuarios_repo.j_buscar_por_identificacion(nueva_id)
            if encontrado and encontrado["id"] != id_usuario:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"La identificación '{nueva_id}' ya está en uso por otro usuario."
                )

        # Si actualiza contraseña, aplicar hash bcrypt (RN06)
        if "password" in datos_actualizar and datos_actualizar["password"]:
            datos_actualizar["password"] = j_hashear_password(datos_actualizar["password"])

        usuario_act = j_usuarios_repo.j_actualizar(id_usuario, datos_actualizar)
        usuario_act.pop("password", None)
        return usuario_act

    def j_eliminar_usuario(self, id_usuario: str) -> Dict[str, Any]:
        """
        Regla RN04: Si tiene movimientos (compras o pedidos registrados),
        se realiza borrado lógico cambiando a INACTIVO.
        """
        usuario = j_usuarios_repo.j_obtener_por_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID '{id_usuario}' no encontrado."
            )

        tiene_compras = j_compras_repo.j_tiene_compras_de_usuario(id_usuario)
        tiene_pedidos = j_pedidos_repo.j_tiene_pedidos_de_usuario(id_usuario)

        if tiene_compras or tiene_pedidos:
            j_usuarios_repo.j_cambiar_estado(id_usuario, "INACTIVO")
            return {
                "mensaje": "El usuario posee movimientos asociados (compras o pedidos). Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_usuario
            }
        else:
            j_usuarios_repo.j_eliminar_fisico(id_usuario)
            return {
                "mensaje": "Usuario eliminado físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_usuario
            }


j_usuarios_service = JUsuariosService()

from enum import Enum


class JRolUsuario(str, Enum):
    ADMIN = "ADMIN"
    CAJERO = "CAJERO"
    COCINERO = "COCINERO"


class JEstadoGenerico(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class JEstadoProducto(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    INACTIVO = "INACTIVO"


class JUnidadMedida(str, Enum):
    G = "g"
    KG = "kg"
    ML = "ml"
    L = "l"
    LB = "lb"
    UNIDAD = "unidad"


class JTipoCliente(str, Enum):
    APRENDIZ = "APRENDIZ"
    INSTRUCTOR = "INSTRUCTOR"
    FUNCIONARIO = "FUNCIONARIO"
    EXTERNO = "EXTERNO"


class JTipoPedido(str, Enum):
    MESA = "MESA"
    PARA_LLEVAR = "PARA_LLEVAR"
    EVENTO = "EVENTO"


class JEstadoPedido(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    ENTREGADO = "ENTREGADO"
    ANULADO = "ANULADO"

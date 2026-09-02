from typing import List, Optional


from pydantic import BaseModel


# ============================================================
# GENERICOS
# ============================================================

class SeriePeriodo(BaseModel):
    periodo: str
    valor: float


class ItemCantidad(BaseModel):
    nombre: str
    cantidad: int
    porcentaje: float


# ============================================================
# CURSOS
# ============================================================

class CursosKPI(BaseModel):
    cursos_activos: int
    estudiantes_inscritos: int
    inscripciones_completadas: int
    ingresos_registrados: float


class CursoIngresos(BaseModel):
    id_curso: int
    nombre: str
    ingresos: float


class CursoProgreso(BaseModel):
    rango: str
    cantidad: int
    porcentaje: float


class CursosDashboard(BaseModel):

    kpis: CursosKPI

    inscripciones_por_mes: List[SeriePeriodo]

    por_curso: List[ItemCantidad]

    ingresos_por_curso: List[CursoIngresos]

    gratuito_vs_premium: List[ItemCantidad]

    por_nivel: List[ItemCantidad]

    progreso_estudiantes: List[CursoProgreso]


# ============================================================
# SERVICIOS
# ============================================================

class ServiciosKPI(BaseModel):
    servicios_activos: int
    solicitudes_totales: int
    clientes_registrados: int
    servicio_mas_solicitado: Optional[str] = None


class ServicioIngresosPotenciales(BaseModel):
    id_servicio: int
    nombre: str
    solicitudes: int
    precio_base: float
    valor_referencial: float


class ServiciosDashboard(BaseModel):

    kpis: ServiciosKPI

    solicitudes_por_mes: List[SeriePeriodo]

    por_servicio: List[ItemCantidad]

    por_estado: List[ItemCantidad]

    tipo_cliente: List[ItemCantidad]

    demanda_servicios: List[ServicioIngresosPotenciales]
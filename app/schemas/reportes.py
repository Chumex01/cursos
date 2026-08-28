from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, model_validator


# ============================================================
# FILTROS GENERALES
# ============================================================

class FiltroFecha(BaseModel):
    desde: Optional[datetime] = None
    hasta: Optional[datetime] = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.desde and self.hasta and self.desde > self.hasta:
            raise ValueError(
                "La fecha 'desde' no puede ser mayor que 'hasta'."
            )

        return self


# ============================================================
# ELEMENTOS GENERICOS
# ============================================================

class SerieFecha(BaseModel):
    fecha: date
    valor: float


class RankingItem(BaseModel):
    nombre: str
    valor: float


class Paginacion(BaseModel):
    pagina: int
    limite: int
    total: int
    paginas: int


# ============================================================
# ============================================================
# AUDITORIA
# ============================================================
# ============================================================

class AuditoriaKPI(BaseModel):
    total_acciones: int
    usuarios_activos: int
    tablas_afectadas: int
    acciones_periodo: int


class AuditoriaDashboard(BaseModel):
    filtros: FiltroFecha

    kpis: AuditoriaKPI

    por_dia: List[SerieFecha]
    por_accion: List[RankingItem]
    por_tabla: List[RankingItem]
    por_usuario: List[RankingItem]


class AuditoriaDetalle(BaseModel):
    id_auditoria: int
    usuario: str
    accion: str
    tabla: str

    registro_id: Optional[int] = None
    ip: Optional[str] = None

    fecha_hora: datetime

    datos_antiguos: Optional[Dict[str, Any]] = None
    datos_nuevos: Optional[Dict[str, Any]] = None


class AuditoriaDetalleResponse(BaseModel):
    datos: List[AuditoriaDetalle]
    paginacion: Paginacion


class AuditoriaFiltros(BaseModel):
    acciones: List[str]
    tablas: List[str]

    usuarios: List[Dict[str, Any]]


# ============================================================
# ============================================================
# FUENTES DE TRAFICO
# ============================================================
# ============================================================

class TraficoKPI(BaseModel):
    total_sesiones: int
    fuentes_distintas: int
    campanias_distintas: int

    mejor_fuente: Optional[str] = None


class FuenteTraficoItem(BaseModel):
    nombre: str
    sesiones: int
    porcentaje: float


class FuentesTraficoDashboard(BaseModel):
    filtros: FiltroFecha

    kpis: TraficoKPI

    evolucion: List[SerieFecha]

    por_fuente: List[FuenteTraficoItem]
    por_medio: List[FuenteTraficoItem]
    por_campania: List[FuenteTraficoItem]


class FuenteTraficoDetalle(BaseModel):
    id_sesion: int
    visitante_id: int

    fuente: Optional[str] = None
    medio: Optional[str] = None
    campania: Optional[str] = None
    contenido: Optional[str] = None
    termino: Optional[str] = None

    fecha_inicio: datetime


class FuenteTraficoDetalleResponse(BaseModel):
    datos: List[FuenteTraficoDetalle]
    paginacion: Paginacion


class FuentesTraficoFiltros(BaseModel):
    fuentes: List[str]
    medios: List[str]
    campanias: List[str]
    contenidos: List[str]
    terminos: List[str]


# ============================================================
# ============================================================
# EVENTOS
# ============================================================
# ============================================================

class EventosKPI(BaseModel):
    total_eventos: int
    sesiones_con_eventos: int

    tipo_principal: Optional[str] = None
    pagina_principal: Optional[str] = None


class EventoItem(BaseModel):
    nombre: str
    cantidad: int
    porcentaje: float


class EventosDashboard(BaseModel):
    filtros: FiltroFecha

    kpis: EventosKPI

    evolucion: List[SerieFecha]

    por_tipo: List[EventoItem]
    por_pagina: List[EventoItem]
    por_curso: List[EventoItem]
    por_servicio: List[EventoItem]
    por_proyecto: List[EventoItem]


class EventoDetalle(BaseModel):
    id_evento: int
    id_sesion: int

    tipo_evento: str
    pagina: Optional[str] = None

    curso: Optional[str] = None
    servicio: Optional[str] = None
    proyecto: Optional[str] = None

    fecha_hora: datetime

    datos: Optional[Dict[str, Any]] = None


class EventoDetalleResponse(BaseModel):
    datos: List[EventoDetalle]
    paginacion: Paginacion


class EventosFiltros(BaseModel):
    tipos_evento: List[str]
    paginas: List[str]

    cursos: List[Dict[str, Any]]
    servicios: List[Dict[str, Any]]
    proyectos: List[Dict[str, Any]]


# ============================================================
# ============================================================
# VISITANTES
# ============================================================
# ============================================================

class VisitantesKPI(BaseModel):
    total_visitantes: int

    nuevos_visitantes: int
    visitantes_recurrentes: int

    sesiones_totales: int

    pais_principal: Optional[str] = None


class VisitanteItem(BaseModel):
    nombre: str
    visitantes: int
    porcentaje: float


class VisitantesDashboard(BaseModel):
    filtros: FiltroFecha

    kpis: VisitantesKPI

    evolucion: List[SerieFecha]

    por_pais: List[VisitanteItem]
    por_ciudad: List[VisitanteItem]
    por_dispositivo: List[VisitanteItem]
    por_sistema_operativo: List[VisitanteItem]
    por_navegador: List[VisitanteItem]
    por_idioma: List[VisitanteItem]


class VisitanteDetalle(BaseModel):
    id_visitante: int
    identificador: str

    pais: Optional[str] = None
    ciudad: Optional[str] = None
    region: Optional[str] = None

    tipo_dispositivo: Optional[str] = None
    sistema_operativo: Optional[str] = None
    navegador: Optional[str] = None
    idioma: Optional[str] = None

    fecha_primera_visita: datetime
    fecha_ultima_visita: datetime


class VisitanteDetalleResponse(BaseModel):
    datos: List[VisitanteDetalle]
    paginacion: Paginacion


class VisitantesFiltros(BaseModel):
    paises: List[str]
    ciudades: List[str]
    regiones: List[str]

    dispositivos: List[str]
    sistemas_operativos: List[str]
    navegadores: List[str]
    idiomas: List[str]


# ============================================================
# ============================================================
# SESIONES
# ============================================================
# ============================================================

class SesionesKPI(BaseModel):
    total_sesiones: int

    duracion_promedio_segundos: float
    paginas_promedio: float
    tasa_rebote: float


class SesionesDashboard(BaseModel):
    filtros: FiltroFecha

    kpis: SesionesKPI

    evolucion: List[SerieFecha]

    por_fuente: List[RankingItem]

    paginas_entrada: List[RankingItem]
    paginas_salida: List[RankingItem]

    rebotes_por_dia: List[SerieFecha]


class SesionDetalle(BaseModel):
    id_sesion: int
    id_visitante: int

    fuente: Optional[str] = None
    medio: Optional[str] = None
    campania: Optional[str] = None

    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None

    duracion_segundos: Optional[int] = None

    paginas_visitadas: int

    pagina_entrada: Optional[str] = None
    pagina_salida: Optional[str] = None

    es_rebote: bool


class SesionDetalleResponse(BaseModel):
    datos: List[SesionDetalle]
    paginacion: Paginacion


class SesionesFiltros(BaseModel):
    fuentes: List[str]
    medios: List[str]
    campanias: List[str]

    paginas_entrada: List[str]
    paginas_salida: List[str]
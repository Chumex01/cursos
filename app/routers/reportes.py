from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Auditoria,
    Usuarios,
    FuentesTrafico,
    Sesiones,
    Visitantes,
    Eventos,
    Cursos,
    Servicios,
    Proyectos,
)

from app.schemas.reportes import (
    FiltroFecha,

    SerieFecha,
    RankingItem,
    Paginacion,

    # Auditoria
    AuditoriaKPI,
    AuditoriaDashboard,
    AuditoriaDetalle,
    AuditoriaDetalleResponse,
    AuditoriaFiltros,

    # Fuentes
    TraficoKPI,
    FuenteTraficoItem,
    FuentesTraficoDashboard,
    FuenteTraficoDetalle,
    FuenteTraficoDetalleResponse,
    FuentesTraficoFiltros,

    # Eventos
    EventosKPI,
    EventoItem,
    EventosDashboard,
    EventoDetalle,
    EventoDetalleResponse,
    EventosFiltros,

    # Visitantes
    VisitantesKPI,
    VisitanteItem,
    VisitantesDashboard,
    VisitanteDetalle,
    VisitanteDetalleResponse,
    VisitantesFiltros,

    # Sesiones
    SesionesKPI,
    SesionesDashboard,
    SesionDetalle,
    SesionDetalleResponse,
    SesionesFiltros,
)

import math


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes BI"]
)


# ============================================================
# HELPERS
# ============================================================

def porcentaje(valor, total):
    if not total:
        return 0.0

    return round(
        (float(valor) / float(total)) * 100,
        2
    )


def calcular_paginas(total: int, limite: int) -> int:
    if not total:
        return 0

    return math.ceil(total / limite)


def aplicar_fecha(query, columna, desde, hasta):

    if desde is not None:
        query = query.filter(
            columna >= desde
        )

    if hasta is not None:
        query = query.filter(
            columna <= hasta
        )

    return query


def obtener_valores_unicos(
    db: Session,
    columna
):
    filas = (
        db.query(columna)
        .filter(columna.isnot(None))
        .distinct()
        .order_by(columna)
        .all()
    )

    return [
        fila[0]
        for fila in filas
        if fila[0] is not None
    ]


# ============================================================
# ============================================================
# 1. AUDITORIA
# ============================================================
# ============================================================

@router.get(
    "/auditoria/dashboard",
    response_model=AuditoriaDashboard
)
def dashboard_auditoria(

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    accion: Optional[str] = Query(None),
    tabla: Optional[str] = Query(None),
    id_usuario: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = db.query(Auditoria)

    query = aplicar_fecha(
        query,
        Auditoria.fecha_hora,
        desde,
        hasta
    )

    if accion:
        query = query.filter(
            Auditoria.accion == accion
        )

    if tabla:
        query = query.filter(
            Auditoria.tabla == tabla
        )

    if id_usuario:
        query = query.filter(
            Auditoria.id_usuario == id_usuario
        )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_acciones = query.count()

    usuarios_activos = (
        query.with_entities(
            func.count(
                func.distinct(
                    Auditoria.id_usuario
                )
            )
        )
        .scalar()
        or 0
    )

    tablas_afectadas = (
        query.with_entities(
            func.count(
                func.distinct(
                    Auditoria.tabla
                )
            )
        )
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # POR DIA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.date(
                Auditoria.fecha_hora
            ).label("fecha"),

            func.count(
                Auditoria.id_auditoria
            ).label("valor")
        )
        .group_by(
            func.date(
                Auditoria.fecha_hora
            )
        )
        .order_by(
            func.date(
                Auditoria.fecha_hora
            )
        )
        .all()
    )

    por_dia = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR ACCION
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Auditoria.accion.label("nombre"),

            func.count(
                Auditoria.id_auditoria
            ).label("valor")
        )
        .group_by(
            Auditoria.accion
        )
        .order_by(
            desc("valor")
        )
        .all()
    )

    por_accion = [
        RankingItem(
            nombre=f.nombre or "SIN DEFINIR",
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR TABLA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Auditoria.tabla.label("nombre"),

            func.count(
                Auditoria.id_auditoria
            ).label("valor")
        )
        .group_by(
            Auditoria.tabla
        )
        .order_by(
            desc("valor")
        )
        .all()
    )

    por_tabla = [
        RankingItem(
            nombre=f.nombre or "SIN DEFINIR",
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR USUARIO
    # --------------------------------------------------------

    filas = (
        query.join(
            Usuarios,
            Usuarios.id_usuario ==
            Auditoria.id_usuario
        )
        .with_entities(
            func.concat(
                Usuarios.nombres,
                " ",
                Usuarios.primer_apellido
            ).label("nombre"),

            func.count(
                Auditoria.id_auditoria
            ).label("valor")
        )
        .group_by(
            Usuarios.id_usuario,
            Usuarios.nombres,
            Usuarios.primer_apellido
        )
        .order_by(
            desc("valor")
        )
        .all()
    )

    por_usuario = [
        RankingItem(
            nombre=f.nombre,
            valor=float(f.valor)
        )
        for f in filas
    ]

    return AuditoriaDashboard(
        filtros=FiltroFecha(
            desde=desde,
            hasta=hasta
        ),

        kpis=AuditoriaKPI(
            total_acciones=total_acciones,
            usuarios_activos=usuarios_activos,
            tablas_afectadas=tablas_afectadas,
            acciones_periodo=total_acciones
        ),

        por_dia=por_dia,
        por_accion=por_accion,
        por_tabla=por_tabla,
        por_usuario=por_usuario
    )


# ============================================================
# DETALLE AUDITORIA
# ============================================================

@router.get(
    "/auditoria/detalle",
    response_model=AuditoriaDetalleResponse
)
def detalle_auditoria(

    pagina: int = Query(1, ge=1),
    limite: int = Query(25, ge=1, le=100),

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    accion: Optional[str] = Query(None),
    tabla: Optional[str] = Query(None),
    id_usuario: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Auditoria,
            Usuarios
        )
        .join(
            Usuarios,
            Usuarios.id_usuario ==
            Auditoria.id_usuario
        )
    )

    if desde:
        query = query.filter(
            Auditoria.fecha_hora >= desde
        )

    if hasta:
        query = query.filter(
            Auditoria.fecha_hora <= hasta
        )

    if accion:
        query = query.filter(
            Auditoria.accion == accion
        )

    if tabla:
        query = query.filter(
            Auditoria.tabla == tabla
        )

    if id_usuario:
        query = query.filter(
            Auditoria.id_usuario == id_usuario
        )

    total = query.count()

    registros = (
        query
        .order_by(
            Auditoria.fecha_hora.desc()
        )
        .offset(
            (pagina - 1) * limite
        )
        .limit(limite)
        .all()
    )

    datos = []

    for auditoria, usuario in registros:

        datos.append(
            AuditoriaDetalle(
                id_auditoria=
                auditoria.id_auditoria,

                usuario=(
                    f"{usuario.nombres} "
                    f"{usuario.primer_apellido}"
                ),

                accion=auditoria.accion,
                tabla=auditoria.tabla,

                registro_id=
                auditoria.registro_id,

                ip=auditoria.ip,

                fecha_hora=
                auditoria.fecha_hora,

                datos_antiguos=
                auditoria.datos_antiguos,

                datos_nuevos=
                auditoria.datos_nuevos
            )
        )

    return AuditoriaDetalleResponse(
        datos=datos,

        paginacion=Paginacion(
            pagina=pagina,
            limite=limite,
            total=total,
            paginas=calcular_paginas(
                total,
                limite
            )
        )
    )


# ============================================================
# FILTROS AUDITORIA
# ============================================================

@router.get(
    "/auditoria/filtros",
    response_model=AuditoriaFiltros
)
def filtros_auditoria(
    db: Session = Depends(get_db)
):

    acciones = obtener_valores_unicos(
        db,
        Auditoria.accion
    )

    tablas = obtener_valores_unicos(
        db,
        Auditoria.tabla
    )

    usuarios = (
        db.query(Usuarios)
        .join(
            Auditoria,
            Auditoria.id_usuario ==
            Usuarios.id_usuario
        )
        .distinct()
        .order_by(
            Usuarios.nombres,
            Usuarios.primer_apellido
        )
        .all()
    )

    usuarios_response = [
        {
            "id_usuario": usuario.id_usuario,
            "nombre": (
                f"{usuario.nombres} "
                f"{usuario.primer_apellido}"
            )
        }
        for usuario in usuarios
    ]

    return AuditoriaFiltros(
        acciones=acciones,
        tablas=tablas,
        usuarios=usuarios_response
    )


# ============================================================
# ============================================================
# 2. FUENTES DE TRAFICO
# ============================================================
# ============================================================

@router.get(
    "/fuentes-trafico/dashboard",
    response_model=FuentesTraficoDashboard
)
def dashboard_fuentes_trafico(

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    fuente: Optional[str] = Query(None),
    medio: Optional[str] = Query(None),
    campania: Optional[str] = Query(None),
    contenido: Optional[str] = Query(None),
    termino: Optional[str] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(Sesiones)
        .outerjoin(
            FuentesTrafico,
            FuentesTrafico.id_fuente_trafico ==
            Sesiones.id_fuente_trafico
        )
    )

    if desde:
        query = query.filter(
            Sesiones.fecha_inicio >= desde
        )

    if hasta:
        query = query.filter(
            Sesiones.fecha_inicio <= hasta
        )

    if fuente:
        query = query.filter(
            FuentesTrafico.fuente == fuente
        )

    if medio:
        query = query.filter(
            FuentesTrafico.medio == medio
        )

    if campania:
        query = query.filter(
            FuentesTrafico.campania == campania
        )

    if contenido:
        query = query.filter(
            FuentesTrafico.contenido == contenido
        )

    if termino:
        query = query.filter(
            FuentesTrafico.termino == termino
        )

    total_sesiones = query.count()

    # --------------------------------------------------------
    # FUENTES DISTINTAS
    # --------------------------------------------------------

    fuentes_distintas = (
        query.with_entities(
            func.count(
                func.distinct(
                    FuentesTrafico.fuente
                )
            )
        )
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # CAMPAÑAS DISTINTAS
    # --------------------------------------------------------

    campanias_distintas = (
        query.with_entities(
            func.count(
                func.distinct(
                    FuentesTrafico.campania
                )
            )
        )
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # EVOLUCION
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.date(
                Sesiones.fecha_inicio
            ).label("fecha"),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .group_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .order_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .all()
    )

    evolucion = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR FUENTE
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.coalesce(
                FuentesTrafico.fuente,
                "DIRECTO / DESCONOCIDO"
            ).label("nombre"),

            func.count(
                Sesiones.id_sesion
            ).label("sesiones")
        )
        .group_by(
            FuentesTrafico.fuente
        )
        .order_by(
            desc("sesiones")
        )
        .all()
    )

    por_fuente = [
        FuenteTraficoItem(
            nombre=f.nombre,
            sesiones=f.sesiones,
            porcentaje=porcentaje(
                f.sesiones,
                total_sesiones
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR MEDIO
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.coalesce(
                FuentesTrafico.medio,
                "NO DEFINIDO"
            ).label("nombre"),

            func.count(
                Sesiones.id_sesion
            ).label("sesiones")
        )
        .group_by(
            FuentesTrafico.medio
        )
        .order_by(
            desc("sesiones")
        )
        .all()
    )

    por_medio = [
        FuenteTraficoItem(
            nombre=f.nombre,
            sesiones=f.sesiones,
            porcentaje=porcentaje(
                f.sesiones,
                total_sesiones
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # POR CAMPAÑA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.coalesce(
                FuentesTrafico.campania,
                "SIN CAMPAÑA"
            ).label("nombre"),

            func.count(
                Sesiones.id_sesion
            ).label("sesiones")
        )
        .group_by(
            FuentesTrafico.campania
        )
        .order_by(
            desc("sesiones")
        )
        .all()
    )

    por_campania = [
        FuenteTraficoItem(
            nombre=f.nombre,
            sesiones=f.sesiones,
            porcentaje=porcentaje(
                f.sesiones,
                total_sesiones
            )
        )
        for f in filas
    ]

    mejor_fuente = (
        por_fuente[0].nombre
        if por_fuente
        else None
    )

    return FuentesTraficoDashboard(
        filtros=FiltroFecha(
            desde=desde,
            hasta=hasta
        ),

        kpis=TraficoKPI(
            total_sesiones=total_sesiones,
            fuentes_distintas=fuentes_distintas,
            campanias_distintas=campanias_distintas,
            mejor_fuente=mejor_fuente
        ),

        evolucion=evolucion,

        por_fuente=por_fuente,
        por_medio=por_medio,
        por_campania=por_campania
    )


# ============================================================
# DETALLE FUENTES
# ============================================================

@router.get(
    "/fuentes-trafico/detalle",
    response_model=FuenteTraficoDetalleResponse
)
def detalle_fuentes_trafico(

    pagina: int = Query(1, ge=1),
    limite: int = Query(25, ge=1, le=100),

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    fuente: Optional[str] = Query(None),
    medio: Optional[str] = Query(None),
    campania: Optional[str] = Query(None),
    contenido: Optional[str] = Query(None),
    termino: Optional[str] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Sesiones,
            FuentesTrafico
        )
        .outerjoin(
            FuentesTrafico,
            FuentesTrafico.id_fuente_trafico ==
            Sesiones.id_fuente_trafico
        )
    )

    if desde:
        query = query.filter(
            Sesiones.fecha_inicio >= desde
        )

    if hasta:
        query = query.filter(
            Sesiones.fecha_inicio <= hasta
        )

    if fuente:
        query = query.filter(
            FuentesTrafico.fuente == fuente
        )

    if medio:
        query = query.filter(
            FuentesTrafico.medio == medio
        )

    if campania:
        query = query.filter(
            FuentesTrafico.campania == campania
        )

    if contenido:
        query = query.filter(
            FuentesTrafico.contenido == contenido
        )

    if termino:
        query = query.filter(
            FuentesTrafico.termino == termino
        )

    total = query.count()

    registros = (
        query
        .order_by(
            Sesiones.fecha_inicio.desc()
        )
        .offset(
            (pagina - 1) * limite
        )
        .limit(limite)
        .all()
    )

    datos = []

    for sesion, fuente_data in registros:

        datos.append(
            FuenteTraficoDetalle(
                id_sesion=sesion.id_sesion,
                visitante_id=sesion.id_visitante,

                fuente=(
                    fuente_data.fuente
                    if fuente_data
                    else None
                ),

                medio=(
                    fuente_data.medio
                    if fuente_data
                    else None
                ),

                campania=(
                    fuente_data.campania
                    if fuente_data
                    else None
                ),

                contenido=(
                    fuente_data.contenido
                    if fuente_data
                    else None
                ),

                termino=(
                    fuente_data.termino
                    if fuente_data
                    else None
                ),

                fecha_inicio=sesion.fecha_inicio
            )
        )

    return FuenteTraficoDetalleResponse(
        datos=datos,

        paginacion=Paginacion(
            pagina=pagina,
            limite=limite,
            total=total,
            paginas=calcular_paginas(
                total,
                limite
            )
        )
    )


# ============================================================
# FILTROS FUENTES
# ============================================================

@router.get(
    "/fuentes-trafico/filtros",
    response_model=FuentesTraficoFiltros
)
def filtros_fuentes_trafico(
    db: Session = Depends(get_db)
):

    return FuentesTraficoFiltros(
        fuentes=obtener_valores_unicos(
            db,
            FuentesTrafico.fuente
        ),

        medios=obtener_valores_unicos(
            db,
            FuentesTrafico.medio
        ),

        campanias=obtener_valores_unicos(
            db,
            FuentesTrafico.campania
        ),

        contenidos=obtener_valores_unicos(
            db,
            FuentesTrafico.contenido
        ),

        terminos=obtener_valores_unicos(
            db,
            FuentesTrafico.termino
        )
    )


# ============================================================
# ============================================================
# 3. EVENTOS
# ============================================================
# ============================================================

@router.get(
    "/eventos/dashboard",
    response_model=EventosDashboard
)
def dashboard_eventos(

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    tipo_evento: Optional[str] = Query(None),
    pagina: Optional[str] = Query(None),

    id_curso: Optional[int] = Query(None),
    id_servicio: Optional[int] = Query(None),
    id_proyecto: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = db.query(Eventos)

    query = aplicar_fecha(
        query,
        Eventos.fecha_hora,
        desde,
        hasta
    )

    if tipo_evento:
        query = query.filter(
            Eventos.tipo_evento == tipo_evento
        )

    if pagina:
        query = query.filter(
            Eventos.pagina == pagina
        )

    if id_curso:
        query = query.filter(
            Eventos.id_curso == id_curso
        )

    if id_servicio:
        query = query.filter(
            Eventos.id_servicio == id_servicio
        )

    if id_proyecto:
        query = query.filter(
            Eventos.id_proyecto == id_proyecto
        )

    total_eventos = query.count()

    # --------------------------------------------------------
    # SESIONES CON EVENTOS
    # --------------------------------------------------------

    sesiones_con_eventos = (
        query.with_entities(
            func.count(
                func.distinct(
                    Eventos.id_sesion
                )
            )
        )
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # EVOLUCION
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.date(
                Eventos.fecha_hora
            ).label("fecha"),

            func.count(
                Eventos.id_evento
            ).label("valor")
        )
        .group_by(
            func.date(
                Eventos.fecha_hora
            )
        )
        .order_by(
            func.date(
                Eventos.fecha_hora
            )
        )
        .all()
    )

    evolucion = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # TIPO
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Eventos.tipo_evento.label("nombre"),

            func.count(
                Eventos.id_evento
            ).label("cantidad")
        )
        .group_by(
            Eventos.tipo_evento
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    por_tipo = [
        EventoItem(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_eventos
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # PAGINA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Eventos.pagina.label("nombre"),

            func.count(
                Eventos.id_evento
            ).label("cantidad")
        )
        .filter(
            Eventos.pagina.isnot(None)
        )
        .group_by(
            Eventos.pagina
        )
        .order_by(
            desc("cantidad")
        )
        .limit(20)
        .all()
    )

    por_pagina = [
        EventoItem(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_eventos
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # CURSOS
    # --------------------------------------------------------

    filas = (
        query.join(
            Cursos,
            Cursos.id_curso ==
            Eventos.id_curso
        )
        .with_entities(
            Cursos.titulo.label("nombre"),

            func.count(
                Eventos.id_evento
            ).label("cantidad")
        )
        .group_by(
            Cursos.id_curso,
            Cursos.titulo
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    por_curso = [
        EventoItem(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_eventos
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # SERVICIOS
    # --------------------------------------------------------

    filas = (
        query.join(
            Servicios,
            Servicios.id_servicio ==
            Eventos.id_servicio
        )
        .with_entities(
            Servicios.nombre.label("nombre"),

            func.count(
                Eventos.id_evento
            ).label("cantidad")
        )
        .group_by(
            Servicios.id_servicio,
            Servicios.nombre
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    por_servicio = [
        EventoItem(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_eventos
            )
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # PROYECTOS
    # --------------------------------------------------------

    filas = (
        query.join(
            Proyectos,
            Proyectos.id_proyecto ==
            Eventos.id_proyecto
        )
        .with_entities(
            Proyectos.titulo.label("nombre"),

            func.count(
                Eventos.id_evento
            ).label("cantidad")
        )
        .group_by(
            Proyectos.id_proyecto,
            Proyectos.titulo
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    por_proyecto = [
        EventoItem(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_eventos
            )
        )
        for f in filas
    ]

    tipo_principal = (
        por_tipo[0].nombre
        if por_tipo
        else None
    )

    pagina_principal = (
        por_pagina[0].nombre
        if por_pagina
        else None
    )

    return EventosDashboard(
        filtros=FiltroFecha(
            desde=desde,
            hasta=hasta
        ),

        kpis=EventosKPI(
            total_eventos=total_eventos,
            sesiones_con_eventos=sesiones_con_eventos,
            tipo_principal=tipo_principal,
            pagina_principal=pagina_principal
        ),

        evolucion=evolucion,

        por_tipo=por_tipo,
        por_pagina=por_pagina,
        por_curso=por_curso,
        por_servicio=por_servicio,
        por_proyecto=por_proyecto
    )


# ============================================================
# DETALLE EVENTOS
# ============================================================

@router.get(
    "/eventos/detalle",
    response_model=EventoDetalleResponse
)
def detalle_eventos(

    pagina_num: int = Query(
        1,
        ge=1,
        alias="pagina"
    ),

    limite: int = Query(
        25,
        ge=1,
        le=100
    ),

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    tipo_evento: Optional[str] = Query(None),
    pagina: Optional[str] = Query(None),

    id_curso: Optional[int] = Query(None),
    id_servicio: Optional[int] = Query(None),
    id_proyecto: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Eventos,
            Cursos,
            Servicios,
            Proyectos
        )
        .outerjoin(
            Cursos,
            Cursos.id_curso ==
            Eventos.id_curso
        )
        .outerjoin(
            Servicios,
            Servicios.id_servicio ==
            Eventos.id_servicio
        )
        .outerjoin(
            Proyectos,
            Proyectos.id_proyecto ==
            Eventos.id_proyecto
        )
    )

    if desde:
        query = query.filter(
            Eventos.fecha_hora >= desde
        )

    if hasta:
        query = query.filter(
            Eventos.fecha_hora <= hasta
        )

    if tipo_evento:
        query = query.filter(
            Eventos.tipo_evento == tipo_evento
        )

    if pagina:
        query = query.filter(
            Eventos.pagina == pagina
        )

    if id_curso:
        query = query.filter(
            Eventos.id_curso == id_curso
        )

    if id_servicio:
        query = query.filter(
            Eventos.id_servicio == id_servicio
        )

    if id_proyecto:
        query = query.filter(
            Eventos.id_proyecto == id_proyecto
        )

    total = query.count()

    registros = (
        query
        .order_by(
            Eventos.fecha_hora.desc()
        )
        .offset(
            (pagina_num - 1) * limite
        )
        .limit(limite)
        .all()
    )

    datos = []

    for evento, curso, servicio, proyecto in registros:

        datos.append(
            EventoDetalle(
                id_evento=evento.id_evento,
                id_sesion=evento.id_sesion,

                tipo_evento=
                evento.tipo_evento,

                pagina=evento.pagina,

                curso=(
                    curso.titulo
                    if curso
                    else None
                ),

                servicio=(
                    servicio.nombre
                    if servicio
                    else None
                ),

                proyecto=(
                    proyecto.titulo
                    if proyecto
                    else None
                ),

                fecha_hora=
                evento.fecha_hora,

                datos=evento.datos
            )
        )

    return EventoDetalleResponse(
        datos=datos,

        paginacion=Paginacion(
            pagina=pagina_num,
            limite=limite,
            total=total,
            paginas=calcular_paginas(
                total,
                limite
            )
        )
    )


# ============================================================
# FILTROS EVENTOS
# ============================================================

@router.get(
    "/eventos/filtros",
    response_model=EventosFiltros
)
def filtros_eventos(
    db: Session = Depends(get_db)
):

    tipos_evento = obtener_valores_unicos(
        db,
        Eventos.tipo_evento
    )

    paginas = obtener_valores_unicos(
        db,
        Eventos.pagina
    )

    cursos = (
        db.query(
            Cursos.id_curso,
            Cursos.titulo
        )
        .join(
            Eventos,
            Eventos.id_curso ==
            Cursos.id_curso
        )
        .distinct()
        .order_by(
            Cursos.titulo
        )
        .all()
    )

    servicios = (
        db.query(
            Servicios.id_servicio,
            Servicios.nombre
        )
        .join(
            Eventos,
            Eventos.id_servicio ==
            Servicios.id_servicio
        )
        .distinct()
        .order_by(
            Servicios.nombre
        )
        .all()
    )

    proyectos = (
        db.query(
            Proyectos.id_proyecto,
            Proyectos.titulo
        )
        .join(
            Eventos,
            Eventos.id_proyecto ==
            Proyectos.id_proyecto
        )
        .distinct()
        .order_by(
            Proyectos.titulo
        )
        .all()
    )

    return EventosFiltros(

        tipos_evento=tipos_evento,

        paginas=paginas,

        cursos=[
            {
                "id_curso": item.id_curso,
                "titulo": item.titulo
            }
            for item in cursos
        ],

        servicios=[
            {
                "id_servicio": item.id_servicio,
                "nombre": item.nombre
            }
            for item in servicios
        ],

        proyectos=[
            {
                "id_proyecto": item.id_proyecto,
                "titulo": item.titulo
            }
            for item in proyectos
        ]
    )


# ============================================================
# ============================================================
# 4. VISITANTES
# ============================================================
# ============================================================

@router.get(
    "/visitantes/dashboard",
    response_model=VisitantesDashboard
)
def dashboard_visitantes(

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    pais: Optional[str] = Query(None),
    ciudad: Optional[str] = Query(None),
    region: Optional[str] = Query(None),

    dispositivo: Optional[str] = Query(None),
    sistema_operativo: Optional[str] = Query(None),
    navegador: Optional[str] = Query(None),
    idioma: Optional[str] = Query(None),

    db: Session = Depends(get_db)
):

    query = db.query(Visitantes)

    if desde:
        query = query.filter(
            Visitantes.fecha_ultima_visita >= desde
        )

    if hasta:
        query = query.filter(
            Visitantes.fecha_ultima_visita <= hasta
        )

    if pais:
        query = query.filter(
            Visitantes.pais == pais
        )

    if ciudad:
        query = query.filter(
            Visitantes.ciudad == ciudad
        )

    if region:
        query = query.filter(
            Visitantes.region == region
        )

    if dispositivo:
        query = query.filter(
            Visitantes.tipo_dispositivo ==
            dispositivo
        )

    if sistema_operativo:
        query = query.filter(
            Visitantes.sistema_operativo ==
            sistema_operativo
        )

    if navegador:
        query = query.filter(
            Visitantes.navegador ==
            navegador
        )

    if idioma:
        query = query.filter(
            Visitantes.idioma == idioma
        )

    total_visitantes = query.count()

    # --------------------------------------------------------
    # NUEVOS
    # --------------------------------------------------------

    nuevos_query = query

    if desde:
        nuevos_query = nuevos_query.filter(
            Visitantes.fecha_primera_visita >= desde
        )

    if hasta:
        nuevos_query = nuevos_query.filter(
            Visitantes.fecha_primera_visita <= hasta
        )

    nuevos_visitantes = nuevos_query.count()

    visitantes_recurrentes = max(
        total_visitantes -
        nuevos_visitantes,
        0
    )

    # --------------------------------------------------------
    # SESIONES
    # --------------------------------------------------------

    sesiones_totales = (
        db.query(
            func.count(Sesiones.id_sesion)
        )
        .join(
            Visitantes,
            Visitantes.id_visitante ==
            Sesiones.id_visitante
        )
    )

    if desde:
        sesiones_totales = sesiones_totales.filter(
            Sesiones.fecha_inicio >= desde
        )

    if hasta:
        sesiones_totales = sesiones_totales.filter(
            Sesiones.fecha_inicio <= hasta
        )

    if pais:
        sesiones_totales = sesiones_totales.filter(
            Visitantes.pais == pais
        )

    if ciudad:
        sesiones_totales = sesiones_totales.filter(
            Visitantes.ciudad == ciudad
        )

    if dispositivo:
        sesiones_totales = sesiones_totales.filter(
            Visitantes.tipo_dispositivo ==
            dispositivo
        )

    sesiones_totales = (
        sesiones_totales
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # EVOLUCION
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.date(
                Visitantes.fecha_ultima_visita
            ).label("fecha"),

            func.count(
                Visitantes.id_visitante
            ).label("valor")
        )
        .group_by(
            func.date(
                Visitantes.fecha_ultima_visita
            )
        )
        .order_by(
            func.date(
                Visitantes.fecha_ultima_visita
            )
        )
        .all()
    )

    evolucion = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # HELPER RANKING
    # --------------------------------------------------------

    def ranking_visitantes(columna):

        filas = (
            query.with_entities(
                func.coalesce(
                    columna,
                    "NO DEFINIDO"
                ).label("nombre"),

                func.count(
                    Visitantes.id_visitante
                ).label("visitantes")
            )
            .group_by(
                columna
            )
            .order_by(
                desc("visitantes")
            )
            .all()
        )

        return [
            VisitanteItem(
                nombre=f.nombre,
                visitantes=f.visitantes,
                porcentaje=porcentaje(
                    f.visitantes,
                    total_visitantes
                )
            )
            for f in filas
        ]

    # --------------------------------------------------------
    # RANKINGS
    # --------------------------------------------------------

    por_pais = ranking_visitantes(
        Visitantes.pais
    )

    por_ciudad = ranking_visitantes(
        Visitantes.ciudad
    )

    por_dispositivo = ranking_visitantes(
        Visitantes.tipo_dispositivo
    )

    por_sistema_operativo = ranking_visitantes(
        Visitantes.sistema_operativo
    )

    por_navegador = ranking_visitantes(
        Visitantes.navegador
    )

    por_idioma = ranking_visitantes(
        Visitantes.idioma
    )

    pais_principal = (
        por_pais[0].nombre
        if por_pais
        else None
    )

    return VisitantesDashboard(

        filtros=FiltroFecha(
            desde=desde,
            hasta=hasta
        ),

        kpis=VisitantesKPI(
            total_visitantes=total_visitantes,
            nuevos_visitantes=nuevos_visitantes,
            visitantes_recurrentes=
                visitantes_recurrentes,
            sesiones_totales=
                sesiones_totales,
            pais_principal=
                pais_principal
        ),

        evolucion=evolucion,

        por_pais=por_pais,
        por_ciudad=por_ciudad,
        por_dispositivo=por_dispositivo,
        por_sistema_operativo=
            por_sistema_operativo,
        por_navegador=por_navegador,
        por_idioma=por_idioma
    )


# ============================================================
# DETALLE VISITANTES
# ============================================================

@router.get(
    "/visitantes/detalle",
    response_model=VisitanteDetalleResponse
)
def detalle_visitantes(

    pagina: int = Query(1, ge=1),
    limite: int = Query(25, ge=1, le=100),

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    pais: Optional[str] = Query(None),
    ciudad: Optional[str] = Query(None),
    region: Optional[str] = Query(None),

    dispositivo: Optional[str] = Query(None),
    sistema_operativo: Optional[str] = Query(None),
    navegador: Optional[str] = Query(None),
    idioma: Optional[str] = Query(None),

    db: Session = Depends(get_db)
):

    query = db.query(Visitantes)

    if desde:
        query = query.filter(
            Visitantes.fecha_ultima_visita >= desde
        )

    if hasta:
        query = query.filter(
            Visitantes.fecha_ultima_visita <= hasta
        )

    if pais:
        query = query.filter(
            Visitantes.pais == pais
        )

    if ciudad:
        query = query.filter(
            Visitantes.ciudad == ciudad
        )

    if region:
        query = query.filter(
            Visitantes.region == region
        )

    if dispositivo:
        query = query.filter(
            Visitantes.tipo_dispositivo ==
            dispositivo
        )

    if sistema_operativo:
        query = query.filter(
            Visitantes.sistema_operativo ==
            sistema_operativo
        )

    if navegador:
        query = query.filter(
            Visitantes.navegador ==
            navegador
        )

    if idioma:
        query = query.filter(
            Visitantes.idioma ==
            idioma
        )

    total = query.count()

    registros = (
        query
        .order_by(
            Visitantes.fecha_ultima_visita.desc()
        )
        .offset(
            (pagina - 1) * limite
        )
        .limit(limite)
        .all()
    )

    datos = [
        VisitanteDetalle(
            id_visitante=v.id_visitante,

            identificador=v.identificador,

            pais=v.pais,
            ciudad=v.ciudad,
            region=v.region,

            tipo_dispositivo=
                v.tipo_dispositivo,

            sistema_operativo=
                v.sistema_operativo,

            navegador=v.navegador,
            idioma=v.idioma,

            fecha_primera_visita=
                v.fecha_primera_visita,

            fecha_ultima_visita=
                v.fecha_ultima_visita
        )

        for v in registros
    ]

    return VisitanteDetalleResponse(
        datos=datos,

        paginacion=Paginacion(
            pagina=pagina,
            limite=limite,
            total=total,
            paginas=calcular_paginas(
                total,
                limite
            )
        )
    )


# ============================================================
# FILTROS VISITANTES
# ============================================================

@router.get(
    "/visitantes/filtros",
    response_model=VisitantesFiltros
)
def filtros_visitantes(
    db: Session = Depends(get_db)
):

    return VisitantesFiltros(

        paises=obtener_valores_unicos(
            db,
            Visitantes.pais
        ),

        ciudades=obtener_valores_unicos(
            db,
            Visitantes.ciudad
        ),

        regiones=obtener_valores_unicos(
            db,
            Visitantes.region
        ),

        dispositivos=obtener_valores_unicos(
            db,
            Visitantes.tipo_dispositivo
        ),

        sistemas_operativos=
            obtener_valores_unicos(
                db,
                Visitantes.sistema_operativo
            ),

        navegadores=obtener_valores_unicos(
            db,
            Visitantes.navegador
        ),

        idiomas=obtener_valores_unicos(
            db,
            Visitantes.idioma
        )
    )


# ============================================================
# ============================================================
# 5. SESIONES
# ============================================================
# ============================================================

@router.get(
    "/sesiones/dashboard",
    response_model=SesionesDashboard
)
def dashboard_sesiones(

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    fuente: Optional[str] = Query(None),
    medio: Optional[str] = Query(None),
    campania: Optional[str] = Query(None),

    pagina_entrada: Optional[str] = Query(None),
    pagina_salida: Optional[str] = Query(None),

    rebote: Optional[bool] = Query(None),

    id_visitante: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(Sesiones)
        .outerjoin(
            FuentesTrafico,
            FuentesTrafico.id_fuente_trafico ==
            Sesiones.id_fuente_trafico
        )
    )

    if desde:
        query = query.filter(
            Sesiones.fecha_inicio >= desde
        )

    if hasta:
        query = query.filter(
            Sesiones.fecha_inicio <= hasta
        )

    if fuente:
        query = query.filter(
            FuentesTrafico.fuente == fuente
        )

    if medio:
        query = query.filter(
            FuentesTrafico.medio == medio
        )

    if campania:
        query = query.filter(
            FuentesTrafico.campania == campania
        )

    if pagina_entrada:
        query = query.filter(
            Sesiones.pagina_entrada ==
            pagina_entrada
        )

    if pagina_salida:
        query = query.filter(
            Sesiones.pagina_salida ==
            pagina_salida
        )

    if rebote is not None:
        query = query.filter(
            Sesiones.es_rebote == rebote
        )

    if id_visitante:
        query = query.filter(
            Sesiones.id_visitante ==
            id_visitante
        )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_sesiones = query.count()

    duracion_promedio = (
        query.with_entities(
            func.avg(
                Sesiones.duracion_segundos
            )
        )
        .scalar()
        or 0
    )

    paginas_promedio = (
        query.with_entities(
            func.avg(
                Sesiones.paginas_visitadas
            )
        )
        .scalar()
        or 0
    )

    rebotes = (
        query.filter(
            Sesiones.es_rebote == True
        )
        .count()
    )

    tasa_rebote = (
        (rebotes / total_sesiones) * 100
        if total_sesiones
        else 0
    )

    # --------------------------------------------------------
    # EVOLUCION
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.date(
                Sesiones.fecha_inicio
            ).label("fecha"),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .group_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .order_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .all()
    )

    evolucion = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # FUENTES
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            func.coalesce(
                FuentesTrafico.fuente,
                "DIRECTO / DESCONOCIDO"
            ).label("nombre"),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .group_by(
            FuentesTrafico.fuente
        )
        .order_by(
            desc("valor")
        )
        .all()
    )

    por_fuente = [
        RankingItem(
            nombre=f.nombre,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # PAGINAS DE ENTRADA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Sesiones.pagina_entrada.label(
                "nombre"
            ),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .filter(
            Sesiones.pagina_entrada.isnot(None)
        )
        .group_by(
            Sesiones.pagina_entrada
        )
        .order_by(
            desc("valor")
        )
        .limit(20)
        .all()
    )

    paginas_entrada = [
        RankingItem(
            nombre=f.nombre,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # PAGINAS DE SALIDA
    # --------------------------------------------------------

    filas = (
        query.with_entities(
            Sesiones.pagina_salida.label(
                "nombre"
            ),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .filter(
            Sesiones.pagina_salida.isnot(None)
        )
        .group_by(
            Sesiones.pagina_salida
        )
        .order_by(
            desc("valor")
        )
        .limit(20)
        .all()
    )

    paginas_salida = [
        RankingItem(
            nombre=f.nombre,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # --------------------------------------------------------
    # REBOTES POR DIA
    # --------------------------------------------------------

    filas = (
        query
        .filter(
            Sesiones.es_rebote == True
        )
        .with_entities(
            func.date(
                Sesiones.fecha_inicio
            ).label("fecha"),

            func.count(
                Sesiones.id_sesion
            ).label("valor")
        )
        .group_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .order_by(
            func.date(
                Sesiones.fecha_inicio
            )
        )
        .all()
    )

    rebotes_por_dia = [
        SerieFecha(
            fecha=f.fecha,
            valor=float(f.valor)
        )
        for f in filas
    ]

    return SesionesDashboard(

        filtros=FiltroFecha(
            desde=desde,
            hasta=hasta
        ),

        kpis=SesionesKPI(
            total_sesiones=total_sesiones,

            duracion_promedio_segundos=
                round(
                    float(duracion_promedio),
                    2
                ),

            paginas_promedio=
                round(
                    float(paginas_promedio),
                    2
                ),

            tasa_rebote=
                round(
                    float(tasa_rebote),
                    2
                )
        ),

        evolucion=evolucion,

        por_fuente=por_fuente,

        paginas_entrada=
            paginas_entrada,

        paginas_salida=
            paginas_salida,

        rebotes_por_dia=
            rebotes_por_dia
    )


# ============================================================
# DETALLE SESIONES
# ============================================================

@router.get(
    "/sesiones/detalle",
    response_model=SesionDetalleResponse
)
def detalle_sesiones(

    pagina: int = Query(1, ge=1),
    limite: int = Query(25, ge=1, le=100),

    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),

    fuente: Optional[str] = Query(None),
    medio: Optional[str] = Query(None),
    campania: Optional[str] = Query(None),

    pagina_entrada: Optional[str] = Query(None),
    pagina_salida: Optional[str] = Query(None),

    rebote: Optional[bool] = Query(None),

    id_visitante: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Sesiones,
            FuentesTrafico
        )
        .outerjoin(
            FuentesTrafico,
            FuentesTrafico.id_fuente_trafico ==
            Sesiones.id_fuente_trafico
        )
    )

    if desde:
        query = query.filter(
            Sesiones.fecha_inicio >= desde
        )

    if hasta:
        query = query.filter(
            Sesiones.fecha_inicio <= hasta
        )

    if fuente:
        query = query.filter(
            FuentesTrafico.fuente == fuente
        )

    if medio:
        query = query.filter(
            FuentesTrafico.medio == medio
        )

    if campania:
        query = query.filter(
            FuentesTrafico.campania == campania
        )

    if pagina_entrada:
        query = query.filter(
            Sesiones.pagina_entrada ==
            pagina_entrada
        )

    if pagina_salida:
        query = query.filter(
            Sesiones.pagina_salida ==
            pagina_salida
        )

    if rebote is not None:
        query = query.filter(
            Sesiones.es_rebote == rebote
        )

    if id_visitante:
        query = query.filter(
            Sesiones.id_visitante ==
            id_visitante
        )

    total = query.count()

    registros = (
        query
        .order_by(
            Sesiones.fecha_inicio.desc()
        )
        .offset(
            (pagina - 1) * limite
        )
        .limit(limite)
        .all()
    )

    datos = []

    for sesion, fuente_data in registros:

        datos.append(
            SesionDetalle(

                id_sesion=
                sesion.id_sesion,

                id_visitante=
                sesion.id_visitante,

                fuente=(
                    fuente_data.fuente
                    if fuente_data
                    else None
                ),

                medio=(
                    fuente_data.medio
                    if fuente_data
                    else None
                ),

                campania=(
                    fuente_data.campania
                    if fuente_data
                    else None
                ),

                fecha_inicio=
                sesion.fecha_inicio,

                fecha_fin=
                sesion.fecha_fin,

                duracion_segundos=
                sesion.duracion_segundos,

                paginas_visitadas=
                sesion.paginas_visitadas,

                pagina_entrada=
                sesion.pagina_entrada,

                pagina_salida=
                sesion.pagina_salida,

                es_rebote=
                sesion.es_rebote
            )
        )

    return SesionDetalleResponse(

        datos=datos,

        paginacion=Paginacion(
            pagina=pagina,
            limite=limite,
            total=total,
            paginas=calcular_paginas(
                total,
                limite
            )
        )
    )


# ============================================================
# FILTROS SESIONES
# ============================================================

@router.get(
    "/sesiones/filtros",
    response_model=SesionesFiltros
)
def filtros_sesiones(
    db: Session = Depends(get_db)
):

    return SesionesFiltros(

        fuentes=obtener_valores_unicos(
            db,
            FuentesTrafico.fuente
        ),

        medios=obtener_valores_unicos(
            db,
            FuentesTrafico.medio
        ),

        campanias=obtener_valores_unicos(
            db,
            FuentesTrafico.campania
        ),

        paginas_entrada=
            obtener_valores_unicos(
                db,
                Sesiones.pagina_entrada
            ),

        paginas_salida=
            obtener_valores_unicos(
                db,
                Sesiones.pagina_salida
            )
    )
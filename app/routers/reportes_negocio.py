from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Cursos,
    Inscripciones,
    Estudiantes,
    Carrito,
    CarritoItems,
    Pagos,
    Servicios,
    Solicitudes,
)

from app.schemas.reportes_negocio import (
    SeriePeriodo,
    ItemCantidad,

    CursosKPI,
    CursoIngresos,
    CursoProgreso,
    CursosDashboard,

    ServiciosKPI,
    ServicioIngresosPotenciales,
    ServiciosDashboard,
)


router = APIRouter(
    prefix="/reportes/negocio",
    tags=["Reportes de Negocio"]
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


# ============================================================
# ============================================================
# CURSOS
# ============================================================
# ============================================================

@router.get(
    "/cursos/dashboard",
    response_model=CursosDashboard
)
def dashboard_cursos(

    desde: Optional[str] = Query(None),
    hasta: Optional[str] = Query(None),

    nivel: Optional[str] = Query(None),
    es_gratuito: Optional[bool] = Query(None),
    id_curso: Optional[int] = Query(None),

    db: Session = Depends(get_db)
):

    # ========================================================
    # CURSOS
    # ========================================================

    cursos_query = db.query(Cursos).filter(
        Cursos.activo == True
    )

    if nivel:
        cursos_query = cursos_query.filter(
            Cursos.nivel == nivel
        )

    if es_gratuito is not None:
        cursos_query = cursos_query.filter(
            Cursos.es_gratuito == es_gratuito
        )

    if id_curso:
        cursos_query = cursos_query.filter(
            Cursos.id_curso == id_curso
        )

    cursos_activos = cursos_query.count()

    # ========================================================
    # INSCRIPCIONES BASE
    # ========================================================

    inscripciones_query = (
        db.query(Inscripciones)
        .join(
            Cursos,
            Cursos.id_curso ==
            Inscripciones.id_curso
        )
        .filter(
            Cursos.activo == True
        )
    )

    if nivel:
        inscripciones_query = inscripciones_query.filter(
            Cursos.nivel == nivel
        )

    if es_gratuito is not None:
        inscripciones_query = \
            inscripciones_query.filter(
                Cursos.es_gratuito == es_gratuito
            )

    if id_curso:
        inscripciones_query = \
            inscripciones_query.filter(
                Inscripciones.id_curso == id_curso
            )

    if desde:
        inscripciones_query = \
            inscripciones_query.filter(
                Inscripciones.fecha_inscripcion >= desde
            )

    if hasta:
        inscripciones_query = \
            inscripciones_query.filter(
                Inscripciones.fecha_inscripcion <= hasta
            )

    # ========================================================
    # KPI INSCRITOS
    # ========================================================

    estudiantes_inscritos = (
        inscripciones_query
        .with_entities(
            func.count(
                func.distinct(
                    Inscripciones.id_estudiante
                )
            )
        )
        .scalar()
        or 0
    )

    # ========================================================
    # COMPLETADOS
    # ========================================================

    inscripciones_completadas = (
        inscripciones_query
        .filter(
            Inscripciones.fecha_completado.isnot(None)
        )
        .count()
    )

    # ========================================================
    # EVOLUCION INSCRIPCIONES
    # ========================================================

    filas = (
        inscripciones_query
        .with_entities(
            func.date_format(
                Inscripciones.fecha_inscripcion,
                "%Y-%m"
            ).label("periodo"),

            func.count(
                Inscripciones.id_inscripcion
            ).label("valor")
        )
        .group_by(
            func.date_format(
                Inscripciones.fecha_inscripcion,
                "%Y-%m"
            )
        )
        .order_by(
            func.date_format(
                Inscripciones.fecha_inscripcion,
                "%Y-%m"
            )
        )
        .all()
    )

    inscripciones_por_mes = [
        SeriePeriodo(
            periodo=f.periodo,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # ========================================================
    # INSCRIPCIONES POR CURSO
    # ========================================================

    filas = (
        inscripciones_query
        .with_entities(
            Cursos.titulo.label("nombre"),

            func.count(
                Inscripciones.id_inscripcion
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

    total_inscripciones = sum(
        f.cantidad for f in filas
    )

    por_curso = [
        ItemCantidad(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_inscripciones
            )
        )
        for f in filas
    ]

    # ========================================================
    # GRATUITO VS PREMIUM
    # ========================================================

    filas = (
        inscripciones_query
        .with_entities(
            Cursos.es_gratuito.label("gratuito"),

            func.count(
                Inscripciones.id_inscripcion
            ).label("cantidad")
        )
        .group_by(
            Cursos.es_gratuito
        )
        .all()
    )

    total_modelo = sum(
        f.cantidad for f in filas
    )

    gratuito_vs_premium = [
        ItemCantidad(
            nombre=(
                "Gratuitos"
                if f.gratuito
                else "Premium"
            ),
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_modelo
            )
        )
        for f in filas
    ]

    # ========================================================
    # POR NIVEL
    # ========================================================

    filas = (
        inscripciones_query
        .with_entities(
            Cursos.nivel.label("nombre"),

            func.count(
                Inscripciones.id_inscripcion
            ).label("cantidad")
        )
        .group_by(
            Cursos.nivel
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    total_niveles = sum(
        f.cantidad for f in filas
    )

    por_nivel = [
        ItemCantidad(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_niveles
            )
        )
        for f in filas
    ]

    # ========================================================
    # PROGRESO
    # ========================================================

    progreso_data = {
        "0 - 24%": 0,
        "25 - 49%": 0,
        "50 - 74%": 0,
        "75 - 99%": 0,
        "100%": 0,
    }

    progresos = (
        inscripciones_query
        .with_entities(
            Inscripciones.porcentaje_progreso
        )
        .all()
    )

    for registro in progresos:

        progreso = float(
            registro.porcentaje_progreso or 0
        )

        if progreso >= 100:
            progreso_data["100%"] += 1

        elif progreso >= 75:
            progreso_data["75 - 99%"] += 1

        elif progreso >= 50:
            progreso_data["50 - 74%"] += 1

        elif progreso >= 25:
            progreso_data["25 - 49%"] += 1

        else:
            progreso_data["0 - 24%"] += 1

    total_progreso = sum(
        progreso_data.values()
    )

    progreso_estudiantes = [
        CursoProgreso(
            rango=rango,
            cantidad=cantidad,
            porcentaje=porcentaje(
                cantidad,
                total_progreso
            )
        )
        for rango, cantidad
        in progreso_data.items()
    ]

    # ========================================================
    # INGRESOS
    #
    # Se consideran artículos de carrito cuyo carrito
    # posee al menos un pago registrado.
    #
    # Esto evita depender de nombres concretos de estados
    # de Pagos que pueden variar en tu implementación.
    # ========================================================

    pago_existente = (
        db.query(Pagos.id_pago)
        .filter(
            Pagos.id_carrito ==
            CarritoItems.id_carrito
        )
        .exists()
    )

    ingresos_query = (
        db.query(
            CarritoItems,
            Cursos
        )
        .join(
            Cursos,
            Cursos.id_curso ==
            CarritoItems.id_curso
        )
        .filter(
            Cursos.activo == True
        )
        .filter(
            pago_existente
        )
    )

    if nivel:
        ingresos_query = ingresos_query.filter(
            Cursos.nivel == nivel
        )

    if es_gratuito is not None:
        ingresos_query = ingresos_query.filter(
            Cursos.es_gratuito == es_gratuito
        )

    if id_curso:
        ingresos_query = ingresos_query.filter(
            Cursos.id_curso == id_curso
        )

    ingresos_registrados = (
        ingresos_query
        .with_entities(
            func.coalesce(
                func.sum(
                    CarritoItems.subtotal
                ),
                0
            )
        )
        .scalar()
        or 0
    )

    # ========================================================
    # INGRESOS POR CURSO
    # ========================================================

    filas = (
        ingresos_query
        .with_entities(
            Cursos.id_curso.label("id_curso"),

            Cursos.titulo.label("nombre"),

            func.coalesce(
                func.sum(
                    CarritoItems.subtotal
                ),
                0
            ).label("ingresos")
        )
        .group_by(
            Cursos.id_curso,
            Cursos.titulo
        )
        .order_by(
            desc("ingresos")
        )
        .all()
    )

    ingresos_por_curso = [
        CursoIngresos(
            id_curso=f.id_curso,
            nombre=f.nombre,
            ingresos=float(
                f.ingresos or 0
            )
        )
        for f in filas
    ]

    return CursosDashboard(

        kpis=CursosKPI(
            cursos_activos=cursos_activos,

            estudiantes_inscritos=
                estudiantes_inscritos,

            inscripciones_completadas=
                inscripciones_completadas,

            ingresos_registrados=
                float(
                    ingresos_registrados
                )
        ),

        inscripciones_por_mes=
            inscripciones_por_mes,

        por_curso=
            por_curso,

        ingresos_por_curso=
            ingresos_por_curso,

        gratuito_vs_premium=
            gratuito_vs_premium,

        por_nivel=
            por_nivel,

        progreso_estudiantes=
            progreso_estudiantes
    )


# ============================================================
# ============================================================
# FILTROS CURSOS
# ============================================================
# ============================================================

@router.get(
    "/cursos/filtros"
)
def filtros_cursos(
    db: Session = Depends(get_db)
):

    niveles = [
        fila[0]
        for fila in (
            db.query(Cursos.nivel)
            .filter(Cursos.nivel.isnot(None))
            .distinct()
            .order_by(Cursos.nivel)
            .all()
        )
    ]

    cursos = (
        db.query(
            Cursos.id_curso,
            Cursos.titulo
        )
        .filter(
            Cursos.activo == True
        )
        .order_by(
            Cursos.titulo
        )
        .all()
    )

    return {
        "niveles": niveles,

        "tipos": [
            {
                "valor": True,
                "nombre": "Gratuitos"
            },
            {
                "valor": False,
                "nombre": "Premium"
            }
        ],

        "cursos": [
            {
                "id_curso": curso.id_curso,
                "titulo": curso.titulo
            }
            for curso in cursos
        ]
    }


# ============================================================
# ============================================================
# SERVICIOS
# ============================================================
# ============================================================

@router.get(
    "/servicios/dashboard",
    response_model=ServiciosDashboard
)
def dashboard_servicios(

    desde: Optional[str] = Query(None),
    hasta: Optional[str] = Query(None),

    id_servicio: Optional[int] = Query(None),
    estado: Optional[str] = Query(None),

    db: Session = Depends(get_db)
):

    # ========================================================
    # SERVICIOS ACTIVOS
    # ========================================================

    servicios_query = db.query(Servicios).filter(
        Servicios.activo == True
    )

    if id_servicio:
        servicios_query = servicios_query.filter(
            Servicios.id_servicio ==
            id_servicio
        )

    servicios_activos = servicios_query.count()

    # ========================================================
    # SOLICITUDES
    # ========================================================

    solicitudes_query = (
        db.query(
            Solicitudes
        )
        .join(
            Servicios,
            Servicios.id_servicio ==
            Solicitudes.id_servicio
        )
        .filter(
            Servicios.activo == True
        )
    )

    if id_servicio:
        solicitudes_query = \
            solicitudes_query.filter(
                Solicitudes.id_servicio ==
                id_servicio
            )

    if estado:
        solicitudes_query = \
            solicitudes_query.filter(
                Solicitudes.estado ==
                estado
            )

    if desde:
        solicitudes_query = \
            solicitudes_query.filter(
                Solicitudes.fecha_creacion >=
                desde
            )

    if hasta:
        solicitudes_query = \
            solicitudes_query.filter(
                Solicitudes.fecha_creacion <=
                hasta
            )

    solicitudes_totales = \
        solicitudes_query.count()

    # ========================================================
    # CLIENTES REGISTRADOS
    # ========================================================

    clientes_registrados = (
        solicitudes_query
        .with_entities(
            func.count(
                func.distinct(
                    Solicitudes.id_estudiante
                )
            )
        )
        .filter(
            Solicitudes.id_estudiante.isnot(None)
        )
        .scalar()
        or 0
    )

    # ========================================================
    # EVOLUCION MENSUAL
    # ========================================================

    filas = (
        solicitudes_query
        .with_entities(
            func.date_format(
                Solicitudes.fecha_creacion,
                "%Y-%m"
            ).label("periodo"),

            func.count(
                Solicitudes.id_solicitud
            ).label("valor")
        )
        .group_by(
            func.date_format(
                Solicitudes.fecha_creacion,
                "%Y-%m"
            )
        )
        .order_by(
            func.date_format(
                Solicitudes.fecha_creacion,
                "%Y-%m"
            )
        )
        .all()
    )

    solicitudes_por_mes = [
        SeriePeriodo(
            periodo=f.periodo,
            valor=float(f.valor)
        )
        for f in filas
    ]

    # ========================================================
    # SOLICITUDES POR SERVICIO
    # ========================================================

    filas = (
        solicitudes_query
        .with_entities(
            Servicios.nombre.label("nombre"),

            func.count(
                Solicitudes.id_solicitud
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

    total_solicitudes = sum(
        f.cantidad for f in filas
    )

    por_servicio = [
        ItemCantidad(
            nombre=f.nombre,
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_solicitudes
            )
        )
        for f in filas
    ]

    servicio_mas_solicitado = (
        por_servicio[0].nombre
        if por_servicio
        else None
    )

    # ========================================================
    # ESTADOS
    # ========================================================

    filas = (
        solicitudes_query
        .with_entities(
            Solicitudes.estado.label("nombre"),

            func.count(
                Solicitudes.id_solicitud
            ).label("cantidad")
        )
        .group_by(
            Solicitudes.estado
        )
        .order_by(
            desc("cantidad")
        )
        .all()
    )

    total_estados = sum(
        f.cantidad for f in filas
    )

    por_estado = [
        ItemCantidad(
            nombre=f.nombre or "SIN ESTADO",
            cantidad=f.cantidad,
            porcentaje=porcentaje(
                f.cantidad,
                total_estados
            )
        )
        for f in filas
    ]

    # ========================================================
    # TIPO DE CLIENTE
    # ========================================================

    particulares = (
        solicitudes_query
        .filter(
            Solicitudes.empresa.is_(None)
        )
        .count()
    )

    empresas = (
        solicitudes_query
        .filter(
            Solicitudes.empresa.isnot(None)
        )
        .count()
    )

    total_clientes = \
        particulares + empresas

    tipo_cliente = [
        ItemCantidad(
            nombre="Particulares",
            cantidad=particulares,
            porcentaje=porcentaje(
                particulares,
                total_clientes
            )
        ),

        ItemCantidad(
            nombre="Empresas",
            cantidad=empresas,
            porcentaje=porcentaje(
                empresas,
                total_clientes
            )
        )
    ]

    # ========================================================
    # DEMANDA + VALOR REFERENCIAL
    # ========================================================

    filas = (
        solicitudes_query
        .with_entities(
            Servicios.id_servicio.label(
                "id_servicio"
            ),

            Servicios.nombre.label(
                "nombre"
            ),

            Servicios.precio_base.label(
                "precio_base"
            ),

            func.count(
                Solicitudes.id_solicitud
            ).label(
                "solicitudes"
            )
        )
        .group_by(
            Servicios.id_servicio,
            Servicios.nombre,
            Servicios.precio_base
        )
        .order_by(
            desc("solicitudes")
        )
        .all()
    )

    demanda_servicios = [
        ServicioIngresosPotenciales(
            id_servicio=f.id_servicio,

            nombre=f.nombre,

            solicitudes=f.solicitudes,

            precio_base=float(
                f.precio_base or 0
            ),

            valor_referencial=float(
                (f.precio_base or 0) *
                f.solicitudes
            )
        )
        for f in filas
    ]

    return ServiciosDashboard(

        kpis=ServiciosKPI(
            servicios_activos=
                servicios_activos,

            solicitudes_totales=
                solicitudes_totales,

            clientes_registrados=
                clientes_registrados,

            servicio_mas_solicitado=
                servicio_mas_solicitado
        ),

        solicitudes_por_mes=
            solicitudes_por_mes,

        por_servicio=
            por_servicio,

        por_estado=
            por_estado,

        tipo_cliente=
            tipo_cliente,

        demanda_servicios=
            demanda_servicios
    )


# ============================================================
# FILTROS SERVICIOS
# ============================================================

@router.get(
    "/servicios/filtros"
)
def filtros_servicios(
    db: Session = Depends(get_db)
):

    servicios = (
        db.query(
            Servicios.id_servicio,
            Servicios.nombre
        )
        .filter(
            Servicios.activo == True
        )
        .order_by(
            Servicios.nombre
        )
        .all()
    )

    estados = [
        fila[0]
        for fila in (
            db.query(
                Solicitudes.estado
            )
            .filter(
                Solicitudes.estado.isnot(None)
            )
            .distinct()
            .order_by(
                Solicitudes.estado
            )
            .all()
        )
    ]

    return {

        "servicios": [
            {
                "id_servicio":
                    servicio.id_servicio,

                "nombre":
                    servicio.nombre
            }

            for servicio in servicios
        ],

        "estados": estados
    }
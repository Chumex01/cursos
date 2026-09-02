from datetime import datetime, timezone
from typing import List, Optional

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.database import get_db


router = APIRouter(prefix="/public", tags=["public"])


# ============================================================
# CONFIGURACIÓN DE CORREO
# ============================================================

SMTP_USER = "chumex012020@gmail.com"
SMTP_PASS = "tu_contraseña_de_aplicacion_aqui"


# ============================================================
# ESQUEMAS
# ============================================================

class TechOut(BaseModel):
    nombre: str
    categoria: str

    model_config = ConfigDict(from_attributes=True)


class ProyectoLandingOut(BaseModel):
    id_proyecto: int
    titulo: str
    slug: str
    descripcion_corta: str
    url_demo: Optional[str] = None
    url_github: Optional[str] = None
    tecnologias: List[TechOut] = []

    model_config = ConfigDict(from_attributes=True)


class CursoLandingOut(BaseModel):
    id_curso: int
    titulo: str
    slug: str
    descripcion: str
    nivel: str
    precio: float
    moneda: str
    es_gratuito: bool
    total_estudiantes: int = 0

    model_config = ConfigDict(from_attributes=True)


class ServicioLandingOut(BaseModel):
    id_servicio: int
    nombre: str
    descripcion: str
    precio_base: float
    moneda: str
    carga_horaria: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EstadisticasOut(BaseModel):
    total_estudiantes: int
    total_proyectos: int
    total_cursos: int


class ContactoForm(BaseModel):
    nombre: str
    email: EmailStr
    empresa: Optional[str] = None
    servicio_solicitado: str
    mensaje: str


class LeccionOut(BaseModel):
    id_leccion: int
    id_curso: int
    titulo: str
    descripcion: Optional[str] = None
    duracion_minutos: int
    es_preview: bool
    orden: int
    completada: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class CursoDetalleOut(BaseModel):
    id_curso: int
    titulo: str
    slug: str
    descripcion: str
    nivel: str
    precio: float
    moneda: str
    es_gratuito: bool
    total_estudiantes: int = 0
    lecciones: List[LeccionOut] = []

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# ENDPOINTS LANDING
# ============================================================

@router.get("/estadisticas", response_model=EstadisticasOut)
def get_estadisticas(db: Session = Depends(get_db)):
    total_estudiantes = (
        db.query(func.count(models.Estudiantes.id_estudiante))
        .scalar()
        or 0
    )

    total_proyectos = (
        db.query(func.count(models.Proyectos.id_proyecto))
        .filter(models.Proyectos.activo == True)
        .scalar()
        or 0
    )

    total_cursos = (
        db.query(func.count(models.Cursos.id_curso))
        .filter(models.Cursos.activo == True)
        .scalar()
        or 0
    )

    return EstadisticasOut(
        total_estudiantes=total_estudiantes,
        total_proyectos=total_proyectos,
        total_cursos=total_cursos,
    )


@router.get("/servicios", response_model=List[ServicioLandingOut])
def get_servicios_landing(db: Session = Depends(get_db)):
    return (
        db.query(models.Servicios)
        .filter(models.Servicios.activo == True)
        .limit(3)
        .all()
    )


@router.get("/proyectos", response_model=List[ProyectoLandingOut])
def get_proyectos_landing(db: Session = Depends(get_db)):
    proyectos = (
        db.query(models.Proyectos)
        .filter(
            models.Proyectos.activo == True,
            models.Proyectos.destacado == True,
        )
        .limit(3)
        .all()
    )

    if not proyectos:
        return []

    proyecto_ids = [p.id_proyecto for p in proyectos]

    relaciones = (
        db.query(models.ProyectosTecnologias)
        .filter(
            models.ProyectosTecnologias.id_proyecto.in_(proyecto_ids)
        )
        .all()
    )

    tech_ids = list(set(r.id_tecnologia for r in relaciones))

    if tech_ids:
        tecnologias_db = (
            db.query(models.Tecnologias)
            .filter(
                models.Tecnologias.id_tecnologia.in_(tech_ids)
            )
            .all()
        )
    else:
        tecnologias_db = []

    tech_dict = {
        t.id_tecnologia: t
        for t in tecnologias_db
    }

    rel_dict = {}

    for r in relaciones:
        if r.id_proyecto not in rel_dict:
            rel_dict[r.id_proyecto] = []

        if r.id_tecnologia in tech_dict:
            rel_dict[r.id_proyecto].append(
                tech_dict[r.id_tecnologia]
            )

    return [
        ProyectoLandingOut(
            id_proyecto=p.id_proyecto,
            titulo=p.titulo,
            slug=p.slug,
            descripcion_corta=p.descripcion_corta,
            url_demo=p.url_demo,
            url_github=p.url_github,
            tecnologias=rel_dict.get(p.id_proyecto, []),
        )
        for p in proyectos
    ]


@router.get("/cursos", response_model=List[CursoLandingOut])
def get_cursos_landing(db: Session = Depends(get_db)):
    cursos_data = (
        db.query(
            models.Cursos,
            func.count(
                models.Inscripciones.id_inscripcion
            ).label("total_estudiantes"),
        )
        .outerjoin(
            models.Inscripciones,
            models.Inscripciones.id_curso
            == models.Cursos.id_curso,
        )
        .filter(models.Cursos.activo == True)
        .group_by(models.Cursos.id_curso)
        .limit(4)
        .all()
    )

    resultado = []

    for curso, total_est in cursos_data:
        resultado.append(
            CursoLandingOut(
                id_curso=curso.id_curso,
                titulo=curso.titulo,
                slug=curso.slug,
                descripcion=curso.descripcion,
                nivel=curso.nivel,
                precio=float(curso.precio),
                moneda=curso.moneda,
                es_gratuito=curso.es_gratuito,
                total_estudiantes=total_est,
            )
        )

    return resultado


# ============================================================
# ENDPOINTS PÁGINAS INTERNAS
# ============================================================

@router.get("/servicios/todos", response_model=List[ServicioLandingOut])
def get_servicios_todos(db: Session = Depends(get_db)):
    return (
        db.query(models.Servicios)
        .filter(models.Servicios.activo == True)
        .all()
    )


@router.get("/proyectos/todos", response_model=List[ProyectoLandingOut])
def get_proyectos_todos(db: Session = Depends(get_db)):
    proyectos = (
        db.query(models.Proyectos)
        .filter(models.Proyectos.activo == True)
        .order_by(models.Proyectos.fecha_creacion.desc())
        .all()
    )

    if not proyectos:
        return []

    proyecto_ids = [p.id_proyecto for p in proyectos]

    relaciones = (
        db.query(models.ProyectosTecnologias)
        .filter(
            models.ProyectosTecnologias.id_proyecto.in_(proyecto_ids)
        )
        .all()
    )

    tech_ids = list(set(r.id_tecnologia for r in relaciones))

    if tech_ids:
        tecnologias_db = (
            db.query(models.Tecnologias)
            .filter(
                models.Tecnologias.id_tecnologia.in_(tech_ids)
            )
            .all()
        )
    else:
        tecnologias_db = []

    tech_dict = {
        t.id_tecnologia: t
        for t in tecnologias_db
    }

    rel_dict = {}

    for r in relaciones:
        if r.id_proyecto not in rel_dict:
            rel_dict[r.id_proyecto] = []

        if r.id_tecnologia in tech_dict:
            rel_dict[r.id_proyecto].append(
                tech_dict[r.id_tecnologia]
            )

    return [
        ProyectoLandingOut(
            id_proyecto=p.id_proyecto,
            titulo=p.titulo,
            slug=p.slug,
            descripcion_corta=p.descripcion_corta,
            url_demo=p.url_demo,
            url_github=p.url_github,
            tecnologias=rel_dict.get(p.id_proyecto, []),
        )
        for p in proyectos
    ]


@router.get("/cursos/todos", response_model=List[CursoLandingOut])
def get_cursos_todos(db: Session = Depends(get_db)):
    cursos_data = (
        db.query(
            models.Cursos,
            func.count(
                models.Inscripciones.id_inscripcion
            ).label("total_estudiantes"),
        )
        .outerjoin(
            models.Inscripciones,
            models.Inscripciones.id_curso
            == models.Cursos.id_curso,
        )
        .filter(models.Cursos.activo == True)
        .group_by(models.Cursos.id_curso)
        .all()
    )

    return [
        CursoLandingOut(
            id_curso=curso.id_curso,
            titulo=curso.titulo,
            slug=curso.slug,
            descripcion=curso.descripcion,
            nivel=curso.nivel,
            precio=float(curso.precio),
            moneda=curso.moneda,
            es_gratuito=curso.es_gratuito,
            total_estudiantes=total,
        )
        for curso, total in cursos_data
    ]


# ============================================================
# DETALLE DEL CURSO
# ============================================================

@router.get("/cursos/{slug}", response_model=CursoDetalleOut)
def get_curso_detalle(
    slug: str,
    db: Session = Depends(get_db),
):
    # 1. Obtener el curso
    curso = (
        db.query(models.Cursos)
        .filter(
            models.Cursos.slug == slug,
            models.Cursos.activo == True,
        )
        .first()
    )

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado",
        )

    # 2. Contar estudiantes
    total_estudiantes = (
        db.query(
            func.count(models.Inscripciones.id_inscripcion)
        )
        .filter(
            models.Inscripciones.id_curso
            == curso.id_curso
        )
        .scalar()
        or 0
    )

    # 3. Obtener lecciones ordenadas
    lecciones_db = (
        db.query(models.Lecciones)
        .filter(
            models.Lecciones.id_curso == curso.id_curso,
            models.Lecciones.activo == True,
        )
        .order_by(models.Lecciones.orden)
        .all()
    )

    # 4. Buscar inscripción del estudiante
    #    Actualmente está hardcodeado al estudiante ID 1.
    inscripcion = (
        db.query(models.Inscripciones)
        .filter(
            models.Inscripciones.id_estudiante == 1,
            models.Inscripciones.id_curso == curso.id_curso,
            models.Inscripciones.estado == "INSCRITO",
        )
        .first()
    )

    lecciones_out = []

    if inscripcion:
        # Obtener todas las lecciones completadas
        progreso_db = (
            db.query(models.ProgresoLecciones)
            .filter(
                models.ProgresoLecciones.id_inscripcion
                == inscripcion.id_inscripcion,
                models.ProgresoLecciones.fecha_completada
                != None,
            )
            .all()
        )

        progreso_ids = {
            p.id_leccion
            for p in progreso_db
        }

        for lec in lecciones_db:
            lecciones_out.append(
                LeccionOut(
                    id_leccion=lec.id_leccion,
                    id_curso=lec.id_curso,
                    titulo=lec.titulo,
                    descripcion=lec.descripcion,
                    duracion_minutos=lec.duracion_minutos,
                    es_preview=lec.es_preview,
                    orden=lec.orden,
                    completada=lec.id_leccion in progreso_ids,
                )
            )

    else:
        for lec in lecciones_db:
            lecciones_out.append(
                LeccionOut(
                    id_leccion=lec.id_leccion,
                    id_curso=lec.id_curso,
                    titulo=lec.titulo,
                    descripcion=lec.descripcion,
                    duracion_minutos=lec.duracion_minutos,
                    es_preview=lec.es_preview,
                    orden=lec.orden,
                    completada=False,
                )
            )

    return CursoDetalleOut(
        id_curso=curso.id_curso,
        titulo=curso.titulo,
        slug=curso.slug,
        descripcion=curso.descripcion,
        nivel=curso.nivel,
        precio=float(curso.precio),
        moneda=curso.moneda,
        es_gratuito=curso.es_gratuito,
        total_estudiantes=total_estudiantes,
        lecciones=lecciones_out,
    )


# ============================================================
# PROGRESO DEL CURSO
# ============================================================

@router.post("/cursos/{slug}/progreso")
def guardar_progreso(
    slug: str,
    data: dict,
    db: Session = Depends(get_db),
):
    # 1. Buscar curso
    curso = (
        db.query(models.Cursos)
        .filter(models.Cursos.slug == slug)
        .first()
    )

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado",
        )

    # 2. Buscar inscripción
    inscripcion = (
        db.query(models.Inscripciones)
        .filter(
            models.Inscripciones.id_estudiante == 1,
            models.Inscripciones.id_curso
            == curso.id_curso,
            models.Inscripciones.estado == "INSCRITO",
        )
        .first()
    )

    if not inscripcion:
        raise HTTPException(
            status_code=400,
            detail="No estás inscrito en este curso.",
        )

    # 3. Buscar lección
    leccion = (
        db.query(models.Lecciones)
        .filter(
            models.Lecciones.id_leccion
            == data["id_leccion"],
            models.Lecciones.id_curso
            == curso.id_curso,
        )
        .first()
    )

    if not leccion:
        raise HTTPException(
            status_code=404,
            detail="La lección no pertenece al curso.",
        )

    # 4. Buscar progreso existente
    existe_progreso = (
        db.query(models.ProgresoLecciones)
        .filter(
            models.ProgresoLecciones.id_inscripcion
            == inscripcion.id_inscripcion,
            models.ProgresoLecciones.id_leccion
            == data["id_leccion"],
        )
        .first()
    )

    # 5. Desmarcar
    if existe_progreso and not data.get("completada"):
        db.delete(existe_progreso)
        db.commit()

        return {
            "mensaje": "Lección desmarcada."
        }

    # 6. Marcar como completada
    if not existe_progreso and data.get("completada"):
        nuevo_progreso = models.ProgresoLecciones(
            id_inscripcion=inscripcion.id_inscripcion,
            id_leccion=data["id_leccion"],
            porcentaje=100.0,
            fecha_completada=datetime.now(timezone.utc),
        )

        db.add(nuevo_progreso)
        db.commit()

        return {
            "mensaje": "¡Lección marcada como completada!"
        }

    # 7. Ya estaba completada
    return {
        "mensaje": "Ya estaba completada."
    }
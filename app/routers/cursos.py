from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/cursos", tags=["Cursos"])

@router.get("/")
def listar_cursos(
    nivel: Optional[str] = None,
    es_gratuito: Optional[bool] = None,
    busqueda: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Cursos).filter(models.Cursos.activo == True)
    
    if nivel and nivel != "Todos":
        query = query.filter(models.Cursos.nivel == nivel)
    if es_gratuito is not None:
        query = query.filter(models.Cursos.es_gratuito == es_gratuito)
    if busqueda:
        query = query.filter(models.Cursos.titulo.ilike(f"%{busqueda}%"))
        
    return query.all()

@router.get("/{slug}")
def obtener_curso_por_slug(slug: str, db: Session = Depends(get_db)):
    curso = db.query(models.Cursos).filter(models.Cursos.slug == slug, models.Cursos.activo == True).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/{id_curso}/inscripcion-gratis")
def inscribir_curso_gratuito(id_curso: int, id_estudiante: int, db: Session = Depends(get_db)):
    curso = db.query(models.Cursos).filter(models.Cursos.id_curso == id_curso).first()
    if not curso or not curso.es_gratuito:
        raise HTTPException(status_code=400, detail="El curso no es gratuito o no existe")

    # Crear o recuperar inscripción
    inscripcion = db.query(models.Inscripciones).filter(
        models.Inscripciones.id_estudiante == id_estudiante,
        models.Inscripciones.id_curso == id_curso
    ).first()

    if not inscripcion:
        inscripcion = models.Inscripciones(
            id_estudiante=id_estudiante,
            id_curso=id_curso,
            estado="INSCRITO"
        )
        db.add(inscripcion)
        db.commit()
        db.refresh(inscripcion)

    return {"status": "ok", "id_inscripcion": inscripcion.id_inscripcion}

@router.post("/progreso/{id_inscripcion}/leccion/{id_leccion}")
def marcar_leccion_completada(id_inscripcion: int, id_leccion: int, db: Session = Depends(get_db)):
    progreso = db.query(models.ProgresoLecciones).filter(
        models.ProgresoLecciones.id_inscripcion == id_inscripcion,
        models.ProgresoLecciones.id_leccion == id_leccion
    ).first()

    if not progreso:
        progreso = models.ProgresoLecciones(
            id_inscripcion=id_inscripcion,
            id_leccion=id_leccion,
            porcentaje=100.00
        )
        db.add(progreso)
    else:
        progreso.porcentaje = 100.00

    db.commit()
    return {"status": "completado"}
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Esquema de un estudiante individual
class EstudianteGet(BaseModel):
    nombres: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    # Ojo: Devolver el correo públicamente en internet puede ser un problema de privacidad.
    # Te recomiendo omitirlo para el front, pero lo dejo según lo pediste.
    correo: str 
    
    model_config = ConfigDict(from_attributes=True)

# Esquema de la respuesta completa (Lista + Count)
class EstudiantesResponse(BaseModel):
    total: int
    estudiantes: List[EstudianteGet]
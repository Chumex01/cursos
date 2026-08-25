from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.database import Base


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def utc_now():
    return datetime.now(timezone.utc)


# ============================================================
# 1. USUARIOS
# Administración del sistema
# ============================================================

class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(50), nullable=False)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=True)

    correo = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    rol = Column(String(50), nullable=False, default="ADMIN")
    activo = Column(Boolean, nullable=False, default=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    auditorias = relationship(
        "Auditoria",
        back_populates="usuario"
    )


# ============================================================
# 2. ESTUDIANTES
# Usuarios que consumen los cursos
# ============================================================

class Estudiantes(Base):
    __tablename__ = "estudiantes"

    id_estudiante = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(50), nullable=False)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=True)

    correo = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    activo = Column(Boolean, nullable=False, default=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relaciones
    inscripciones = relationship(
        "Inscripciones",
        back_populates="estudiante"
    )

    carritos = relationship(
        "Carrito",
        back_populates="estudiante"
    )

    pagos = relationship(
        "Pagos",
        back_populates="estudiante"
    )

    solicitudes = relationship(
        "Solicitudes",
        back_populates="estudiante"
    )


# ============================================================
# 3. SERVICIOS
# Servicios profesionales del portafolio
# ============================================================

class Servicios(Base):
    __tablename__ = "servicios"

    id_servicio = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)

    precio_base = Column(
        Numeric(10, 2),
        nullable=False
    )

    moneda = Column(String(10), nullable=False, default="BOB")

    carga_horaria = Column(
        String(100),
        nullable=True
    )

    activo = Column(Boolean, nullable=False, default=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    solicitudes = relationship(
        "Solicitudes",
        back_populates="servicio"
    )


# ============================================================
# 4. CURSOS
# Modelo Freemium
# ============================================================

class Cursos(Base):
    __tablename__ = "cursos"

    id_curso = Column(Integer, primary_key=True, index=True)

    titulo = Column(String(100), nullable=False)
    slug = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    descripcion = Column(Text, nullable=False)

    imagen_principal_url = Column(
        String(255),
        nullable=True
    )

    nivel = Column(String(50), nullable=False)

    precio = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    moneda = Column(
        String(10),
        nullable=False,
        default="BOB"
    )

    es_gratuito = Column(
        Boolean,
        nullable=False,
        default=True
    )

    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relaciones
    lecciones = relationship(
        "Lecciones",
        back_populates="curso",
        cascade="all, delete-orphan"
    )

    inscripciones = relationship(
        "Inscripciones",
        back_populates="curso"
    )

    carrito_items = relationship(
        "CarritoItems",
        back_populates="curso"
    )

    eventos = relationship(
        "Eventos",
        back_populates="curso"
    )


# ============================================================
# 5. LECCIONES
# ============================================================

class Lecciones(Base):
    __tablename__ = "lecciones"

    id_leccion = Column(Integer, primary_key=True, index=True)

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    contenido = Column(Text, nullable=False)

    orden = Column(Integer, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)

    # Permite mostrar una lección gratis
    # aunque el curso completo sea premium.
    es_preview = Column(
        Boolean,
        nullable=False,
        default=False
    )

    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    curso = relationship(
        "Cursos",
        back_populates="lecciones"
    )

    progresos = relationship(
        "ProgresoLecciones",
        back_populates="leccion"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_curso",
            "orden",
            name="uq_leccion_curso_orden"
        ),
    )


# ============================================================
# 6. INSCRIPCIONES
# Un estudiante puede inscribirse a varios cursos
# ============================================================

class Inscripciones(Base):
    __tablename__ = "inscripciones"

    id_inscripcion = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_estudiante = Column(
        Integer,
        ForeignKey("estudiantes.id_estudiante"),
        nullable=False,
        index=True
    )

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso"),
        nullable=False,
        index=True
    )

    estado = Column(
        String(50),
        nullable=False,
        default="INSCRITO"
    )

    porcentaje_progreso = Column(
        Numeric(5, 2),
        nullable=False,
        default=0
    )

    fecha_inscripcion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_inicio = Column(
        DateTime(timezone=True),
        nullable=True
    )

    fecha_completado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    estudiante = relationship(
        "Estudiantes",
        back_populates="inscripciones"
    )

    curso = relationship(
        "Cursos",
        back_populates="inscripciones"
    )

    progresos = relationship(
        "ProgresoLecciones",
        back_populates="inscripcion",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_estudiante",
            "id_curso",
            name="uq_estudiante_curso"
        ),
    )


# ============================================================
# 7. PROGRESO DE LECCIONES
# ============================================================

class ProgresoLecciones(Base):
    __tablename__ = "progreso_lecciones"

    id_progreso_leccion = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_inscripcion = Column(
        Integer,
        ForeignKey(
            "inscripciones.id_inscripcion",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    id_leccion = Column(
        Integer,
        ForeignKey(
            "lecciones.id_leccion",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    porcentaje = Column(
        Numeric(5, 2),
        nullable=False,
        default=0
    )

    fecha_inicio = Column(
        DateTime(timezone=True),
        nullable=True
    )

    fecha_ultima_actividad = Column(
        DateTime(timezone=True),
        nullable=True
    )

    fecha_completado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    inscripcion = relationship(
        "Inscripciones",
        back_populates="progresos"
    )

    leccion = relationship(
        "Lecciones",
        back_populates="progresos"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_inscripcion",
            "id_leccion",
            name="uq_progreso_inscripcion_leccion"
        ),
    )


# ============================================================
# 8. CARRITO
# Exclusivamente para desbloquear cursos
# ============================================================

class Carrito(Base):
    __tablename__ = "carrito"

    id_carrito = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_estudiante = Column(
        Integer,
        ForeignKey("estudiantes.id_estudiante"),
        nullable=False,
        index=True
    )

    estado = Column(
        String(50),
        nullable=False,
        default="ABIERTO"
    )

    moneda = Column(
        String(10),
        nullable=False,
        default="BOB"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    estudiante = relationship(
        "Estudiantes",
        back_populates="carritos"
    )

    items = relationship(
        "CarritoItems",
        back_populates="carrito",
        cascade="all, delete-orphan"
    )

    pagos = relationship(
        "Pagos",
        back_populates="carrito"
    )


# ============================================================
# 9. CARRITO ITEMS
# ============================================================

class CarritoItems(Base):
    __tablename__ = "carrito_items"

    id_carrito_item = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_carrito = Column(
        Integer,
        ForeignKey(
            "carrito.id_carrito",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso"),
        nullable=False,
        index=True
    )

    cantidad = Column(
        Integer,
        nullable=False,
        default=1
    )

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    carrito = relationship(
        "Carrito",
        back_populates="items"
    )

    curso = relationship(
        "Cursos",
        back_populates="carrito_items"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_carrito",
            "id_curso",
            name="uq_carrito_curso"
        ),
    )


# ============================================================
# 10. PAGOS
# Pasarela simulada
# ============================================================

class Pagos(Base):
    __tablename__ = "pagos"

    id_pago = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_carrito = Column(
        Integer,
        ForeignKey("carrito.id_carrito"),
        nullable=False,
        index=True
    )

    id_estudiante = Column(
        Integer,
        ForeignKey("estudiantes.id_estudiante"),
        nullable=False,
        index=True
    )

    monto = Column(
        Numeric(10, 2),
        nullable=False
    )

    moneda = Column(
        String(10),
        nullable=False,
        default="BOB"
    )

    metodo_pago = Column(
        String(50),
        nullable=False
    )

    estado = Column(
        String(50),
        nullable=False
    )

    codigo_transaccion = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    fecha_pago = Column(
        DateTime(timezone=True),
        nullable=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    carrito = relationship(
        "Carrito",
        back_populates="pagos"
    )

    estudiante = relationship(
        "Estudiantes",
        back_populates="pagos"
    )


# ============================================================
# 11. SOLICITUDES
# Solicitudes de servicios.
# NO utilizan carrito.
# ============================================================

class Solicitudes(Base):
    __tablename__ = "solicitudes"

    id_solicitud = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Puede ser NULL porque una persona puede solicitar
    # un servicio sin registrarse como estudiante.
    id_estudiante = Column(
        Integer,
        ForeignKey("estudiantes.id_estudiante"),
        nullable=True,
        index=True
    )

    id_servicio = Column(
        Integer,
        ForeignKey("servicios.id_servicio"),
        nullable=False,
        index=True
    )

    nombre_cliente = Column(
        String(150),
        nullable=False
    )

    correo_cliente = Column(
        String(150),
        nullable=False,
        index=True
    )

    empresa = Column(
        String(150),
        nullable=True
    )

    mensaje = Column(
        Text,
        nullable=False
    )

    estado = Column(
        String(50),
        nullable=False,
        default="NUEVA"
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    estudiante = relationship(
        "Estudiantes",
        back_populates="solicitudes"
    )

    servicio = relationship(
        "Servicios",
        back_populates="solicitudes"
    )


# ============================================================
# 12. AUDITORIA
# Acciones realizadas por administradores
# ============================================================

class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        index=True
    )

    accion = Column(
        String(100),
        nullable=False
    )

    tabla = Column(
        String(100),
        nullable=False
    )

    registro_id = Column(
        Integer,
        nullable=True
    )

    datos_antiguos = Column(
        JSON,
        nullable=True
    )

    datos_nuevos = Column(
        JSON,
        nullable=True
    )

    ip = Column(
        String(45),
        nullable=True
    )

    fecha_hora = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    usuario = relationship(
        "Usuarios",
        back_populates="auditorias"
    )


# ============================================================
# 13. TECNOLOGIAS
# ============================================================

class Tecnologias(Base):
    __tablename__ = "tecnologias"

    id_tecnologia = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String(50),
        nullable=False,
        unique=True
    )

    categoria = Column(
        String(50),
        nullable=False
    )

    icono_url = Column(
        String(255),
        nullable=True
    )

    descripcion = Column(
        Text,
        nullable=True
    )

    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    proyectos = relationship(
        "ProyectosTecnologias",
        back_populates="tecnologia"
    )


# ============================================================
# 14. PROYECTOS
# ============================================================

class Proyectos(Base):
    __tablename__ = "proyectos"

    id_proyecto = Column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo = Column(
        String(100),
        nullable=False
    )

    slug = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    descripcion_corta = Column(
        Text,
        nullable=False
    )

    descripcion = Column(
        Text,
        nullable=True
    )

    problema = Column(
        Text,
        nullable=True
    )

    solucion = Column(
        Text,
        nullable=True
    )

    resultados = Column(
        Text,
        nullable=True
    )

    url_demo = Column(
        String(255),
        nullable=True
    )

    url_github = Column(
        String(255),
        nullable=True
    )

    destacado = Column(
        Boolean,
        nullable=False,
        default=False
    )

    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )

    fecha_eliminado = Column(
        DateTime(timezone=True),
        nullable=True
    )

    imagenes = relationship(
        "ProyectosImagenes",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )

    tecnologias = relationship(
        "ProyectosTecnologias",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )

    eventos = relationship(
        "Eventos",
        back_populates="proyecto"
    )


# ============================================================
# 15. IMAGENES
# ============================================================

class Imagenes(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(
        Integer,
        primary_key=True,
        index=True
    )

    url_imagen = Column(
        String(500),
        nullable=False
    )

    titulo = Column(
        String(100),
        nullable=True
    )

    alt_text = Column(
        String(255),
        nullable=True
    )

    tipo = Column(
        String(50),
        nullable=False,
        default="GALERIA"
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    proyectos = relationship(
        "ProyectosImagenes",
        back_populates="imagen",
        cascade="all, delete-orphan"
    )


# ============================================================
# 16. PROYECTOS_IMAGENES
# Relación Proyecto ↔ Imágenes
# ============================================================

class ProyectosImagenes(Base):
    __tablename__ = "proyectos_imagenes"

    id_proyecto_imagen = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_proyecto = Column(
        Integer,
        ForeignKey(
            "proyectos.id_proyecto",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    id_imagen = Column(
        Integer,
        ForeignKey(
            "imagenes.id_imagen",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    orden = Column(
        Integer,
        nullable=False,
        default=0
    )

    es_principal = Column(
        Boolean,
        nullable=False,
        default=False
    )

    proyecto = relationship(
        "Proyectos",
        back_populates="imagenes"
    )

    imagen = relationship(
        "Imagenes",
        back_populates="proyectos"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_proyecto",
            "id_imagen",
            name="uq_proyecto_imagen"
        ),
    )


# ============================================================
# 17. PROYECTOS_TECNOLOGIAS
# Relación N:M
# ============================================================

class ProyectosTecnologias(Base):
    __tablename__ = "proyectos_tecnologias"

    id_proyecto_tecnologia = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_proyecto = Column(
        Integer,
        ForeignKey(
            "proyectos.id_proyecto",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    id_tecnologia = Column(
        Integer,
        ForeignKey(
            "tecnologias.id_tecnologia",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    proyecto = relationship(
        "Proyectos",
        back_populates="tecnologias"
    )

    tecnologia = relationship(
        "Tecnologias",
        back_populates="proyectos"
    )

    __table_args__ = (
        UniqueConstraint(
            "id_proyecto",
            "id_tecnologia",
            name="uq_proyecto_tecnologia"
        ),
    )


# ============================================================
# 18. VISITANTES
# Visitantes anónimos de la aplicación
# ============================================================

class Visitantes(Base):
    __tablename__ = "visitantes"

    id_visitante = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Identificador anónimo generado por la aplicación
    identificador = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    pais = Column(
        String(100),
        nullable=True
    )

    ciudad = Column(
        String(100),
        nullable=True
    )

    region = Column(
        String(100),
        nullable=True
    )

    tipo_dispositivo = Column(
        String(100),
        nullable=True
    )

    sistema_operativo = Column(
        String(100),
        nullable=True
    )

    navegador = Column(
        String(100),
        nullable=True
    )

    idioma = Column(
        String(20),
        nullable=True
    )

    fecha_primera_visita = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_ultima_visita = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    sesiones = relationship(
        "Sesiones",
        back_populates="visitante"
    )


# ============================================================
# 19. FUENTES DE TRAFICO
# ============================================================

class FuentesTrafico(Base):
    __tablename__ = "fuentes_trafico"

    id_fuente_trafico = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fuente = Column(
        String(100),
        nullable=True
    )

    medio = Column(
        String(100),
        nullable=True
    )

    campania = Column(
        String(100),
        nullable=True
    )

    contenido = Column(
        String(100),
        nullable=True
    )

    termino = Column(
        String(100),
        nullable=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    sesiones = relationship(
        "Sesiones",
        back_populates="fuente_trafico"
    )

    __table_args__ = (
        Index(
            "idx_fuente_medio",
            "fuente",
            "medio"
        ),
    )


# ============================================================
# 20. SESIONES
# Una persona puede tener muchas sesiones
# ============================================================

class Sesiones(Base):
    __tablename__ = "sesiones"

    id_sesion = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_visitante = Column(
        Integer,
        ForeignKey("visitantes.id_visitante"),
        nullable=False,
        index=True
    )

    id_fuente_trafico = Column(
        Integer,
        ForeignKey("fuentes_trafico.id_fuente_trafico"),
        nullable=True,
        index=True
    )

    fecha_inicio = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    fecha_fin = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duracion_segundos = Column(
        Integer,
        nullable=True
    )

    paginas_visitadas = Column(
        Integer,
        nullable=False,
        default=0
    )

    pagina_entrada = Column(
        String(255),
        nullable=True
    )

    pagina_salida = Column(
        String(255),
        nullable=True
    )

    es_rebote = Column(
        Boolean,
        nullable=False,
        default=False
    )

    visitante = relationship(
        "Visitantes",
        back_populates="sesiones"
    )

    fuente_trafico = relationship(
        "FuentesTrafico",
        back_populates="sesiones"
    )

    eventos = relationship(
        "Eventos",
        back_populates="sesion",
        cascade="all, delete-orphan"
    )


# ============================================================
# 21. EVENTOS
# Analítica de comportamiento
# ============================================================

class Eventos(Base):
    __tablename__ = "eventos"

    id_evento = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_sesion = Column(
        Integer,
        ForeignKey(
            "sesiones.id_sesion",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    tipo_evento = Column(
        String(100),
        nullable=False,
        index=True
    )

    pagina = Column(
        String(255),
        nullable=True
    )

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso"),
        nullable=True,
        index=True
    )

    id_servicio = Column(
        Integer,
        ForeignKey("servicios.id_servicio"),
        nullable=True,
        index=True
    )

    id_proyecto = Column(
        Integer,
        ForeignKey("proyectos.id_proyecto"),
        nullable=True,
        index=True
    )

    datos = Column(
        JSON,
        nullable=True
    )

    fecha_hora = Column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True
    )

    sesion = relationship(
        "Sesiones",
        back_populates="eventos"
    )

    curso = relationship(
        "Cursos",
        back_populates="eventos"
    )

    servicio = relationship(
        "Servicios"
    )

    proyecto = relationship(
        "Proyectos",
        back_populates="eventos"
    )
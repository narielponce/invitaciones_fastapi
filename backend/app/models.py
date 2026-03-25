import enum
from sqlalchemy import (Column, Integer, String, Text, Date, Time, 
                        Boolean, ForeignKey, Enum, UniqueConstraint)
from sqlalchemy.orm import relationship
from .database import Base

# Usamos Enums de Python para replicar los "choices" de Django
class TipoEventoChoices(str, enum.Enum):
    quince = "15"
    boda = "boda"
    cumple = "cumple"
    otros = "otros"
    infantil = "infantil"

class GoogleFontsChoices(str, enum.Enum):
    great_vibes = "Great+Vibes"
    dancing_script = "Dancing+Script"
    allura = "Allura"
    sacramento = "Sacramento"
    parisienne = "Parisienne"

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, index=True)
    descripcion = Column(Text, nullable=True)
    preview = Column(String(255), nullable=True)
    tipo_evento = Column(Enum(TipoEventoChoices), nullable=False) # NUEVO CAMPO

    clientes = relationship("Cliente", back_populates="template")

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    
    # Relación con Template
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    template = relationship("Template", back_populates="clientes")

    nombre = Column(String(100), nullable=False)
    titulo = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    email = Column(String(100), nullable=False)
    telefono_envio_confirmacion = Column(String(30), nullable=True)
    tipo_evento = Column(Enum(TipoEventoChoices), nullable=False)
    
    # --- Datos del Evento Principal (Fiesta) ---
    fecha_evento = Column(Date, nullable=False)
    hora_evento = Column(Time, nullable=True)
    lugar_evento = Column(String(255), nullable=True)
    direccion_evento = Column(Text, nullable=True)

    # --- NUEVO: Datos de la Ceremonia ---
    fecha_ceremonia = Column(Date, nullable=True)
    hora_ceremonia = Column(Time, nullable=True)
    lugar_ceremonia = Column(String(255), nullable=True)
    direccion_ceremonia = Column(Text, nullable=True)
    
    # --- Campos de Personalización ---
    fuente_nombre = Column(Enum(GoogleFontsChoices), default=GoogleFontsChoices.great_vibes)
    mensaje_bienvenida = Column(Text, nullable=True)
    codigo_vestimenta = Column(String(100), nullable=True)
    instagram_url = Column(String(300), nullable=True)
    alias_regalos = Column(String(100), nullable=True)
    token_acceso = Column(String(40), unique=True, index=True, nullable=True)

    # --- NUEVO: Banderas de Visibilidad ---
    mostrar_ceremonia = Column(Boolean, default=False, nullable=False)
    mostrar_galeria = Column(Boolean, default=True, nullable=False)
    mostrar_dresscode = Column(Boolean, default=True, nullable=False)
    mostrar_instagram = Column(Boolean, default=True, nullable=False)
    mostrar_playlist = Column(Boolean, default=True, nullable=False)
    mostrar_regalos = Column(Boolean, default=True, nullable=False)
    
    # Campos de imagen (guardamos la ruta/URL como string)
    imagen_fondo = Column(String(255), nullable=True)
    imagen_fondo_ig = Column(String(255), nullable=True)
    imagen1 = Column(String(255), nullable=True)
    imagen2 = Column(String(255), nullable=True)
    imagen3 = Column(String(255), nullable=True)
    imagen4 = Column(String(255), nullable=True)
    imagen5 = Column(String(255), nullable=True)
    imagen6 = Column(String(255), nullable=True)
    imagen7 = Column(String(255), nullable=True)
    imagen8 = Column(String(255), nullable=True)
    imagen9 = Column(String(255), nullable=True)

    # Relaciones inversas
    confirmaciones = relationship("ConfirmacionAsistencia", back_populates="cliente", cascade="all, delete-orphan")
    canciones = relationship("CancionPlaylist", back_populates="cliente", cascade="all, delete-orphan")

class ConfirmacionAsistencia(Base):
    __tablename__ = "confirmaciones_asistencia"
    # ... (sin cambios)
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nombre_invitado = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    telefono = Column(String(30), nullable=True)
    asistencia = Column(Boolean, nullable=False)
    cantidad_acompanantes = Column(Integer, default=1)
    restricciones_alimentarias = Column(Text, nullable=True)
    cliente = relationship("Cliente", back_populates="confirmaciones")


class CancionPlaylist(Base):
    __tablename__ = "canciones_playlist"
    # ... (sin cambios)
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nombre_interprete = Column(String(100), nullable=False)
    nombre_tema = Column(String(200), nullable=False)
    cliente = relationship("Cliente", back_populates="canciones")

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, time
from .models import TipoEventoChoices, GoogleFontsChoices

# --- Template Schemas ---
class TemplateBase(BaseModel):
    nombre: str
    slug: str
    descripcion: Optional[str] = None
    preview: Optional[str] = None
    tipo_evento: TipoEventoChoices # NUEVO CAMPO
class TemplateCreate(TemplateBase): pass
class TemplateUpdate(TemplateBase): pass
class Template(TemplateBase):
    id: int
    class Config: from_attributes = True

# --- CancionPlaylist Schemas ---
class CancionPlaylistBase(BaseModel):
    nombre_interprete: str
    nombre_tema: str
class CancionPlaylistCreate(CancionPlaylistBase): pass
class CancionPlaylist(CancionPlaylistBase):
    id: int
    cliente_id: int
    class Config: from_attributes = True

# --- ConfirmacionAsistencia Schemas ---
class ConfirmacionAsistenciaBase(BaseModel):
    nombre_invitado: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    asistencia: bool
    cantidad_acompanantes: int = 1
    restricciones_alimentarias: Optional[str] = None
class ConfirmacionAsistenciaCreate(ConfirmacionAsistenciaBase): pass
class ConfirmacionAsistencia(ConfirmacionAsistenciaBase):
    id: int
    cliente_id: int
    class Config: from_attributes = True

# --- Cliente Schemas ---
class ClienteBase(BaseModel):
    nombre: str
    titulo: str
    slug: str
    email: EmailStr
    telefono_envio_confirmacion: Optional[str] = None
    tipo_evento: TipoEventoChoices
    
    # Evento Principal
    fecha_evento: date
    hora_evento: Optional[time] = None
    lugar_evento: Optional[str] = None
    direccion_evento: Optional[str] = None

    # NUEVO: Ceremonia
    fecha_ceremonia: Optional[date] = None
    hora_ceremonia: Optional[time] = None
    lugar_ceremonia: Optional[str] = None
    direccion_ceremonia: Optional[str] = None

    # Personalización
    fuente_nombre: Optional[GoogleFontsChoices] = GoogleFontsChoices.great_vibes
    mensaje_bienvenida: Optional[str] = None
    codigo_vestimenta: Optional[str] = None
    instagram_url: Optional[str] = None
    alias_regalos: Optional[str] = None

    # NUEVO: Visibilidad
    mostrar_ceremonia: bool = False
    mostrar_galeria: bool = True
    mostrar_dresscode: bool = True
    mostrar_instagram: bool = True
    mostrar_playlist: bool = True
    mostrar_regalos: bool = True
    
    # Imágenes
    imagen_fondo: Optional[str] = None
    imagen_fondo_ig: Optional[str] = None
    imagen1: Optional[str] = None
    imagen2: Optional[str] = None
    imagen3: Optional[str] = None
    imagen4: Optional[str] = None
    imagen5: Optional[str] = None
    imagen6: Optional[str] = None
    imagen7: Optional[str] = None
    imagen8: Optional[str] = None
    imagen9: Optional[str] = None

class ClienteCreate(ClienteBase):
    template_id: Optional[int] = None

class ClienteUpdate(ClienteBase):
    template_id: Optional[int] = None

class Cliente(ClienteBase):
    id: int
    template_id: Optional[int] = None
    token_acceso: Optional[str] = None
    template: Optional[Template] = None
    confirmaciones: List[ConfirmacionAsistencia] = []
    canciones: List[CancionPlaylist] = []
    class Config: from_attributes = True

class ClienteInList(ClienteBase):
    id: int
    template_id: Optional[int] = None
    token_acceso: Optional[str] = None
    template: Optional[Template] = None
    class Config: from_attributes = True

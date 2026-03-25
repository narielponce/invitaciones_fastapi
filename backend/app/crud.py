import uuid
import re
import unicodedata
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas

# --- Helpers ---
def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

# --- Template CRUD ---
async def get_template(db: AsyncSession, template_id: int):
    result = await db.execute(select(models.Template).filter(models.Template.id == template_id))
    return result.scalar_one_or_none()

async def get_template_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(models.Template).filter(models.Template.slug == slug))
    return result.scalar_one_or_none()

async def get_templates(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Template)
        .order_by(models.Template.slug)   # 👈 ordenar por slug (ascendente)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_template(db: AsyncSession, template: schemas.TemplateCreate):
    db_template = models.Template(**template.dict())
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return db_template

async def update_template(db: AsyncSession, template_id: int, template_update: schemas.TemplateUpdate):
    db_template = await get_template(db=db, template_id=template_id)
    if not db_template:
        return None
    update_data = template_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)
    await db.commit()
    await db.refresh(db_template)
    return db_template

async def delete_template(db: AsyncSession, template_id: int):
    db_template = await get_template(db=db, template_id=template_id)
    if not db_template:
        return None
    await db.delete(db_template)
    await db.commit()
    return db_template

# --- Cliente CRUD ---
async def get_cliente(db: AsyncSession, cliente_id: int):
    query = select(models.Cliente).where(models.Cliente.id == cliente_id).options(selectinload(models.Cliente.template), selectinload(models.Cliente.confirmaciones), selectinload(models.Cliente.canciones))
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_cliente_by_slug(db: AsyncSession, slug: str):
    query = select(models.Cliente).where(models.Cliente.slug == slug).options(selectinload(models.Cliente.template), selectinload(models.Cliente.confirmaciones), selectinload(models.Cliente.canciones))
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_cliente_by_event_type_and_slug(db: AsyncSession, event_type: str, slug: str):
    query = select(models.Cliente).where(
        models.Cliente.tipo_evento == event_type,
        models.Cliente.slug == slug
    ).options(
        selectinload(models.Cliente.template),
        selectinload(models.Cliente.confirmaciones),
        selectinload(models.Cliente.canciones)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_cliente_by_email_or_slug(db: AsyncSession, email: str, slug: str):
    query = select(models.Cliente).where(or_(models.Cliente.email == email, models.Cliente.slug == slug))
    result = await db.execute(query)
    return result.scalars().first()

async def get_clientes(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(models.Cliente).offset(skip).limit(limit).options(selectinload(models.Cliente.template))
    result = await db.execute(query)
    return result.scalars().all()

async def create_cliente(db: AsyncSession, cliente: schemas.ClienteCreate):
    cliente_data = cliente.dict()
    if not cliente_data.get("slug"):
        cliente_data["slug"] = slugify(cliente_data["nombre"])
    cliente_data["token_acceso"] = uuid.uuid4().hex
    db_cliente = models.Cliente(**cliente_data)
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    
    query = select(models.Cliente).where(models.Cliente.id == db_cliente.id).options(
        selectinload(models.Cliente.template)
    )
    result = await db.execute(query)
    return result.scalars().one()

async def update_cliente(db: AsyncSession, cliente_id: int, cliente_update: schemas.ClienteUpdate):
    db_cliente = await get_cliente(db=db, cliente_id=cliente_id)
    if not db_cliente:
        return None
    update_data = cliente_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

async def delete_cliente(db: AsyncSession, cliente_id: int):
    db_cliente = await get_cliente(db=db, cliente_id=cliente_id)
    if not db_cliente:
        return None
    await db.delete(db_cliente)
    await db.commit()
    return db_cliente

async def update_cliente_image_field(db: AsyncSession, cliente_id: int, field_name: str, image_path: str):
    allowed_fields = [
        'imagen_fondo', 'imagen_fondo_ig', 'imagen1', 'imagen2', 'imagen3', 
        'imagen4', 'imagen5', 'imagen6', 'imagen7', 'imagen8', 'imagen9'
    ]
    if field_name not in allowed_fields:
        return None
    db_cliente = await get_cliente(db=db, cliente_id=cliente_id)
    if db_cliente:
        setattr(db_cliente, field_name, image_path)
        await db.commit()
        await db.refresh(db_cliente)
    return db_cliente

# --- CancionPlaylist CRUD ---
async def create_cliente_cancion(db: AsyncSession, cancion: schemas.CancionPlaylistCreate, cliente_id: int):
    db_cancion = models.CancionPlaylist(**cancion.dict(), cliente_id=cliente_id)
    db.add(db_cancion)
    await db.commit()
    await db.refresh(db_cancion)
    return db_cancion

# --- ConfirmacionAsistencia CRUD ---
async def create_cliente_confirmacion(db: AsyncSession, confirmacion: schemas.ConfirmacionAsistenciaCreate, cliente_id: int):
    db_confirmacion = models.ConfirmacionAsistencia(**confirmacion.dict(), cliente_id=cliente_id)
    db.add(db_confirmacion)
    await db.commit()
    await db.refresh(db_confirmacion)
    return db_confirmacion

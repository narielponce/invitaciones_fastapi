from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Literal

from .. import crud, schemas, image_utils
from ..database import get_db

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    responses={404: {"description": "Not found"}},
)

ImageField = Literal[
    'imagen_fondo', 'imagen_fondo_ig', 'imagen1', 'imagen2', 'imagen3', 
    'imagen4', 'imagen5', 'imagen6', 'imagen7', 'imagen8', 'imagen9'
]

@router.post("/", response_model=schemas.Cliente)
async def create_cliente(cliente: schemas.ClienteCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el email o slug ya existen
    db_cliente = await crud.get_cliente_by_email_or_slug(db, email=cliente.email, slug=cliente.slug)
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email o el slug ya están en uso.")
    return await crud.create_cliente(db=db, cliente=cliente)

@router.post("/{cliente_id}/image", response_model=schemas.Cliente)
async def upload_cliente_image(
    cliente_id: int,
    file: UploadFile = File(...),
    field_name: ImageField = Query(..., description="El campo de imagen a actualizar"),
    db: AsyncSession = Depends(get_db)
):
    db_cliente = await crud.get_cliente(db, cliente_id=cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")

    try:
        image_path = image_utils.process_and_save_image(upload_file=file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {e}")

    updated_cliente = await crud.update_cliente_image_field(
        db=db, cliente_id=cliente_id, field_name=field_name, image_path=image_path
    )
    return updated_cliente

@router.get("/", response_model=List[schemas.ClienteInList])
async def read_clientes(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_clientes(db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=schemas.Cliente)
async def read_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    db_cliente = await crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente
    
@router.put("/{cliente_id}", response_model=schemas.Cliente)
async def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: AsyncSession = Depends(get_db)):
    # Opcional: También se podría verificar duplicados aquí al actualizar
    db_cliente = await crud.update_cliente(db=db, cliente_id=cliente_id, cliente_update=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.delete("/{cliente_id}", response_model=schemas.Cliente)
async def delete_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    db_cliente = await crud.delete_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@router.get("/slug/{slug}", response_model=schemas.Cliente)
async def read_cliente_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    db_cliente = await crud.get_cliente_by_slug(db, slug=slug)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

# --- Endpoints anidados (Canciones y Confirmaciones) ---
@router.post("/{cliente_id}/canciones/", response_model=schemas.CancionPlaylist)
async def create_cancion_for_cliente(
    cliente_id: int, cancion: schemas.CancionPlaylistCreate, db: AsyncSession = Depends(get_db)
):
    db_cliente = await crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return await crud.create_cliente_cancion(db=db, cancion=cancion, cliente_id=cliente_id)

@router.post("/{cliente_id}/confirmaciones/", response_model=schemas.ConfirmacionAsistencia)
async def create_confirmacion_for_cliente(
    cliente_id: int, confirmacion: schemas.ConfirmacionAsistenciaCreate, db: AsyncSession = Depends(get_db)
):
    db_cliente = await crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return await crud.create_cliente_confirmacion(db=db, confirmacion=confirmacion, cliente_id=cliente_id)

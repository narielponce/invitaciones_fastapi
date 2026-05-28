from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_db
from ..models import TipoEventoChoices

router = APIRouter(
    tags=["Invitaciones"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{event_type}/{slug}", response_model=schemas.ClientePublic)
async def read_invitacion(
    event_type: TipoEventoChoices, 
    slug: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint público para obtener los datos de una invitación específica
    por su tipo de evento y slug.
    """
    db_cliente = await crud.get_cliente_by_event_type_and_slug(db, event_type=event_type.value, slug=slug)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    return db_cliente

@router.get("/{event_type}/{slug}/panel", response_model=schemas.Cliente)
async def read_invitacion_panel(
    event_type: TipoEventoChoices, 
    slug: str, 
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint privado para obtener los datos completos (con RSVPs y canciones)
    requiriendo el token de acceso del cliente.
    """
    db_cliente = await crud.get_cliente_by_event_type_and_slug(db, event_type=event_type.value, slug=slug)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Panel no encontrado")
        
    if db_cliente.token_acceso != token:
        raise HTTPException(status_code=403, detail="Token de acceso inválido")
        
    return db_cliente

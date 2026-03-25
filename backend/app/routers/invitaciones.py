from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_db
from ..models import TipoEventoChoices

router = APIRouter(
    tags=["Invitaciones"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{event_type}/{slug}", response_model=schemas.Cliente)
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

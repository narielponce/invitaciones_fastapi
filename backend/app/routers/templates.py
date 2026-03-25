from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/templates",
    tags=["Templates"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Template)
async def create_template(template: schemas.TemplateCreate, db: AsyncSession = Depends(get_db)):
    db_template = await crud.get_template_by_slug(db, slug=template.slug)
    if db_template:
        raise HTTPException(status_code=400, detail="El slug del template ya está en uso.")
    return await crud.create_template(db=db, template=template)

@router.get("/", response_model=List[schemas.Template])
async def read_templates(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    templates = await crud.get_templates(db, skip=skip, limit=limit)
    return templates

@router.get("/{template_id}", response_model=schemas.Template)
async def read_template(template_id: int, db: AsyncSession = Depends(get_db)):
    db_template = await crud.get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.put("/{template_id}", response_model=schemas.Template)
async def update_template(template_id: int, template: schemas.TemplateUpdate, db: AsyncSession = Depends(get_db)):
    db_template = await crud.update_template(db=db, template_id=template_id, template_update=template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.delete("/{template_id}", response_model=schemas.Template)
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    db_template = await crud.delete_template(db=db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

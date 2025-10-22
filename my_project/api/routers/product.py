from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.model.helper_db import db_helpers

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("/")
async def create_product(session: Annotated[AsyncSession, Depends(db_helpers)]):
    pass


@router.get("/")
async def get_products(session: Annotated[AsyncSession, Depends(db_helpers)]):
    pass


@router.get("/{product_id}/")
async def get_product(session: Annotated[AsyncSession, Depends(db_helpers)]):
    pass


@router.patch("/{product_id}/")
async def update_product_partial(
    session: Annotated[AsyncSession, Depends(db_helpers)],
    data_product=Depends(get_product),
):
    pass


@router.put("/{product_id}/")
async def update_product(
    session: Annotated[AsyncSession, Depends(db_helpers)],
    data_product=Depends(get_product),
):
    pass


@router.delete("/{product_id}/")
async def delete_product(
    session: Annotated[AsyncSession, Depends(db_helpers)],
    data_product=Depends(get_product),
):
    await session.delete(data_product)
    await session.commit()

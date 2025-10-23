from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.crud_product import (
    create_new_product,
    get_all_product,
    get_product_by_id,
    update_product_by_id,
)
from core.model.helper_db import db_helpers
from core.schema.product_schema import CreateProduct, ReadProduct, UpdateProduct

router = APIRouter(prefix="/product", tags=["Product"])


@router.post(
    "/",
    response_model=ReadProduct,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data_product: CreateProduct,
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
) -> ReadProduct:
    return await create_new_product(
        data_product=data_product,
        session=session,
    )


@router.get(
    "/",
    response_model=list[ReadProduct],
    status_code=status.HTTP_200_OK,
)
async def get_products(
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
) -> Sequence[ReadProduct]:
    return await get_all_product(session=session)


@router.get(
    "/{product_id}/",
    response_model=ReadProduct,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID,
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
) -> ReadProduct:
    return await get_product_by_id(
        product_id=product_id,
        session=session,
    )


@router.patch(
    "/{product_id}/",
    response_model=ReadProduct,
    status_code=status.HTTP_200_OK,
)
async def update_product_partial(
    data_update: UpdateProduct,
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
    data_product=Depends(get_product),
) -> ReadProduct:
    return await update_product_by_id(
        data_update=data_update,
        data_product=data_product,
        session=session,
        partial=True,
    )


@router.put(
    "/{product_id}/",
    response_model=ReadProduct,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    data_update: UpdateProduct,
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
    data_product=Depends(get_product),
) -> ReadProduct:
    return await update_product_by_id(
        data_update=data_update,
        data_product=data_product,
        session=session,
    )


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    session: Annotated[AsyncSession, Depends(db_helpers.getter_session)],
    data_product=Depends(get_product),
) -> None:
    await session.delete(data_product)
    await session.commit()

from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import Product, Category
from core.schema.product_schema import ReadProduct, UpdateProduct


async def get_all_product(session: AsyncSession) -> Sequence[ReadProduct]:
    stmt = select(Product).options(selectinload(Product.category)).order_by(Product.id)
    result = await session.scalars(stmt)
    products = result.all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid not found",
        )
    return [ReadProduct.model_validate(product) for product in products]


async def get_product_by_id(
    product_id: UUID,
    session: AsyncSession,
) -> ReadProduct:
    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == product_id)
    )
    result = await session.scalars(stmt)
    product = result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: {product_id!r} not found",
        )
    return ReadProduct.model_validate(product)


async def update_product_by_id(
    data_update: UpdateProduct,
    data_product: Product,
    session: AsyncSession,
    partial: bool = False,
) -> ReadProduct:
    for name, value in data_update.model_dump(exclude_unset=partial).items():
        if isinstance(value, dict) and name == "category":
            category_name = value.get(name)
            stmt = select(Category).where(Category.name == category_name)
            result = await session.scalars(stmt)
            category = result.first()
            if category is None:
                category = Category(name=category_name)
                session.add(category)
                await session.flush()
            data_product.category = category
        else:
            setattr(data_product, name, value)
    await session.commit()
    await session.refresh(data_product)
    return ReadProduct.model_validate(data_product)

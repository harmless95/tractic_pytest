from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP

from core.model import IdPrKey, Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base, IdPrKey):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    create_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    products: Mapped[list[Product]] = relationship("Product", back_populates="category")

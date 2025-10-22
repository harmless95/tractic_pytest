from datetime import datetime, timezone
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DECIMAL, Numeric, ForeignKey, TIMESTAMP

from core.model import Base, IdPrKey

if TYPE_CHECKING:
    from .category import Category


class Product(Base, IdPrKey):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    price: Mapped[DECIMAL] = mapped_column(Numeric(10, 2))
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categorys.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    create_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func

class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select"
    )


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )   

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )   

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product {self.name} - ${self.price}>"

from datetime import datetime

from _decimal import Decimal
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, relationship

from src.adapters.database import Base
from src.db_models.products import Products


class Orders(Base):
    __tablename__ = "orders"

    srid: str = Column(String, primary_key=True, index=True, nullable=False)
    date: datetime = Column(DateTime)
    last_change_date: datetime = Column(DateTime)
    warehouse_name: str = Column(String)
    country_name: str = Column(String)
    oblast_okrug_name: str = Column(String)
    region_name: str = Column(String)
    nm_id: int = Column(Integer, ForeignKey(Products.nm_id), nullable=False)
    income_id: int = Column(Integer)
    is_supply: bool = Column(Boolean)
    is_realization: bool = Column(Boolean)
    total_price: Decimal = Column(Numeric(precision=10, scale=2))
    discount_percent: int = Column(Integer)
    spp: int = Column(Integer)
    finished_price: Decimal = Column(Numeric(precision=10, scale=2))
    price_with_disc: Decimal = Column(Numeric(precision=10, scale=2))
    order_type: str = Column(String)
    sticker: str = Column(String)
    g_number: str = Column(String)
    is_cancel: bool = Column(Boolean)
    cancel_date: datetime = Column(DateTime)

    sales: Mapped[list["Sales"]] = relationship(back_populates='order')


class Sales(Base):
    __tablename__ = "sales"

    sale_id: str = Column(String, primary_key=True, index=True, nullable=False)
    payment_sale_amount: int = Column(Integer)
    for_pay: Decimal = Column(Numeric(precision=10, scale=2))
    srid: str = Column(String, ForeignKey(Orders.srid), nullable=False)

    order: Mapped["Orders"] = relationship(back_populates='sales')

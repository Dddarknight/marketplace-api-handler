from datetime import date, datetime

from sqlalchemy import Column, Boolean, String, Integer, Date, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from src.adapters.database import Base


class Products(Base):
    __tablename__ = "products"

    supplier_article: int = Column(Integer)
    nm_id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    barcode: str = Column(String)
    category: str = Column(String)
    subject: str = Column(String)
    brand: str = Column(String)
    tech_size: str = Column(String)

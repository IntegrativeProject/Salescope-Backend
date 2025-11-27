from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, Boolean, ForeignKey, text
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP, server_default=text("NOW()"))
    deleted_at = Column(TIMESTAMP, nullable=True)
    deleted_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)

from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(20), nullable=False)
    total_amount = Column(Numeric(10, 2), server_default="0")

    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP, server_default=text("NOW()"))

    user = relationship("User")
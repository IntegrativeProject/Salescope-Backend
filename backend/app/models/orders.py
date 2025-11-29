from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP, Boolean, text
from sqlalchemy.orm import relationship
from ..database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(20), nullable=False)
    total_amount = Column(Numeric(10, 2), server_default="0")

    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP, server_default=text("NOW()"))
    is_active = Column(Boolean, server_default=text("TRUE"), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    deleted_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
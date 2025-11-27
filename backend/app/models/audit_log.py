from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, ForeignKey, text
from sqlalchemy.orm import relationship

from ..database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    actor_username = Column(Text, nullable=False)
    full_name = Column(String(150), nullable=False)

    action_timestamp = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))
    details = Column(Text)

    user = relationship("User")

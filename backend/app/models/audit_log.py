from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text

from ..database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    actor_id = Column(Integer, nullable=True)
    actor_name = Column(String(150), nullable=True)

    action_timestamp = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))
    old_data = Column(Text)
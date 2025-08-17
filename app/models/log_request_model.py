from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base

class LogRequest(Base):
    __tablename__ = "log_requests"
    id = Column(Integer, primary_key=True, index=True)
    entry_date = Column(DateTime, default=datetime.now(), index=True)
    method = Column(VARCHAR)
    response_body = Column(JSONB)
    file_hash = Column(VARCHAR)
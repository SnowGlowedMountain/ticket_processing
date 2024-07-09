from sqlalchemy import Column, String, Text, DateTime, Float
from datetime import datetime
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    customer_email = Column(String, index=True)
    status = Column(String, index=True)
    category = Column(String, index=True, nullable=True)
    priority = Column(String, index=True, nullable=True)
    initial_response = Column(Text, nullable=True)
    category_confidence = Column(Float, nullable=True)
    priority_confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

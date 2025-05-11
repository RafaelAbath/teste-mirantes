from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sale(Base):
    __tablename__ = "sales"
    id           = Column(Integer, primary_key=True, index=True)
    product      = Column(String,  index=True)
    quantity     = Column(Integer, nullable=False)
    unit_price   = Column(Numeric(10, 2), nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String,FLOAT
from database import Base

# Define Address class inheriting from Base

class Address(Base):
    __tablename__ = 'Address'
    id = Column(Integer, primary_key=True)
    adr = Column(String(256))
    lat = Column(FLOAT())
    lon = Column(FLOAT())

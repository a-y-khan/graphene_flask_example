#from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from database import Base


class House(Base):
	__tablename__ = 'house'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	location = Column(String)
	founder = Column(String)
	colors = Column(String)
	ghost = Column(String)

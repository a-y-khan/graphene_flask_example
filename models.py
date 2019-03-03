from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import backref, relationship

from database import Base


class House(Base):
	__tablename__ = 'house'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	location = Column(String)
	founder = Column(String)
	colors = Column(String)
	crest = Column(String)
	ghost = Column(String)


class Student(Base):
	__tablename__ = 'student'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	wand_wood = Column(String)
	wand_core = Column(String)
	wand_length = Column(Float)
	wand_length_unit = Column(String)
	house_id = Column(Integer, ForeignKey('house.id'))
	house = relationship(
		House,
		backref=backref('houses', uselist=True, cascade='delete,all')
	)


class Pet(Base):
	__tablename__ = 'pet'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	species = Column(String)
	student_id = Column(Integer, ForeignKey('student.id'))
	student = relationship(
		Student,
		backref=backref('students', uselist=True, cascade='delete,all')
	)
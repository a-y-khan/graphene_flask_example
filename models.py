from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import backref, relationship

from database import Base


class House(Base):
	__tablename__ = 'house'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	location = Column(String, doc="Location on Hogwarts campus.")
	founder = Column(String, doc="Hogwarts house founder.")
	colors = Column(String, doc="Each Hogwarts house has two colors.")
	crest = Column(String, doc="Hogwarts house crest.")
	ghost = Column(String, doc="Each Hogwarts house has a resident ghost.")


## TODO: create Wand table?

class Student(Base):
	__tablename__ = 'student'
	id = Column(Integer, primary_key=True)
	name = Column(String, doc="Hogwarts student name. Typically first name, surname.")
	wand_wood = Column(String, doc="Hogwarts student's wand material.")
	wand_core = Column(String, doc="Hogwarts student's wand core.")
	wand_length = Column(Float, doc="Length of student's wand.")
	wand_length_unit = Column(String, doc="Measurement unit used for wand length.")
	house_id = Column(Integer, ForeignKey('house.id'))
	house = relationship(
		House,
		backref=backref('houses', uselist=True, cascade='delete,all')
	)


class Pet(Base):
	__tablename__ = 'pet'
	id = Column(Integer, primary_key=True)
	name = Column(String, doc="Pet name.")
	species = Column(String, doc="Pet species.")
	student_id = Column(Integer, ForeignKey('student.id'))
	student = relationship(
		Student,
		backref=backref('students', uselist=True, cascade='delete,all')
	)
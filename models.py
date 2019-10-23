import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from database import Base as db_Base
import database as db

class House(db_Base):
	__tablename__ = 'house'
	id = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.String, doc="TODO")
	location = sa.Column(sa.String, doc="Location on Hogwarts campus.")
	founder = sa.Column(sa.String, doc="Hogwarts house founder.")
	colors = sa.Column(sa.String, doc="Each Hogwarts house has two colors.")
	crest = sa.Column(sa.String, doc="Hogwarts house crest.")
	ghost = sa.Column(sa.String, doc="Each Hogwarts house has a resident ghost.")

class Student(db_Base):
	__tablename__ = 'student'
	id = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.String, doc="Hogwarts student name. Typically first name, surname.")
	wand_wood = sa.Column(sa.String, doc="Hogwarts student's wand material.")
	wand_core = sa.Column(sa.String, doc="Hogwarts student's wand core.")
	wand_length = sa.Column(sa.Float, doc="Length of student's wand.")
	wand_length_unit = sa.Column(sa.String, doc="Measurement unit used for wand length.", default="inch")
	house_id = sa.Column(sa.Integer, sa.ForeignKey("house.id"))
	# house = sa_orm.relationship(
	# 	House,
	# 	backref=sa_orm.backref('houses', uselist=True, cascade="delete,all"))
	house = sa_orm.relationship(House)

class Staff(db_Base):
	__tablename__ = 'staff'
	id = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.String, doc="Hogwarts staff member name. "
	                                "Typically first name, surname.")
	position = sa.Column(sa.String, doc="TODO")
	specialization = sa.Column(sa.String, doc="TODO")
	wand_wood = sa.Column(sa.String, doc="Hogwarts staff member's wand material.")
	wand_core = sa.Column(sa.String, doc="Hogwarts staff member's wand core.")
	wand_length = sa.Column(sa.Float, doc="Length of staff member's wand.")
	wand_length_unit = sa.Column(sa.String,
	                             doc="Measurement unit used for wand length. "
	                                 "Default is inches", default="inch")
	house_id = sa.Column(sa.Integer, sa.ForeignKey("house.id"))
	house = sa_orm.relationship(House)

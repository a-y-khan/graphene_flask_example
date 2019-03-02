from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import json

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import House, Student, Pet
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)

	# create the fixtures

	# houses
	with open('raw_data/houses.json', 'rt') as file:
		houses = json.load(file)
		for house in houses:
			db_session.add(
				House(name=house['name'], location=house['location'], founder=house['founder'],
					  colors=house['colors'], crest=house['crest'], ghost=house['ghost'])
			)

	with open('raw_data/students.json') as file:
		students = json.load(file)
		for student in students:
			db_session.add(
				Student(name=student['name'], house=student['house'],
					    wand_wood=student['wand_wood'], wand_core=student['wand_core'],
					    wand_length=student['wand_length'], wand_length_unit=student['wand_length_unit'])
			)

	with open('raw_data/pets.json') as file:
		pets = json.load(file)
		for pet in pets:
			db_session.add(
				Pet(name=pet['name'], species=pet['species'], student=pet['student'])
			)

	db_session.commit()
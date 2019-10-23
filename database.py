import sqlalchemy as sa
import sqlalchemy.ext.declarative as sa_decl
import sqlalchemy.orm as sa_orm

import json

engine = sa.create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = sa_orm.scoped_session(
	sa_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = sa_decl.declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import House, Student, Staff
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)

	# create the fixtures
	houses_map = dict()

	with open('raw_data/houses.json', 'rt') as file:
		houses = json.load(file)
		for house in houses:
			houses_map[house['name']] = House(name=house['name'],
				                              location=house['location'],
				                              founder=house['founder'],
					                          colors=house['colors'],
					                          crest=house['crest'],
					                          ghost=house['ghost'])
			db_session.add(houses_map[house['name']])

	with open('raw_data/students.json', 'rt') as file:
		students = json.load(file)
		for student in students:
			student_model = Student(name=student['name'],
					  		 		house=houses_map[student['house']],
					 		  		wand_wood=student['wand_wood'],
							  		wand_core=student['wand_core'],
							  		wand_length=float(student['wand_length']))
			db_session.add(student_model)

	with open('raw_data/hogwarts_staff.json', 'rt') as file:
		staff = json.load(file)
		for staff_member in staff:
			staff_model = Staff(name=staff_member['name'],
				                position=staff_member['position'],
				                specialization=staff_member['specialization'],
				                house=houses_map.get(staff_member.get('house')),
					 		  	wand_wood=student['wand_wood'],
							  	wand_core=student['wand_core'],
							  	wand_length=float(student['wand_length']))
			db_session.add(staff_model)
	
	db_session.commit()

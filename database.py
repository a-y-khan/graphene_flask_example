from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import json

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import House
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)

	# create the fixtures

	# houses
	with open('raw_data/houses.json', 'rt') as file:
		houses = json.load(file)
		for house in houses:
			db_session.add(
				House(name=house['name'], location=house['location'], founder=house['founder'],
					  colors=house['colors'], ghost=house['ghost'])
			)


	db_session.commit()
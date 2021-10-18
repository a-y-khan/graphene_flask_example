from sqlalchemy import inspect as sa_inspect
from sqlalchemy import func as sa_func

from example.database import load_from_raw
from example.models import db_Base, House, Student, Staff


def test_table_names(session):
    inspector = sa_inspect(session.get_bind())
    assert len(set(inspector.get_table_names()).difference(["house", "staff", "student"])) == 0


def test_house_data(session):
    house_models, student_models, staff_models = load_from_raw()
    for model in house_models + student_models + staff_models:
        session.add(model)
    session.commit()

    result = session.query(sa_func.count(Staff.position),
                           House.name).join(House).filter(Staff.position == "Professor").group_by(House.name).all()
    # each house must have at least one professor
    for row in result:
        assert row[0] > 0

    result = session.query(sa_func.count(Student.id), House.name).join(House).group_by(House.name).all()
    # each house must have at least one student
    for row in result:
        assert row[0] > 0

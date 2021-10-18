import pytest
import sqlalchemy as sa
import sqlalchemy.ext.declarative as sa_decl
import sqlalchemy.orm as sa_orm

from example.models import db_Base

# in-memory db for testing
test_db_url = "sqlite://"


@pytest.fixture(scope="function")
def session_factory():
    engine = sa.create_engine(test_db_url)
    db_Base.metadata.create_all(engine)

    yield sa_orm.sessionmaker(bind=engine)

    engine.dispose()


@pytest.fixture(scope="function")
def session(session_factory):
    return sa_orm.scoped_session(session_factory)

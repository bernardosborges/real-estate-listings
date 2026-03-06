# ruff: noqa: E402
from tests.settings import apply_test_settings

apply_test_settings()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.api.deps.oauth2 import get_current_user
from app.infrastructure.db.mappers.user_mapper import UserMapper
from app.infrastructure.db.mappers.user_profile_mapper import UserProfileMapper

from tests.factories.address_factory import address_factory
from tests.factories.property_factory import property_factory
from tests.factories.user_factory import user_factory
from tests.factories.user_profile_factory import user_profile_factory
from tests.unit.application.fakes.fake_unit_of_work import FakeUnitOfWork

# -----------------------------------------------
# DB SETTINGS (SQLITE)
# -----------------------------------------------

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -----------------------------------------------
# FACTORY FIXTURES
# -----------------------------------------------

# ---------------------- ENTITIES ----------------------


@pytest.fixture
def address_factory_fixture():
    return address_factory()


@pytest.fixture
def property_factory_fixture():
    return property_factory()


@pytest.fixture
def user_factory_fixture():
    return user_factory()


@pytest.fixture
def user_profile_factory_fixture():
    return user_profile_factory()


# -----------------------------------------------
# TEST ENVIRONMENTS
# -----------------------------------------------

# ---------------------- FIXTURES ----------------------


@pytest.fixture
def test_env_guest(db_session):
    # yield data back to test
    yield {"db": db_session}


@pytest.fixture
def test_env_logged(db_session):
    # create user and its profile in the db
    user = create_test_user(db_session)
    profile = create_test_user_profile(db_session, user)

    # saves original and overrides
    original_override = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: user

    # yield data back to test
    yield {"db": db_session, "user": user, "profile": profile}

    # recover original
    if original_override:
        app.dependency_overrides[get_current_user] = original_override
    else:
        app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def test_env_admin(db_session):
    # create user and its profile in the db
    user = create_test_admin(db_session)
    profile = create_test_user_profile(db_session, user)

    # saves original and overrides
    original_override = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: user

    # yield data back to test
    yield {"db": db_session, "user": user, "profile": profile}

    # recover original
    if original_override:
        app.dependency_overrides[get_current_user] = original_override
    else:
        app.dependency_overrides.pop(get_current_user, None)


# ---------------------- CREATE TEST USER ----------------------


def create_test_user(db, **overrides):
    user = user_factory(id=None)(**overrides)
    model = UserMapper.to_model(user)
    db.add(model)
    db.commit()
    db.refresh(model)
    user.id = model.id
    return user


def create_test_admin(db, **overrides):
    user = user_factory(is_superuser=True)(**overrides)
    model = UserMapper.to_model(user)
    db.add(model)
    db.commit()
    db.refresh(model)
    user.id = model.id
    return user


def create_test_user_profile(db, user, **overrides):
    profile = user_profile_factory(id=None, user_id=user.id)(**overrides)
    model = UserProfileMapper.to_model(profile)
    db.add(model)
    db.commit()
    db.refresh(model)
    profile.id = model.id
    return profile


# ---------------------- UNIT OF WORK ----------------------


@pytest.fixture
def fake_uow():
    uow = FakeUnitOfWork()
    yield uow


# ---------------------- DATABASE ----------------------


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def override_get_db(db_session):
    """Override for integration tests."""
    original_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = lambda: db_session

    yield db_session

    if original_override:
        app.dependency_overrides[get_db] = original_override
    else:
        app.dependency_overrides.pop(get_db, None)


#     session = TestSessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()

# app.dependency_overrides[get_db] = override_get_db


# ---------------------- FAST API CLIENT ----------------------


@pytest.fixture
def client(override_get_db):
    return TestClient(app)

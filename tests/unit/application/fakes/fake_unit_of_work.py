from app.application.unit_of_work.unit_of_work import UnitOfWork
from tests.unit.application.fakes.fake_user_repository import FakeUserRepository
from tests.unit.application.fakes.fake_user_profile_repository import FakeUserProfileRepository
from tests.unit.application.fakes.fake_property_repository import FakePropertyRepository
from tests.unit.application.fakes.fake_address_repository import FakeAddressRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.user_repository = FakeUserRepository()
        self.profile_repository = FakeUserProfileRepository()
        self.property_repository = FakePropertyRepository()
        self.address_repository = FakeAddressRepository()
        self.committed = False
        self.flushed = False
        self.rolledback = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolledback = True

    def flush(self):
        self.flushed = True

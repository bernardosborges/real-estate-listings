from app.domain.entities.user import User
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.domain.exceptions.property_exceptions import PropertyNotFound, PropertyForbidden

class DeactivatePropertyUseCase:

    """
    Use case responsible for deactivating a Property.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(self, property_public_id: str, current_user: User) -> None:

        # Check property
        db_property = self.uow.property_repository.get_by_public_id(property_public_id)
        if not db_property:
            raise PropertyNotFound()

        # Check profile
        db_profile = self.uow.profile_repository.get_by_user_id(current_user.id)
        if not db_profile:
            raise UserProfileNotFound(property_public_id)

        # Check ownership
        if db_property.profile_id != db_profile.id:
            raise PropertyForbidden()

        # Update status
        db_property.deactivate()

        # Deactivate and persist all changes
        self.uow.property_repository.deactivate(db_property.id)
        self.uow.commit()

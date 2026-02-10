from app.domain.entities.user import User
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.domain.exceptions.user_profile_exceptions import UserProfileNotFound
from app.domain.exceptions.property_exceptions import PropertyNotFound, PropertyForbidden

class RestorePropertyUseCase:

    """
    Use case responsible for restoring a soft deleted Property.
    """

    def __init__(
            self,
            uow: UnitOfWork
        ):

        self.uow = uow


    def execute(self, property_public_id: str, current_user: User) -> None:

        # Check property
        db_property = self.uow.property_repository.get_deleted_by_public_id(property_public_id)
        if not db_property:
            raise PropertyNotFound()

        # Check profile
        db_profile = self.uow.profile_repository.get_by_user_id(current_user.id)
        if not db_profile:
            raise UserProfileNotFound()
        
        # Check ownership
        if db_property.profile_id != db_profile.id:
            raise PropertyForbidden()
        
        # Check restore
        db_property.restore()
        
        # Restore and persist all changes
        self.uow.property_repository.restore(db_property.id)
        self.uow.commit()
from fastapi import Depends

from app.api.deps.uow_deps import get_uow
from app.application.unit_of_work.unit_of_work import UnitOfWork
from app.application.usecases.property.create_property import CreatePropertyUseCase
from app.application.usecases.property.list_properties_by_profile import ListPropertiesByProfileUseCase
from app.application.usecases.property.list_properties_for_map import ListPropertiesForMapUseCase
from app.application.usecases.property.update_property import UpdatePropertyUseCase
from app.application.usecases.property.deactivate_property import DeactivatePropertyUseCase
from app.application.usecases.property.activate_property import ActivatePropertyUseCase
from app.application.usecases.property.soft_delete_property import SoftDeletePropertyUseCase
from app.application.usecases.property.restore_property import RestorePropertyUseCase


def get_create_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> CreatePropertyUseCase:
    return CreatePropertyUseCase(uow = uow)

def get_list_properties_by_profile_usecase(uow: UnitOfWork = Depends(get_uow)) -> ListPropertiesByProfileUseCase:
    return ListPropertiesByProfileUseCase(uow = uow)

def get_list_properties_for_map_usecase(uow: UnitOfWork = Depends(get_uow)) -> ListPropertiesForMapUseCase:
    return ListPropertiesForMapUseCase(uow = uow)

def get_update_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> UpdatePropertyUseCase:
    return UpdatePropertyUseCase(uow = uow)

def get_deactivate_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> DeactivatePropertyUseCase:
    return DeactivatePropertyUseCase(uow = uow)

def get_activate_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> ActivatePropertyUseCase:
    return ActivatePropertyUseCase(uow = uow)

def get_restore_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> RestorePropertyUseCase:
    return RestorePropertyUseCase(uow = uow)

def get_soft_delete_property_usecase(uow: UnitOfWork = Depends(get_uow)) -> SoftDeletePropertyUseCase:
    return SoftDeletePropertyUseCase(uow = uow)




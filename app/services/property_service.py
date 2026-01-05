from app.repositories.property_repository import (
    create_property_repository,
    list_properties_repository
)

def create_property_service(data):
    create_property_repository(data)

def list_properties_service(filters):
    return list_properties_repository(filters)
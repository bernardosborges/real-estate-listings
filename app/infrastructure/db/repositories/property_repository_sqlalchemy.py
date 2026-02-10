from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import select, exists, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.entities.property import Property
from app.domain.repositories.property_repository import PropertyRepository
from app.domain.value_objects.property.property_public_id import PropertyPublicId
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.value_objects.address.latitude import Latitude
from app.domain.value_objects.address.longitude import Longitude
from app.infrastructure.db.models.property_model import PropertyModel
from app.infrastructure.db.models.address_model import AddressModel
from app.infrastructure.db.models.user_profile_model import UserProfileModel
from app.infrastructure.db.mappers.property_mapper import PropertyMapper
from app.domain.exceptions.property_exceptions import PropertyNotFound


class PropertyRepositorySQLAlchemy(PropertyRepository):

# -----------------------------------------------
# INIT
# -----------------------------------------------

    def __init__(self, db: Session):
        self.db = db


# -----------------------------------------------
# METHODS
# -----------------------------------------------
    def refresh(self, property: Property) -> Property:
        model = self.db.get(PropertyModel, property.id)
        if not model or model.deleted_at:
            return None
        
        self.db.refresh(model)
        refreshed_property = PropertyMapper.to_entity(model)

        return PropertyMapper.update_entity(property, refreshed_property)


    def save(self, property: Property) -> None:
        if property.id is None:
            model = PropertyMapper.to_model(property)
            self.db.add(model)
            self.db.flush()
            property.id = model.id
        else:
            model = self.db.get(PropertyModel, property.id)
            if not model or model.deleted_at is not None:
                raise PropertyNotFound(f"Property not found or deleted: public id {property.public_id}.")
            PropertyMapper.update_model(model, property)

        # try:
        #     self.db.flush()
        # except IntegrityError as exc:
        #     self.db.rollback()
        #     raise exc

        # return PropertyMapper.to_entity(model)


    def get_by_id(self, id: int) -> Property | None:
        stmt = (
            select(PropertyModel)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_(None),
            )
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        return PropertyMapper.to_entity(result) if result else None


    def get_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        stmt = (
            select(PropertyModel)
            .where(
                PropertyModel.public_id == str(public_id),
                PropertyModel.deleted_at.is_(None),
            )
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        return PropertyMapper.to_entity(result) if result else None


    def get_deleted_by_public_id(self, public_id: PropertyPublicId) -> Property | None:
        stmt = (
            select(PropertyModel)
            .where(
                PropertyModel.public_id == str(public_id),
                PropertyModel.deleted_at.is_not(None),
            )
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        return PropertyMapper.to_entity(result) if result else None


    # def get_by_profile_public_id(self, public_id: UserProfilePublicId) -> Property | None:
    #     stmt = (
    #         select(PropertyModel)
    #         .join(UserProfileModel, PropertyModel.profile_id == UserProfileModel.id)
    #         .where(
    #             UserProfileModel.public_id == str(public_id),
    #             UserProfileModel.deleted_at.is_(None),
    #             PropertyModel.deleted_at.is_(None)
    #         )
    #     )

    #     result = self.db.execute(stmt).scalar_one_or_none()

    #     return PropertyMapper.to_entity(result) if result else None

    def list_by_profile_id(self, profile_id: int, limit: int, offset: int, include_inactive: bool = False, price_min: Decimal | None = None, price_max: Decimal | None = None) -> list[Property]:
        stmt = (
            select(PropertyModel)
            .where(
                PropertyModel.profile_id == profile_id,
                PropertyModel.deleted_at.is_(None),
            )
        )

        if not include_inactive:
            stmt = stmt.where(PropertyModel.is_active == True)
        if price_min is not None:
            stmt = stmt.where(PropertyModel.price >= price_min)
        if price_max is not None:
            stmt = stmt.where(PropertyModel.price <= price_max)

        stmt = (
            stmt
            .order_by(PropertyModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = self.db.execute(stmt).scalars().all()
        return [PropertyMapper.to_entity(model) for model in result]
    

    def list_for_map(
            self,
            lat_north: Latitude,
            lat_south: Latitude,
            lng_east: Longitude,
            lng_west: Longitude,
            limit: int,
            offset: int,
            include_inactive: bool = False,
            profile_id: int | None = None,
            price_min: Decimal | None = None,
            price_max: Decimal | None = None
        ) -> list[Property]:

        stmt = (
            select(PropertyModel)
            .join(AddressModel, PropertyModel.address_id == AddressModel.id)
            .where(
                PropertyModel.deleted_at.is_(None),
                AddressModel.latitude <= lat_north.value,
                AddressModel.latitude >= lat_south.value,
                AddressModel.longitude <= lng_east.value,
                AddressModel.longitude >= lng_west.value
            )
        )

        if profile_id is not None:
            stmt = stmt.where(PropertyModel.profile_id == profile_id)
        if not include_inactive:
            stmt = stmt.where(PropertyModel.is_active == True)
        if price_min is not None:
            stmt = stmt.where(PropertyModel.price >= price_min)
        if price_max is not None:
            stmt = stmt.where(PropertyModel.price <= price_max)

        stmt = (
            stmt
            .order_by(PropertyModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = self.db.execute(stmt).scalars().all()
        return [PropertyMapper.to_entity(model) for model in result]
    

    def exists_by_public_id(self, public_id: PropertyPublicId) -> bool:
        stmt = select(
            exists().where(PropertyModel.public_id == str(public_id))
        )
        return self.db.execute(stmt).scalar()


    def deactivate(self, id: int) -> None:
        stmt = (
            update(PropertyModel)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_(None)
            )
            .values(
                updated_at = datetime.now(timezone.utc),
                is_active = False
            )
        )
        self.db.execute(stmt)


    def activate(self, id: int) -> None:
        stmt = (
            update(PropertyModel)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_(None)
            )
            .values(
                updated_at = datetime.now(timezone.utc),
                is_active = True
            )
        )
        self.db.execute(stmt)


    def restore(self, id: int) -> None:
        stmt = (
            update(PropertyModel)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_not(None)
            )
            .values(
                deleted_at = None,
                updated_at = datetime.now(timezone.utc),
                is_active = True
            )
        )
        self.db.execute(stmt)   

    def soft_delete(self, id: int) -> None:
        stmt = (
            update(PropertyModel)
            .where(
                PropertyModel.id == id,
                PropertyModel.deleted_at.is_(None)
            )
            .values(
                deleted_at = datetime.now(timezone.utc),
                is_active = False
            )
        )
        self.db.execute(stmt)


# class PropertyRepository:

    # # -----------------------------------------------
    # # CRUD - CREATE
    # # -----------------------------------------------

    # @staticmethod
    # def create(db: Session, description: str, price: Decimal, private_area: Decimal, user_id: int, address_id: int):
    #     #data = schema.model_dump() # exclude={"tags_ids"}
    #     #db_property = PropertyModel(**data, user_id=user_id)
    #     db_property = PropertyModel(
    #         description=description,
    #         price=price,
    #         private_area=private_area,
    #         user_id=user_id,
    #         address_id=address_id
    #     )
    #     db.add(db_property)
    #     db.flush()
    #     return db_property


    # # -----------------------------------------------
    # # CRUD - READ
    # # -----------------------------------------------

    # @staticmethod
    # def get_by_id(db: Session, id: int, is_active: bool | None = True, include_deleted: bool = False) -> PropertyModel | None:
    #     query = db.query(PropertyModel).filter(PropertyModel.id == id)
        
    #     if is_active is not None:
    #         query = query.filter(PropertyModel.is_active == is_active)
        
    #     if not include_deleted:
    #         query = query.filter(PropertyModel.deleted_at.is_(None))

    #     return query.first()
    
    # @staticmethod
    # def get_by_public_id(db: Session, public_id: str, is_active: bool | None = True, include_deleted: bool = False) -> PropertyModel | None:
    #     query = db.query(PropertyModel).filter(PropertyModel.public_id == public_id)
        
    #     if is_active is not None:
    #         query = query.filter(PropertyModel.is_active == is_active)
        
    #     if not include_deleted:
    #         query = query.filter(PropertyModel.deleted_at.is_(None))

    #     return query.first()
    
    # @staticmethod
    # def get_with_details_by_public_id(db: Session, public_id: str, is_editing: bool = False) -> PropertyModel | None:
    #     photo_relation = (PropertyModel.photos_all if is_editing else PropertyModel.photos)
    #     query = (
    #         db.query(PropertyModel)
    #         .options(
    #             selectinload(PropertyModel.property_tags)
    #                 .selectinload(PropertyTagModel.tag), 
    #             selectinload(photo_relation),
    #         )
    #         .filter(PropertyModel.public_id == public_id)
    #     )

    #     if not is_editing:
    #         query = query.filter(PropertyModel.is_active.is_(True))
        
    #     return query.first()

    # @staticmethod
    # def list_all(
    #         db: Session,
    #         price_min: Decimal | None = None,
    #         price_max: Decimal | None = None,
    #         limit: int = 20,
    #         offset: int = 0,
    #         is_active: bool | None  = True,
    #         include_deleted: bool = False
    # ) -> List[PropertyModel]:
    #     query = db.query(PropertyModel)

    #     if is_active is not None:
    #         query = query.filter(PropertyModel.is_active == is_active)

    #     if not include_deleted:
    #             query = query.filter(PropertyModel.deleted_at.is_(None))

    #     if price_min is not None:
    #         query = query.filter(PropertyModel.price >= price_min)
        
    #     if price_max is not None:
    #         query = query.filter(PropertyModel.price <= price_max)

    #     return query.offset(offset).limit(limit).all()

    # @staticmethod
    # def list_by_user_id(
    #         db: Session,
    #         user_id: int,
    #         price_min: Decimal | None = None,
    #         price_max: Decimal | None = None,
    #         limit: int = 20,
    #         offset: int = 0,
    #         is_active: bool | None  = True,
    #         include_deleted: bool = False
    # ) -> List[PropertyModel]:
    #     query = db.query(PropertyModel).filter(PropertyModel.user_id == user_id)

    #     if is_active is not None:
    #         query = query.filter(PropertyModel.is_active == is_active)

    #     if not include_deleted:
    #             query = query.filter(PropertyModel.deleted_at.is_(None))
        
    #     if price_min is not None:
    #         query = query.filter(PropertyModel.price >= price_min)
        
    #     if price_max is not None:
    #         query = query.filter(PropertyModel.price <= price_max)

    #     return query.offset(offset).limit(limit).all()

    # @staticmethod
    # def list_in_rectangle(
    #         db: Session,
    #         min_lat: float,
    #         max_lat: float,
    #         min_lng: float,
    #         max_lng: float,
    #         price_min: Decimal | None = None,
    #         price_max: Decimal | None = None,
    #         limit: int = 50,
    #         offset: int = 0,
    #         is_active: bool | None  = True,
    #         include_deleted: bool = False
    # ) -> List[PropertyModel]:
    #     query = db.query(PropertyModel).join(
    #         AddressModel, 
    #         PropertyModel.address_id == AddressModel.id).filter(
    #         AddressModel.latitude.between(min_lat, max_lat),
    #         AddressModel.longitude.between(min_lng, max_lng)
    #     )

    #     if is_active is not None:
    #         query = query.filter(PropertyModel.is_active == is_active)

    #     if not include_deleted:
    #         query = query.filter(PropertyModel.deleted_at.is_(None))

    #     if price_min is not None:
    #         query = query.filter(PropertyModel.price >= price_min)
        
    #     if price_max is not None:
    #         query = query.filter(PropertyModel.price <= price_max)

    #     return query.offset(offset).limit(limit).all()


    # # -----------------------------------------------
    # # CRUD - UPDATE
    # # -----------------------------------------------

    # @staticmethod
    # def update(db: Session, id: int, **kwargs) -> PropertyModel | None:
    #     db_property = PropertyRepository.get_by_id(db, id)
    #     if not db_property:
    #         return None

    #     for key, value in kwargs.items():
    #         setattr(db_property, key, value)
    #     return db_property

    # @staticmethod
    # def restore(db: Session, id: int) -> PropertyModel | None:
    #     db_property = PropertyRepository.get_by_id(db, id, include_deleted=True)
    #     if not db_property:
    #         return None

    #     db_property.deleted_at = None

    #     return db_property


    # # -----------------------------------------------
    # # CRUD - DELETE
    # # -----------------------------------------------
    
    # @staticmethod
    # def soft_delete(db: Session, id: int) -> PropertyModel | None:
    #     return PropertyRepository._delete(db, id, hard=False)
    
    # @staticmethod
    # def hard_delete(db: Session, id: int) -> PropertyModel | None:
    #     return PropertyRepository._delete(db, id, hard=True)

    # @staticmethod
    # def _delete(db: Session, id: int, hard: bool = False) -> PropertyModel | None:
    #     db_property = PropertyRepository.get_by_id(db, id)
    #     if not db_property:
    #         return None
        
    #     if hard:
    #         db.delete(db_property)
    #     else:
    #         db_property.deleted_at = datetime.now(timezone.utc)
    #         db_property.is_active = False

    #     return db_property
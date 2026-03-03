from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.domain.constants.address_constants import (
    ADDRESS_ZIPCODE_LENGTH,
    ADDRESS_COUNTRY_MAX_LENGTH,
    ADDRESS_STATE_MAX_LENGTH,
    ADDRESS_CITY_MAX_LENGTH,
    ADDRESS_NEIGHBORHOOD_MAX_LENGTH,
    ADDRESS_STREET_MAX_LENGTH,
    ADDRESS_NUMBER_MAX_LENGTH,
    ADDRESS_COMPLEMENT_MAX_LENGTH,
)


class AddressModel(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)

    zip_code = Column(String(ADDRESS_ZIPCODE_LENGTH), nullable=False, index=True)
    country = Column(String(ADDRESS_COUNTRY_MAX_LENGTH), nullable=False, default="BR")
    state = Column(String(ADDRESS_STATE_MAX_LENGTH), nullable=False)
    city = Column(String(ADDRESS_CITY_MAX_LENGTH), nullable=False)
    neighborhood = Column(String(ADDRESS_NEIGHBORHOOD_MAX_LENGTH), nullable=False)
    street = Column(String(ADDRESS_STREET_MAX_LENGTH), nullable=False)
    number = Column(String(ADDRESS_NUMBER_MAX_LENGTH), nullable=False)
    complement = Column(String(ADDRESS_COMPLEMENT_MAX_LENGTH), nullable=True)

    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    properties = relationship("PropertyModel", back_populates="address")

    __table_args__ = (
        UniqueConstraint(
            "zip_code",
            "state",
            "city",
            "neighborhood",
            "street",
            "number",
            "complement",
            name="uq_address_unique_location",
        ),
        CheckConstraint("latitude BETWEEN -90 AND 90"),
        CheckConstraint("longitude BETWEEN -180 AND 180"),
        Index("ix_address_geo", "latitude", "longitude"),
    )

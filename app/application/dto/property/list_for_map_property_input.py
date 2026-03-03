from decimal import Decimal


class ListForMapPropertyInput:

    def __init__(
        self,
        lat_north: Decimal,
        lat_south: Decimal,
        lng_east: Decimal,
        lng_west: Decimal,
        profile_public_id: str | None = None
    ):

        self.lat_north = lat_north
        self.lat_south = lat_south
        self.lng_east = lng_east
        self.lng_west = lng_west
        self.profile_public_id = profile_public_id

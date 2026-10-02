from fastapi import HTTPException
from app.repositories.address import AddressRepository
from app.schemas.address import AddressCreate
from app.models.address import Address
from app.services.geocoding import GeocodingService
from app.services.geo_calc import GeoCalculations
import logging

logger = logging.getLogger(__name__)

class AddressService():
    def __init__(
            self,address_repository: AddressRepository,geocoding_service:GeocodingService,geocalculations:GeoCalculations
            ):

        self.address_repository = address_repository
        self.geocoding_service = geocoding_service
        self.geocalculations = geocalculations

    def create_address(self,address_data:AddressCreate):
        """address creation service, which takes in address data, geocodes it, and saves it to the database"""
        logger.info("Creating address: %s", address_data.name)
        address = Address(
                name = address_data.name,
                street =address_data.street,
                city =address_data.city,
                state =address_data.state,
                postal_code =address_data.postal_code,
                country =address_data.country,
        )
        geo_service_data = {
                "street":address.street,
                "city":address.city,
                "state":address.state,
                "country":address.country,
                "format": "jsonv2",
                "limit": 1,
                }
        coordinates =  self.geocoding_service.adress_get_coordinates(geo_service_data)

        if not coordinates:
            logger.error("Failed to get coordinates for address: %s", address_data.name)
            raise HTTPException(
                status_code=400,
                detail="Failed to get coordinates for the provided address"
            )

        address.latitude = coordinates["latitude"]
        address.longitude = coordinates["longitude"]
        logger.info("Address created: id=%s, name=%s", address.id, address.name)
        return self.address_repository.create_address(address)

    def get_addresses(self):
        return self.address_repository.get_all_addresses()

    def get_address_by_id(self,id):
        return self.address_repository.get_address_by_id(id)

    def update_address(self, address_id, address_data):
        """Update an existing address with new data, including geocoding if location fields change. """
        verify_address= self.address_repository.get_address_by_id(address_id)
        if not verify_address:
            raise HTTPException(status_code=404, detail="Address not found")
        Address_data_dict = address_data.model_dump(exclude_unset=True)

        location_fields = {
                "street",
                "city",
                "state",
                "postal_code",
                "country",
        }

        location_changed = False

        for field in location_fields:
                if field in Address_data_dict:
                        old_value = getattr(verify_address, field)
                        new_value = Address_data_dict[field]

                        if old_value != new_value:
                                location_changed = True
                                break
        if location_changed:
                geo_data = {
                        "street": Address_data_dict.get("street", verify_address.street),
                        "city": Address_data_dict.get("city", verify_address.city),
                        "state": Address_data_dict.get("state", verify_address.state),
                        "postalcode": Address_data_dict.get("postal_code", verify_address.postal_code),
                        "country": Address_data_dict.get("country", verify_address.country),
                        "format": "jsonv2",
                        "limit": 1,
                }
                coordinates =  self.geocoding_service.adress_get_coordinates(geo_data)
                if not coordinates:
                        raise HTTPException(
                                status_code=400,
                                detail="Unable to geocode the updated address"
                        )
                Address_data_dict["latitude"] = coordinates["latitude"]
                Address_data_dict["longitude"] = coordinates["longitude"]
        address_update = self.address_repository.update_address(address_id,Address_data_dict)
        return address_update

    def delete_address(self, address_id):
        """Delete an address by its ID."""
        verify= self.address_repository.get_address_by_id(address_id)
        if not verify:
            raise HTTPException(status_code=404, detail="Address not found")
        success = self.address_repository.delete_address(address_id)
        if not success:
            raise HTTPException(status_code=404, detail="Address not found")
        return {"message": "Address deleted successfully"}
     
    def get_nearby_addresses(self, address_id,radius):
        """Get addresses within a specified radius (in kilometers) of a given address ID."""
        logger.info(
            "Nearby search: address_id=%s, radius_km=%s",
            address_id,
            radius
        )
        
        verify= self.address_repository.get_address_by_id(address_id)
        if not verify:
            raise HTTPException(status_code=404, detail="Address not found")
        latitude = verify.latitude
        longitude = verify.longitude
        bounds = self.geocalculations.get_bounding_box(latitude,longitude,radius)
        dataset = self.get_addresses()
        qualified_address = []
        for address in dataset:
                distance_in_km = self.geocalculations.calculate_distance(latitude,longitude,address.latitude, address.longitude)
                if (bounds["max_lat"] >= address.latitude >= bounds["min_lat"]
                    and
                    bounds["max_lon"] >= address.longitude >= bounds["min_lon"]
                    and
                    distance_in_km <= radius
                    ):
                    qualified_address.append(address)
        return qualified_address
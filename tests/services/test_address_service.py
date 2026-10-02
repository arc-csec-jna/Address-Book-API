from fastapi import HTTPException
import pytest

from app.schemas.address import AddressCreate, AddressUpdate

from app.services.address_service import AddressService

from app.repositories.address import AddressRepository
from app.services.geocoding import GeocodingService
from app.services.geo_calc import GeoCalculations

#defining the geo calculation service to be used in the tests
geo_calculations = GeoCalculations()
# defining a fake geocoder for a simulated test, so we dont have to rely on the actual geocoding service
class FakeGeocoder:
    def adress_get_coordinates(self, address_data):
        return {
            "latitude": 14.535,
            "longitude": 120.982,
        }
    
class FailedGeocoder:
    def adress_get_coordinates(self, address_data):
        return None

def test_create_address(db_session):
    # actual test data for creating an address
    address_data = AddressCreate(
        name="Test Address",
        street= "123 Street",
        city="sample city",
        state="sample state",
        postal_code="4027",
        country="Sample-istan",
        )
    
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    address_service = AddressService(address_repo, geocoding_service, geo_calculations)
    create_address = address_service.create_address(address_data)
    saved = address_repo.get_address_by_id(create_address.id)

    assert saved.latitude == 14.535
    assert saved.longitude == 120.982
    assert create_address.name == "Test Address"
    assert create_address.latitude == 14.535
    assert create_address.longitude == 120.982

def test_get_all_addresses(db_session):
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    address_service = AddressService(address_repo, geocoding_service, geo_calculations)

    # Create multiple addresses for testing
    address_data1 = AddressCreate(
        name="Address 1",
        street="123 Street",
        city="City A",
        state="State A",
        postal_code="12345",
        country="Country A",
    )
    address_data2 = AddressCreate(
        name="Address 2",
        street="456 Avenue",
        city="City B",
        state="State B",
        postal_code="67890",
        country="Country B",
    )

    address_service.create_address(address_data1)
    address_service.create_address(address_data2)

    all_addresses = address_service.get_addresses()

    assert len(all_addresses) == 2


def test_get_address_by_id(db_session):
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    address_service = AddressService(address_repo, geocoding_service, geo_calculations)

    # Create an address for testing
    address_data = AddressCreate(
        name="Test Address",
        street="123 Street",
        city="City A",
        state="State A",
        postal_code="12345",
        country="Country A",
    )
    created_address = address_service.create_address(address_data)

    retrieved_address = address_service.get_address_by_id(created_address.id)

    assert retrieved_address is not None
    assert retrieved_address.id == created_address.id
    assert retrieved_address.name == "Test Address"

def test_update_address(db_session):
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    address_service = AddressService(address_repo, geocoding_service, geo_calculations)

    # Create an address for testing
    address_data = AddressCreate(
        name="Test Address",
        street="123 Street",
        city="City A",
        state="State A",
        postal_code="12345",
        country="Country A",
    )
    created_address = address_service.create_address(address_data)

    # Update the address
    updated_data = AddressUpdate(
        name="Updated Address",
        street="456 Avenue",
        city="City B",
        state="State B",
        postal_code="67890",
        country="Country B",
    )
    updated_address = address_service.update_address(created_address.id, updated_data)

    assert updated_address is not None
    assert updated_address.id == created_address.id
    assert updated_address.name == "Updated Address"

def test_delete_address(db_session):
        address_repo = AddressRepository(db_session)
        geocoding_service = FakeGeocoder()
        address_service = AddressService(address_repo, geocoding_service, geo_calculations)

        # Create an address for testing
        address_data = AddressCreate(
            id=1,
            name="Test Address",
            street="123 Street",
            city="City A",
            state="State A",
            postal_code="12345",
            country="Country A",
        )
        created_address = address_service.create_address(address_data)

        # Delete the address
        deleted_address = address_service.delete_address(created_address.id)

        assert deleted_address is not None

        # Verify that the address is no longer in the database
        retrieved_address = address_service.get_address_by_id(created_address.id)
        assert retrieved_address is None

def test_get_nearby_addresses(db_session):
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    address_service = AddressService(
        address_repo,
        geocoding_service,
        geo_calculations
    )

    address_data = AddressCreate(
        name="Reference Address",
        street="123 Street",
        city="City A",
        state="State A",
        postal_code="12345",
        country="Country A",
    )

    reference_address = address_service.create_address(address_data)

    nearby_addresses = address_service.get_nearby_addresses(
        reference_address.id,
        10
    )

    assert reference_address in nearby_addresses

def test_failed_geocoding(db_session):
        address_repo = AddressRepository(db_session)
        geocoding_service = FailedGeocoder()
        geo_calculations = GeoCalculations()
        address_service = AddressService(address_repo, geocoding_service, geo_calculations)

        # Create an address with invalid data to simulate failed geocoding
        address_data = AddressCreate(
            name="Invalid Address",
            street="",
            city="",
            state="",
            postal_code="",
            country="",
        )

        with pytest.raises(HTTPException) as exc_info:
            address_service.create_address(address_data)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Failed to get coordinates for the provided address"


def test_address_nonexistent(db_session):
    address_repo = AddressRepository(db_session)
    geocoding_service = FakeGeocoder()
    geo_calculations = GeoCalculations()
    address_service = AddressService(address_repo, geocoding_service, geo_calculations)

    # Attempt to retrieve a non-existent address
    non_existent_id = 9999
    retrieved_address = address_service.get_address_by_id(non_existent_id)

    assert retrieved_address is None

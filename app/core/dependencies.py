from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.repositories.address import AddressRepository
from app.services.address_service import AddressService
from app.services.geocoding import GeocodingService
from app.services.geo_calc import GeoCalculations


def get_address_service(db:Session = Depends(get_db)):
    address_repository = AddressRepository(db)
    geocoding_service = GeocodingService()
    geocalculations = GeoCalculations()

    return AddressService(address_repository=address_repository,geocoding_service=geocoding_service,
    geocalculations=geocalculations)  # Pass None for geocalculations if not needed
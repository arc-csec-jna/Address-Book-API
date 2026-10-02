from fastapi import APIRouter,Depends, Query
from app.schemas.address import AddressCreate,AddressResponse,AddressUpdate

from app.services.address_service import AddressService

from app.core.dependencies import get_address_service

router =  APIRouter()

@router.post("/addresses",response_model=AddressResponse)
def create_address(
    address:AddressCreate,
    service:AddressService = Depends(get_address_service)
    ):
    return service.create_address(address)

@router.get("/addresses",response_model=list[AddressResponse])
def get_addresses(
    service: AddressService = Depends(get_address_service)
):
    return service.get_addresses()

@router.get("/addresses/{address_id}",response_model=AddressResponse)
def get_address_by_id(
    address_id:int,
    service: AddressService = Depends(get_address_service)
    ):
    return service.get_address_by_id(address_id)

@router.put("/addresses/{address_id}",response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    service: AddressService = Depends(get_address_service)
):
    return service.update_address(address_id,address_data)

@router.delete("/addresses/{address_id}")
def delete_address(
            address_id: int, 
            service: AddressService = Depends(get_address_service)
            ):
    return service.delete_address(address_id)

@router.get("/addresses/{address_id}/nearby",response_model=list[AddressResponse])
def get_nearby_addresses(
    address_id: int,
    radius: float = Query(ge=0),
    service: AddressService = Depends(get_address_service)
):
    return service.get_nearby_addresses(address_id, radius)
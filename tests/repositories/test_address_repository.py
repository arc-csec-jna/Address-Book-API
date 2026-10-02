from app.models.address import Address
from app.repositories.address import AddressRepository

def test_create_address(db_session):
    address_repo = AddressRepository(db_session)

    address_sample = Address(
        name="sample",
        street= "123 Street",
        city="sample city",
        state="sample state",
        postal_code="4027",
        country="Sample-istan",
    )

    created_address = address_repo.create_address(address_sample)

    assert created_address.id is not None
    assert created_address.name == "sample"


def test_update_adress(db_session):
    address_repo = AddressRepository(db_session)

    address_sample = Address(
    name="sample",
    street= "123 Street",
    city="sample city",
    state="sample state",
    postal_code="4027",
    country="Sample-istan",
    )
    
    db_session.add(address_sample)
    db_session.commit()

    updated_data = {
        "name": "updated_sample",
    }

    updated_address = address_repo.update_address(address_sample.id,updated_data)

    assert updated_address.name == "updated_sample"

def test_delete_job(db_session):
    address_repo = AddressRepository(db_session)

    address_sample = Address(
        name="sample",
        street= "123 Street",
        city="sample city",
        state="sample state",
        postal_code="4027",
        country="Sample-istan",
        )

    db_session.add(address_sample)
    db_session.commit()

    result = address_repo.delete_address(address_sample.id)
    
    assert result is True
    assert address_repo.get_address_by_id(address_sample.id) is None
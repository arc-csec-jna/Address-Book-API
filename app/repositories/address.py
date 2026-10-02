"""
Repository layer to communicate with SQLite database through SQLAlchemy ORM

delete

"""
from app.models.address import Address

class AddressRepository:
    def __init__(self,db):
        self.db = db

    def create_address(self,Address):
        """ create a new address entry"""
        self.db.add(Address)
        self.db.commit()
        self.db.refresh(Address)
        return Address

    def get_all_addresses(self):
        """poll all addresses"""
        return(
            self.db.query(Address)
            .all()
        )

    def get_address_by_id(self, address_id):
        """check address by id"""
        return self.db.query(Address).filter(Address.id == address_id).first()

    def update_address(self,id,address_data):
        address =  self.get_address_by_id(id)
        if address:
            for key, value in address_data.items():
                setattr(address, key, value)
            self.db.commit()
            return address
        return None

    def delete_address(self, id):
        add = self.get_address_by_id(id)
        if add:
            self.db.delete(add)
            self.db.commit()
            return True
        return False
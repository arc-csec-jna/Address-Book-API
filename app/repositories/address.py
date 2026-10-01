"""
Repository layer to communicate with SQLite database through SQLAlchemy ORM

delete

"""
from app.models import address

class AddressRepository:
    def __init__(self,db):
        self.db = db

    def create_address(self,address):
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_all_addresses(self,id):
        return(
            self.db.query(address)
            .filter(address.id == id)
            .all()
        )

    def get_add_by_id(self, address_id):
        return self.db.query(address).filter(address.id == address_id).first()

    def update_address(self,id,address_data):
        address =  self.get_add_by_id(id)
        if address:
            for key, value in address_data.items():
                setattr(address, key, value)
            self.db.commit()
            return address
        return None

    def delete_address(self, id):
        add = self.get_add_by_id(id)
        if add:
            self.db.delete(add)
            self.db.commit()
            return True
        return False
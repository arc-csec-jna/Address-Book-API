from app.core.database import Base, engine
from app.models.address import Address

Base.metadata.create_all(bind=engine)
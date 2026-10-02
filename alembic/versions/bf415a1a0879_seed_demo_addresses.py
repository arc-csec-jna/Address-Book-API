"""Seed Demo addresses
Revision ID: bf415a1a0879
Revises: 45607f465604
Create Date: 2026-10-02 15:49:39.249757

"""
from typing import Sequence, Union
from datetime import datetime
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'bf415a1a0879'
down_revision: Union[str, Sequence[str], None] = '45607f465604'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    addresses = sa.table(
    "addresses",
    sa.column("name", sa.String),
    sa.column("street", sa.String),
    sa.column("city", sa.String),
    sa.column("state", sa.String),
    sa.column("postal_code", sa.String),
    sa.column("country", sa.String),
    sa.column("latitude", sa.Float),
    sa.column("longitude", sa.Float),
    sa.column("created_at", sa.DateTime),
    sa.column("updated_at", sa.DateTime),
    )

    op.bulk_insert(
        addresses,
        [
            {
                "name": "SM Mall of Asia",
                "street": "Seaside Boulevard, Barangay 76",
                "city": "Pasay City",
                "state": "Metro Manila",
                "postal_code": "1300",
                "country": "Philippines",
                "latitude": 14.5350667,
                "longitude": 120.9821528,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "name": "SM Mall of Asia Arena",
                "street": "Jose W. Diokno Boulevard",
                "city": "Pasay City",
                "state": "Metro Manila",
                "postal_code": "1300",
                "country": "Philippines",
                "latitude": 14.53225,
                "longitude": 120.98374,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "name": "SM By The Bay",
                "street": "Seaside Boulevard, MOA Complex",
                "city": "Pasay City",
                "state": "Metro Manila",
                "postal_code": "1300",
                "country": "Philippines",
                "latitude": 14.5363,
                "longitude": 120.97943,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "name": "Ayala Malls Manila Bay",
                "street": "Macapagal Boulevard corner Asean Avenue",
                "city": "Parañaque City",
                "state": "Metro Manila",
                "postal_code": "1701",
                "country": "Philippines",
                "latitude": 14.52342,
                "longitude": 120.9881,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "name": "Libertad Station",
                "street": "Taft Avenue",
                "city": "Pasay City",
                "state": "Metro Manila",
                "postal_code": "1300",
                "country": "Philippines",
                "latitude": 14.54775,
                "longitude": 120.99864,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ],
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    addresses = sa.table(
        "addresses",
        sa.column("name", sa.String),
    )

    op.execute(
        addresses.delete().where(
            addresses.c.name.in_(
                [
                    "SM Mall of Asia",
                    "SM Mall of Asia Arena",
                    "SM By The Bay",
                    "Ayala Malls Manila Bay",
                    "Libertad Station",
                ]
            )
        )
    )
    pass

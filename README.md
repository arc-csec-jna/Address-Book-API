# Address Book API
A small FastAPI backend for managing addresses with geocoded coordinates and nearby-address search.
## Features
- Create, read, update, and delete addresses
- Address coordinates generated automatically through geocoding
- Nearby-address search using latitude/longitude

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic / Pydantic Settings
- HTTPX
- Pytest
- OpenStreetMap Nominatim for geocoding

## Project Structure

```text
AddressBook-ProofofConcept/
│
├── alembic/                         # Database migrations
│   └── versions/
│
├── app/
│   ├── core/                        # Application configuration & infrastructure
│   │   ├── config.py               # Environment/settings configuration
│   │   ├── database.py             # SQLAlchemy engine & database session
│   │   └── dependencies.py         # FastAPI dependency injection
│   │
│   ├── models/                      # SQLAlchemy database models
│   │   └── address.py
│   │
│   ├── repositories/                # Database access layer
│   │   └── address.py              # Address CRUD persistence
│   │
│   ├── routes/                      # HTTP/API layer
│   │   └── address.py              # Address endpoints
│   │
│   ├── schemas/                     # Pydantic request/response models
│   │   └── address.py
│   │
│   ├── services/                    # Application/business logic
│   │   ├── address_service.py      # Address operations & orchestration
│   │   ├── geocoding.py            # External geocoding integration
│   │   └── geo_calc.py             # Distance & bounding-box calculations
│   │
│   └── main.py                      # FastAPI application entry point
│
├── tests/                            # Automated tests
│
├── data/                             # Local SQLite database files
│
├── .env                              # Local environment configuration
├── alembic.ini                       # Alembic configuration
├── pyproject.toml                    # Project & dependency configuration
└── README.md                         # Project documentation
```

### Architecture

The application follows a lightweight layered architecture:

```text
                    ┌──────────────────┐
                    │    FastAPI API   │
                    │     Routes       │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │     Services     │
                    │ Business Logic   │
                    └──────┬─────┬─────┘
              ┌────────────┘     └──────────────┐
              ▼                                 ▼
    ┌──────────────────┐              ┌──────────────────┐
    │   Repository     │              │ External Services│
    │  SQLAlchemy/DB   │              │   Geocoding      │
    └────────┬─────────┘              └──────────────────┘
             ▼
    ┌──────────────────┐
    │      SQLite      │
    └──────────────────┘
```

The main separation of responsibilities is:

- **Routes** — handle HTTP requests and responses.
- **Services** — coordinate application logic and business rules.
- **Repositories** — handle database persistence.
- **Models** — define the database structure.
- **Schemas** — validate API input and shape API responses.
- **Geocoding** — isolates the external geocoding provider.
- **Geo calculations** — handles geographic calculations independently from the API and database layers.
- **Core** — contains shared application infrastructure and dependency wiring.

## Architecture
```text
The application uses a simple layered structure:
HTTP Request
     ▼
 FastAPI Routes
     ▼
 Address Service
     ├─────► Geocoding Service
     ├─────► Geo Calculations
     ▼
 Address Repository
     ▼
   SQLite
```
### Routes
Responsible for HTTP concerns such as request validation, response models, and dependency injection.

### Services
Application and Business rules
`AddressService` coordinates address creation, updates, deletion, geocoding, and nearby searches.
### Repository
Handles database persistence and CRUD operations through SQLAlchemy.
### Geocoding Service
Encapsulates communication with the external geocoding service.
### Geo Calculations
Contains geographic calculations such as Haversine distance and bounding-box generation.

## Requirements

- Python 3.12+
- Internet connection for address geocoding

## Setup
Clone the repository and enter the project directory.
Create a virtual environment:
    python -m venv .venv
Activate it on Windows:
    .venv\Scripts\activate
Activate it on Linux/macOS:
    source .venv/bin/activate

project and development dependencies:
    pip install -e ".[dev]"

## Environment Configuration
Create a `.env` file in the project root:
    DATABASE_URL=sqlite:///./data/address_book.db

## Database Setup

Apply the Alembic migrations:
    alembic upgrade head
    we have included some demo addresses during migration for easier evaluation

## Running the API
    uvicorn app.main:app --reload
## API Endpoints

POST `/addresses` - Create an address
GET `/addresses` - Get all addresses 
GET `/addresses/{address_id}` - Get an address 
PUT `/addresses/{address_id}` - Update an address 
DELETE `/addresses/{address_id}` - Delete an address 
GET `/addresses/{address_id}/nearby` - Find addresses within a radius 

### Creating an Address

The API accepts a human-readable address.

Latitude and longitude are generated by the backend through the geocoding service, user is not required to supply coordinates

Example:
{
  "name": "SM Mall of Asia",
  "street": "Seaside Boulevard, Barangay 76",
  "city": "Pasay City",
  "state": "Metro Manila",
  "postal_code": "1300",
  "country": "Philippines"
}

### Nearby Search

Nearby searches use an existing address as the reference point:
    GET /addresses/{address_id}/nearby?radius=10

The radius is specified in kilometers.
```text
Reference Address
       ▼
Bounding Box -  we define the limits of the boundaries of the coordinates
       ▼
Candidate Addresses -  we extract addresses within the boundaries
       ▼
Haversine Distance - we calculate exact distance using the haversine distance
       ▼
Addresses within radius
```
## Testing

Run the test suite with:  pytest

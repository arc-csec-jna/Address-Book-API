
import httpx
import logging

logger = logging.getLogger(__name__)

class GeocodingService():
    """ Service to get coordinates from an address using OpenStreetMap's Nominatim API. """
    def adress_get_coordinates(self,address_data):
        url = "https://nominatim.openstreetmap.org/search"
        headers = {
                    "User-Agent": "address-book-api/0.1"
                }
        try:
            response = httpx.get(url,
                                params=address_data,
                                headers=headers,
                                timeout=5)
        except httpx.RequestError:
            logger.error("Error occurred while making the request to the geocoding service")
            return None
        try:
            response.raise_for_status()
            results = response.json()
        except httpx.HTTPStatusError:
            logger.error("Geocoding service returned HTTP error: %s",response.status_code)
            return None

        if not results:  
            logger.warning("No geocoding result for address")
            return None

        return {
            "latitude": float(results[0]["lat"]),
            "longitude": float(results[0]["lon"]),
        }

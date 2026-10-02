from math import radians,sin,cos,atan2,sqrt
"""
meat & potatoes = 
find bounds
query nearby addrresses
calculate distance using haversine formula in terms of kilometers
"""
class GeoCalculations():
    def calculate_distance(self,lat1,lon1,lat2,lon2):
    # converting to radians for python trigo compatibility
        lat1 =  radians(lat1)
        lon1 =  radians(lon1)
        lat2 =  radians(lat2)
        lon2 =  radians(lon2)
    # calculating distances
        dlat = lat2 - lat1
        dlon = lon2 - lon1
    # Haversine Formula
        a = (
            sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
        )
    # calculating angular distance
        c = 2 * atan2(sqrt(a),sqrt(1-a))
        
        # Earth's approx radius / we substitute it with the search distance
        R = 6371 

        distance =  R * c
        return distance

    def get_bounding_box(self,lat,lon,radius):
        """
        get the  boundary box of the location based on the edges of the coordinates
        but it doesnt add up to the idea of radius cause addresses might be inside the bounding box but not "inside the circle" of the radius
        """
        delta_lat = radius / 111
        delta_lon = radius / (111*cos(radians(lat)))

        min_lat = lat - delta_lat
        max_lat = lat + delta_lat
        min_lon = lon - delta_lon
        max_lon = lon + delta_lon

        bounds = {
            "min_lat":min_lat,
            "max_lat":max_lat,
            "min_lon":min_lon,
            "max_lon":max_lon,
        }
        return bounds

           
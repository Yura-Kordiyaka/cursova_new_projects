from django.conf import settings
import googlemaps

def get_coordinates(address: str):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

    geocode_result = gmaps.geocode(address)

    if geocode_result and len(geocode_result) > 0:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        pass
import requests
import asyncio
import geocoder
from bs4 import BeautifulSoup
from threading import Thread
from encryption import Encryption
import winsdk.windows.devices.geolocation as wdg


# this function returns geological coordinates
# return value is (latitude , longitude)
# type of latitude and longitude is float
# ---------------------------------------------------------------------------------------------------------------
def geoLogicalCoordinate(location) -> tuple:
    try:
        url = f"https://www.google.com/search?q=coordinates+of+{location}&rlz="
        response = requests.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        coordinates=soup.find(class_="BNeawe iBp4i AP7Wnd").text
        coordinates = coordinates.replace("°", "").split()
        coordinates = (float(coordinates[0]), float(coordinates[2]))
        return coordinates
    except:
        try:
            api_key = Encryption(b'gAAAAABkeaxIj8UrJhRqbsS40fzJxHWJAAiz1EFHFkUSD0ehhz6g2BVvaVBhAE9lqQc8jzYJmfEtWQmIn7e44-yHlmpkATwpCpbRCWaqzFyWz0lwLwn_TMHLYWH0hb_x9VcxMdvOaMk58UzQm26qNa2TW2e4a5Y_VdCIXquuW9h_VLcgOAm9vYOp_mM1LPJL8QtuZOvvKr9gMVMHGOuvKwVW_HRpeb9tFg==').decrypt_text()
            loc = geocoder.bing(location, key=api_key)
            results = loc.json
            location_coordinates = [results['lat'], results['lng']]
            return location_coordinates
        except:
            return None
# ---------------------------------------------------------------------------------------------------------------
    

# This function is used for reverse geocoding. It takes two parameters: latitude and longitude.
# The function returns the address in the form of a string.
# ---------------------------------------------------------------------------------------------------------------
def reverseGeocoding(latitude, longitude) -> str:
    api_key = Encryption(b'gAAAAABkeaxIj8UrJhRqbsS40fzJxHWJAAiz1EFHFkUSD0ehhz6g2BVvaVBhAE9lqQc8jzYJmfEtWQmIn7e44-yHlmpkATwpCpbRCWaqzFyWz0lwLwn_TMHLYWH0hb_x9VcxMdvOaMk58UzQm26qNa2TW2e4a5Y_VdCIXquuW9h_VLcgOAm9vYOp_mM1LPJL8QtuZOvvKr9gMVMHGOuvKwVW_HRpeb9tFg==').decrypt_text()
    g = geocoder.bing([latitude, longitude], method='reverse', key=api_key)
    if g.ok:
        return g.address
    else:
        return None
# ---------------------------------------------------------------------------------------------------------------


# # Microsoft entity recoginition
# # Returned value is list of dictionaries
# # -------------------------------------------------------------------------------------------------------
def entityRecognition(query):
    url = "https://microsoft-text-analytics1.p.rapidapi.com/entities/recognition/general"
    payload = { "documents": [
            {
                "id": "1",
                "language": "en",
                "text": f"{query}"
            }
        ] }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": Encryption(b'gAAAAABkdNC0bFPjzH9FbfRkmdDx5IRirUNgLUFYCpoTGpb_YR19b4eT-1ZHSFd9CooiBwZfRh3pqgSucqk_k1u3xY0mer3k-sbgRvAJczI6qXUeCKouOQOY9AE-gdptHZOSA90gP4-VA-8rNkkltcVoaLJTdx72Tg==').decrypt_text(),
        "X-RapidAPI-Host": "microsoft-text-analytics1.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    entities = response.get('documents')[0].get('entities')
    return entities
#  -------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------
class Route:
    def __init__(self, query):
        self.query = query
        self.coordinates = set()
        self.origin = None
        self.destination = None
        self._route = None

    # Convert address into geological coordinates and add into the set coordinates
    def geoCoding(self, location):
        coordinate = geoLogicalCoordinate(location)
        self.coordinates.add(coordinate)

    # this function is used to retrieve route coordinates, distance and time
    def routeAPI(self):
        self.destination = self.coordinates.pop()
        self.origin = self.coordinates.pop()
        url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        querystring = {"stops": f"{self.origin[0]}, {self.origin[1]};{self.destination[0]}, {self.destination[1]}"}
        headers = {
            "X-RapidAPI-Key": Encryption(b'gAAAAABkdNDgPoPyiGQ7Zz3fYaU3-YRQjHdpR9YBN2bOOoHorYh0UpbYazTUx41TtTmjwyokrCa6W5NOxBdFfpe-3fkTnuRA06eplauxkDW6upNUDk7r3oRh37bDxgK756JYoySTloRqnyIdl9ZXD32-BmEqdP0Fkg==').decrypt_text(),
            "X-RapidAPI-Host": "trueway-directions2.p.rapidapi.com"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring).json()
        distance = str(int(response["route"]["distance"])/1000)
        duration = int(response["route"]["duration"])//60
        if duration >= 60:
            hr = duration//60
            minn = duration % 60
            durationTime = f"{hr} hrs {minn} min"
        else:
            durationTime = f"{duration} min"
        routes = response["route"]["geometry"]["coordinates"]
        self._route = {"distance" : distance,
                       "time" : durationTime,
                       "route": routes}

    def route(self):
        entities = entityRecognition(self.query)
        location = set()
        for enitity in entities:
            location.add(enitity.get('text'))
        if len(location)!=2:
            return None, None
        else:
            origin = location.pop()
            destination = location.pop()
            thread1 = Thread(target=self.geoCoding, args=(origin,))
            thread2 = Thread(target=self.geoCoding, args=(destination,))
            thread1.start(), thread2.start()
            thread1.join(), thread2.join()
            self.routeAPI()
            location = {"origin" : self.origin,
                        "destination": self.destination}
            return location, self._route
            
# ---------------------------------------------------------------------------------------------------------------


# This function is used to get location of the device using ip address
# ---------------------------------------------------------------------------------------------------------------
def ip_based_location() -> dict:
    try:
        ip_address = requests.get('https://api64.ipify.org?format=json').json()
        response=requests.post("http://ip-api.com/batch", json=[{"query":ip_address.get('ip')}]).json()
        return response[0]
    except:
        return None
    

# GPS Based Location
# This class returns the current coordinates of the device based on the GPS Location
# ---------------------------------------------------------------------------------------------------------------
class GPS:
    async def getCoordinates():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        return [pos.coordinate.latitude, pos.coordinate.longitude]

    def getLocation():
        try:
            return asyncio.run(GPS.getCoordinates())
        except PermissionError:
            print("You need to allow applications to access you location in Windows settings")
            return None
# ---------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    print(GPS.getLocation())

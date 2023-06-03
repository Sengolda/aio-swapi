from .http import HTTPClient
from .objects import Film, Person, Planet, Starship, Vehicle

__all__ = (
    "Client",
)

class Client:
    def __init__(self) -> None:
        self.http = HTTPClient()

    async def get_person(self, person_id: int):
        raw_data = await self.http.request("people/{0}".format(person_id))
        return Person(raw_data, http=self.http)

    async def get_film(self, film_id: int):
        raw_data = await self.http.request("films/{0}".format(film_id))
        return Film(raw_data, http=self.http)

    async def get_starship(self, starship_id: int):
        raw_data = await self.http.request("starships/{0}".format(starship_id))
        return Starship(raw_data, http=self.http)

    async def get_vehicle(self, vehicle_id: int):
        raw_data = await self.http.request("vehicles/{0}".format(vehicle_id))
        return Vehicle(raw_data, http=self.http)

    async def get_planet(self, planet_id: int):
        raw_data = await self.http.request("planets/{0}".format(planet_id))
        return Planet(raw_data, http=self.http)

    async def search_people(self, query: str, page: int = 1):
        raw_data = await self.http.request("people", params={"page": page, "search": query})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for person_data in results:
            returning.append(Person(person_data, http=self.http))
        return returning

    async def search_films(self, query: str, page: int = 1):
        raw_data = await self.http.request("films", params={"page": page, "search": query})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for film_data in results:
            returning.append(Film(film_data, http=self.http))
        return returning

    async def search_starships(self, query: str, page: int = 1):
        raw_data = await self.http.request("starships", params={"search": query, "page": page})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for starship_data in results:
            returning.append(Starship(starship_data, http=self.http))
        return returning

    async def search_vehicles(self, query: str, page: int = 1):
        raw_data = await self.http.request("starships", params={"search": query, "page": page})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for vehicle_data in results:
            returning.append(Vehicle(vehicle_data, http=self.http))
        return returning

    async def search_planets(self, query: str, page: int = 1):
        raw_data = await self.http.request("planets", params={"search": query, "page": page})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for planet_data in results:
            returning.append(Planet(planet_data, http=self.http))
        return returning

    @property
    def close(self):
        return self.http.close

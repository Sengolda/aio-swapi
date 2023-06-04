from functools import lru_cache
from types import TracebackType
from typing import Optional, Type, TypeVar

from .http import HTTPClient
from .objects import Film, Person, Planet, Specie, Starship, Vehicle

BE = TypeVar("BE", bound=BaseException)
C = TypeVar("C", bound="Client")

__all__ = ("Client",)


class Client:
    def __init__(self) -> None:
        self.http = HTTPClient()

    async def __aenter__(self) -> C:
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BE]], exc_value: Optional[BE], exc_traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    async def get_person(self, person_id: int) -> Person:
        raw_data = await self.http.request("people/{0}".format(person_id))
        return Person(raw_data, http=self.http)

    async def get_film(self, film_id: int) -> Film:
        raw_data = await self.http.request("films/{0}".format(film_id))
        return Film(raw_data, http=self.http)

    async def get_starship(self, starship_id: int) -> Starship:
        raw_data = await self.http.request("starships/{0}".format(starship_id))
        return Starship(raw_data, http=self.http)

    async def get_vehicle(self, vehicle_id: int) -> Vehicle:
        raw_data = await self.http.request("vehicles/{0}".format(vehicle_id))
        return Vehicle(raw_data, http=self.http)

    async def get_planet(self, planet_id: int) -> Planet:
        raw_data = await self.http.request("planets/{0}".format(planet_id))
        return Planet(raw_data, http=self.http)

    async def get_specie(self, specie_id: int) -> Specie:
        raw_data = await self.http.request("species/{0}".format(specie_id))
        return Specie(raw_data, http=self.http)

    async def _all_data(self, _type: str):
        data = await self.http.request(_type)
        count = 0
        results = {count: data["results"]}
        next = True
        while next:
            next_page = data.get("next")
            if next_page:
                data = await self.http.request(next_page)
                next_page = data["next"]
                count += 1
                results[count] = data["results"]
            else:
                next = False
        return results

    @lru_cache(maxsize=None)
    async def get_all_planets(self):
        raw_data = await self._all_data("planets")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Planet(item, http=self.http))
        return returning

    @lru_cache(maxsize=None)
    async def get_all_vehicles(self):
        raw_data = await self._all_data("vehicles")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Vehicle(item, http=self.http))
        return returning

    @lru_cache(maxsize=None)
    async def get_all_people(self):
        raw_data = await self._all_data("people")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Person(item, http=self.http))
        return returning

    @lru_cache(maxsize=None)
    async def get_all_films(self):
        raw_data = await self._all_data("films")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Film(item, http=self.http))
        return returning

    @lru_cache(maxsize=None)
    async def get_all_species(self):
        raw_data = await self._all_data("species")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Specie(item, http=self.http))
        return returning

    @lru_cache(maxsize=None)
    async def get_all_starships(self):
        raw_data = await self._all_data("starships")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Specie(item, http=self.http))
        return returning

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

    async def search_species(self, query: str, page: int = 1):
        raw_data = await self.http.request("species", params={"search": query, "page": page})
        results = raw_data.get("results")
        if not results:
            return []
        returning = []
        for planet_data in results:
            returning.append(Specie(planet_data, http=self.http))
        return returning

    @property
    def close(self):
        return self.http.close

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self, TracebackType
    from typing import Union, Type, List, TypeVar

    BE = TypeVar("BE", bound=BaseException)

from async_lru import alru_cache

from .http import HTTPClient
from .objects import Film, Person, Planet, Specie, Starship, Vehicle


__all__ = ("Client",)


class Client:
    """
    Represents a client
    """

    def __init__(self) -> None:
        self.http = HTTPClient()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: Union[Type[BE], None], exc_value: Union[BE, None], exc_traceback: Union[TracebackType, None]
    ) -> None:
        await self.close()

    async def get_person(self, person_id: int) -> Person:
        """Gets a person by id

        Parameters
        ---------
           person_id: :class:`int`
              The ID of the person in the API
        """
        raw_data = await self.http.request("people/{0}".format(person_id))
        return Person(raw_data, http=self.http)

    async def get_film(self, film_id: int) -> Film:
        """Gets a film by id

        Parameters
        ---------
           film_id: :class:`int`
              The ID of the film in the API
        """

        raw_data = await self.http.request("films/{0}".format(film_id))
        return Film(raw_data, http=self.http)

    async def get_starship(self, starship_id: int) -> Starship:
        """Gets a starship by id

        Parameters
        ---------
           starship_id: :class:`int`
              The ID of the starship in the API
        """
        raw_data = await self.http.request("starships/{0}".format(starship_id))
        return Starship(raw_data, http=self.http)

    async def get_vehicle(self, vehicle_id: int) -> Vehicle:
        """Gets a vehicle by id

        Parameters
        ---------
           vehicle_id: :class:`int`
              The ID of the vehicle in the API
        """
        raw_data = await self.http.request("vehicles/{0}".format(vehicle_id))
        return Vehicle(raw_data, http=self.http)

    async def get_planet(self, planet_id: int) -> Planet:
        """Gets a planet by id

        Parameters
        ---------
           planet_id: :class:`int`
              The ID of the planet in the API
        """
        raw_data = await self.http.request("planets/{0}".format(planet_id))
        return Planet(raw_data, http=self.http)

    async def get_specie(self, specie_id: int) -> Specie:
        """Gets a specie by id

        Parameters
        ---------
           specie_id: :class:`int`
              The ID of the specie in the API
        """
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

    @alru_cache(maxsize=None)
    async def get_all_planets(self) -> List[Planet]:
        """
        Gets all the planets in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Planet`
        """
        raw_data = await self._all_data("planets")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Planet(item, http=self.http))
        return returning

    @alru_cache(maxsize=None)
    async def get_all_vehicles(self) -> List[Vehicle]:
        """
        Gets all the vehicles in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Vehic;e`
        """
        raw_data = await self._all_data("vehicles")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Vehicle(item, http=self.http))
        return returning

    @alru_cache(maxsize=None)
    async def get_all_people(self) -> List[Person]:
        """
        Gets all the people in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Person`
        """
        raw_data = await self._all_data("people")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Person(item, http=self.http))
        return returning

    @alru_cache(maxsize=None)
    async def get_all_films(self) -> List[Film]:
        """
        Gets all the film in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Film`
        """
        raw_data = await self._all_data("films")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Film(item, http=self.http))
        return returning

    @alru_cache(maxsize=None)
    async def get_all_species(self) -> List[Specie]:
        """
        Gets all the species in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Specie`
        """
        raw_data = await self._all_data("species")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Specie(item, http=self.http))
        return returning

    @alru_cache(maxsize=None)
    async def get_all_starships(self) -> List[Starship]:
        """
        Gets all the starships in the API

        Returns
        --------
        Returns a list of :class:`~aioswapi.Starship`
        """
        raw_data = await self._all_data("starships")
        returning = []
        for key in raw_data.keys():
            for item in raw_data[key]:
                returning.append(Starship(item, http=self.http))
        return returning

    async def search_people(self, query: str) -> List[Person]:
        """
        Searches people by name

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Person`
        """
        all_people = await self.get_all_people()
        query_matched_results = [person for person in all_people if query.lower() in person.name.lower()]
        return query_matched_results

    async def search_films(self, query: str) -> List[Film]:
        """
        Searches films by title

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Film`
        """
        all_films = await self.get_all_films()
        query_matched_results = [film for film in all_films if query.lower() in film.title.lower()]
        return query_matched_results

    async def search_starships(self, query: str) -> List[Starship]:
        """
        Searches starships by name

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Starship`
        """
        all_starships = await self.get_all_starships()
        query_matched_results = [starship for starship in all_starships if query.lower() in starship.name.lower()]
        return query_matched_results

    async def search_vehicles(self, query: str) -> List[Vehicle]:
        """
        Searches vehicles by name

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Vehicle`
        """
        all_vehicles = await self.get_all_vehicles()
        query_matched_results = [vehicle for vehicle in all_vehicles if query.lower() in vehicle.name.lower()]
        return query_matched_results

    async def search_planets(self, query: str):
        """
        Searches planets by name

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Planet`
        """
        all_planets = await self.get_all_planets()
        query_matched_results = [planet for planet in all_planets if query.lower() in planet.name.lower()]
        return query_matched_results

    async def search_species(self, query: str):
        """
        Searches planets by name

        Parameters
        ---------
        query: :class:`str` The search query you are looking for

        Returns
        --------
        Returns a list of :class:`~aioswapi.Specie`
        """
        all_species = await self.get_all_species()
        query_matched_results = [specie for specie in all_species if query.lower() in specie.name.lower()]
        return query_matched_results

    @property
    def close(self):
        return self.http.close

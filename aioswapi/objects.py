from typing import List

from async_lru import alru_cache

from .utils import copy_doc

__all__ = (
    "Person",
    "Planet",
    "Starship",
    "Film",
    "Vehicle",
    "Specie",
)


class _Object:
    def __init__(self, raw_data: dict, *, http) -> None:
        self.raw_data = raw_data
        self.http = http
        for key, value in raw_data.items():
            if value in ("n/a", "none"):
                value = None

            setattr(self, key, value)


class Film(_Object):
    """Represents a film"""

    @alru_cache(maxsize=None)
    async def get_starships(self) -> List["Starship"]:
        """Returns a list of :class:`~aioswapi.Starship` objects that appeared in this film"""

        starships = []
        for starship in self.starships:
            raw_data = await self.http.request(starship)
            starship.append(Starship(raw_data, http=self.http))
        self.starships = starships
        return starships

    @alru_cache(maxsize=None)
    async def get_characters(self) -> List["Person"]:
        """Returns a list of :class:`~aioswapi.Person` objects"""

        characters = []
        for character in self.characters:
            raw_data = await self.http.request(character)
            characters.append(Person(raw_data, http=self.http))
        self.characters = characters
        return characters

    @alru_cache(maxsize=None)
    async def get_vehicles(self) -> List["Vehicle"]:
        """Returns a list of :class:`~aioswapi.Vehicle` objects"""

        vehicles = []
        for vehicle in self.vehicles:
            raw_data = await self.http.request(vehicle)
            vehicles.append(Vehicle(raw_data, http=self.http))
        self.vehicles = vehicles
        return vehicles

    @alru_cache(maxsize=None)
    async def get_planets(self) -> List["Planet"]:
        """Returns a list of :class:`~aioswapi.Planet` objects"""
        planets = []
        for planet in self.planets:
            raw_data = await self.http.request(planet)
            planets.append(Planet(raw_data, http=self.http))
        self.planets = planets
        return planets

    @alru_cache(maxsize=None)
    async def get_species(self) -> List["Specie"]:
        """Returns a list of :class:`~aioswapi.Specie` objects"""
        species = []
        for specie in self.species:
            raw_data = await self.http.request(specie)
            species.append(Specie(raw_data, http=self.http))
        self.species = species
        return species


class Person(_Object):
    @alru_cache(maxsize=None)
    async def get_films(self) -> List[Film]:
        """Returns a list of :class:`~aioswapi.Film` objects"""
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        self.films = films
        return films

    @copy_doc(Film.get_starships)
    @alru_cache(maxsize=None)
    async def get_starships(self) -> List["Starship"]:
        starships = []
        for starship in self.starships:
            raw_data = await self.http.request(starship)
            starships.append(Starship(raw_data, http=self.http))
        self.starships = starships
        return starships

    @alru_cache(maxsize=None)
    async def get_homeworld(self) -> "Planet":
        """Returns the homeworld of the person as a :class:`~aioswapi.Planet` object"""
        raw_data = await self.http.request(self.homeworld)
        self.homeworld = homeworld = Planet(raw_data, http=self.http)
        return homeworld

    @copy_doc(Film.get_species)
    @alru_cache(maxsize=None)
    async def get_species(self) -> List["Specie"]:
        species = []
        for specie in species:
            raw_data = await self.http.request(specie)
            species.append(Specie(raw_data, http=self.http))
        self.species = species
        return species


class Planet(_Object):
    @alru_cache(maxsize=None)
    async def get_residents(self) -> List[Person]:
        """Returns a list of residents in the planet as a list of :class:`aioswapi.Person` objects"""
        residents = []
        for resident in self.residents:
            raw_data = await self.http.request(resident)
            residents.append(Person(raw_data, http=self.http))
        self.residents = residents
        return residents

    @alru_cache(maxsize=None)
    async def get_films(self) -> List[Film]:
        """Returns a list of :class:`~aioswapi.Film` this person has been in"""
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        self.films = films
        return films


class Specie(_Object):
    @alru_cache(maxsize=None)
    async def get_people(self) -> List[Person]:
        """Returns the people who are a type of this species as a list of :class:`~aioswapi.Person` objects"""
        people = []
        for person in self.people:
            raw_data = await self.http.request(person)
            people.append(Person(raw_data, http=self.http))
        self.people = people
        return people

    @alru_cache(maxsize=None)
    async def get_films(self) -> List[Film]:
        """Returns a list of films this type of species has been in as a list :class:`~aioswapi.Film` objects"""
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        self.films = films
        return films


class Starship(_Object):
    @alru_cache(maxsize=None)
    async def get_pilots(self) -> List[Person]:
        """Returns a list of :class:`~aioswapi.Person` who have piloted this starship"""
        pilots = []
        for pilot in self.pilots:
            raw_data = await self.http.request(pilot)
            pilots.append(Person(raw_data, http=self.http))
        self.pilots = pilots
        return pilots

    @alru_cache(maxsize=None)
    async def get_films(self) -> List[Film]:
        """Returns a list of :class:`~aioswapi.Film` objects, it returns all the films this starship has appeared in"""
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        self.films = films
        return films


class Vehicle(Starship):
    pass


setattr(
    Vehicle.get_films,
    "__doc__",
    "Returns a list of :class:`~aioswapi.Film` objects, it returns all the films this vehicle has appeared in",
)
setattr(Vehicle.get_pilots, "__doc__", "Returns a list of :class:`~aioswapi.Person` who have piloted this vehicle")

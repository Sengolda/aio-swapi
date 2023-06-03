from functools import lru_cache

__all__ = (
    "Person",
    "Planet",
    "Starship",
    "Film",
    "Vehicle",
)


class _Object:
    def __init__(self, raw_data: dict, *, http):
        self.raw_data = raw_data
        self.http = http
        for key, value in raw_data.items():
            if value in ("n/a", "none"):
                value = None

            setattr(self, key, value)


class Film(_Object):
    @lru_cache(maxsize=None)
    async def get_starships(self):
        starships = []
        for starship in self.starships:
            raw_data = await self.http.request(starship)
            starship.append(Starship(raw_data, http=self.http))
        self.starships = starships
        return starships

    @lru_cache(maxsize=None)
    async def get_characters(self):
        characters = []
        for character in self.characters:
            raw_data = await self.http.request(character)
            characters.append(Person(raw_data, http=self.http))
        self.characters = characters
        return characters

    @lru_cache(maxsize=None)
    async def get_vehicles(self):
        vehicles = []
        for vehicle in self.vehicle:
            raw_data = await self.http.request(vehicle)
            vehicles.append(Vehicle(raw_data, http=self.http))
        self.vehicles = vehicles
        return vehicles

    @lru_cache(maxsize=None)
    async def get_planets(self):
        planets = []
        for planet in self.planels:
            raw_data = await self.http.request(planet)
            planets.append(Planet(raw_data, http=self.http))
        self.planets = planets
        return planets

    @lru_cache(maxsize=None)
    async def get_species(self):
        species = []
        for specie in self.species:
            raw_data = await self.http.request(specie)
            species.append(Specie(raw_data, http=self.http))
        self.species = species
        return species


class Person(_Object):
    @lru_cache(maxsize=None)
    async def get_films(self):
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        self.films = films
        return films

    @lru_cache(maxsize=None)
    async def get_starships(self):
        starships = []
        for starship in self.starships:
            raw_data = await self.http.request(starship)
            starships.append(Starship(raw_data, http=self.http))
        self.starships = starships
        return starships

    @lru_cache(maxsize=None)
    async def get_homeworld(self):
        raw_data = await self.http.request(self.homeworld)
        self.homeworld = homeworld = Planet(raw_data, http=self.http)
        return homeworld

    @lru_cache(maxsize=None)
    async def get_species(self):
        species = []
        for specie in species:
            raw_data = await self.http.request(self.species)
            species.append(Specie(raw_data, http=self.http))
        return species


class Planet(_Object):
    @lru_cache(maxsize=None)
    async def get_residents(self):
        residents = []
        for resident in self.residents:
            raw_data = await self.http.request(resident)
            residents.append(Person(raw_data, http=self.http))
        return residents

    @lru_cache(maxsize=None)
    async def get_films(self):
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data))
        return films


class Specie:
    @lru_cache(maxsize=None)
    async def get_people(self):
        people = []
        for person in self.people:
            raw_data = await self.http.request(person)
            people.append(Person(raw_data, http=self.http))
        return people

    @lru_cache(maxsize=None)
    async def get_films(self):
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        return films


class Starship(_Object):
    @lru_cache(maxsize=None)
    async def get_pilots(self):
        pilots = []
        for pilot in self.pilots:
            raw_data = await self.http.request(pilot)
            pilots.append(Person(raw_data, http=self.http))
        return pilots

    @lru_cache(maxsize=None)
    async def get_films(self):
        films = []
        for film in self.films:
            raw_data = await self.http.request(film)
            films.append(Film(raw_data, http=self.http))
        return films


class Vehicle(Starship):
    pass

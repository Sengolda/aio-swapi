# aio-swapi

Simple async wrapper around the [swapi starwars API](https://swapi.dev/)

### Key Features
- Modern Pythonic API using `async`/`await`
- Covers all endpoints of the API

### Installing
Python 3.5.3 or higher is required due to the module using aiohttp

To install just run the following command:
```
# Linux/Macos
python3 -m pip install -U git+https://github.com/Sengolda/aio-swapi

# Windows
py -3 -m pip install -U git+https://github.com/Sengolda/aio-swapi
```

This lib is currently in the **Alpha** stage so some breaking changes may happen.

### Usage/Examples
Docs are not ready yet so here are a couple of examples

```python
from aioswapi import Client
import asyncio

async def main():
    async with Client() as c:
        result = await c.get_person(4)
        print(result.name)

asyncio.run(main())
```
Example for searching
```python
from aioswapi import Client
import asyncio

async def main():
    async with Client() as c:
        results = await c.search_people("skywalker")
        for person in results:
            print(person.name)

asyncio.run(main())
```

### Examples without context managers

```python
from aioswapi import Client
import asyncio

client = Client()
async def main():
    person = (await client.get_person(4)) # get person by id
    print(person.name)
    await client.close() # close the http client 
    # this is not required to do when using context managers

asyncio.run(main())
```

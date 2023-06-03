from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional, Union

import aiohttp
import pkginfo


BASE_URL = "https://swapi.dev/api"


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")

    if response.headers["content-type"] == "application/json":
        return json.loads(text)

    return text


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Swapi API"""

    def __init__(
        self,
    ) -> None:
        self.session: Optional[aiohttp.ClientSession] = None

        user_agent = "aio-swapi (https://github.com/Sengolda/aio-swapi) Python/{0[0]}.{0[1]} aiohttp/{1}"
        self.user_agent: str = user_agent.format(sys.version_info, aiohttp.__version__)

    async def request(self, route: str, params={}):
        if not self.session:
            self.session = aiohttp.ClientSession()
        url = BASE_URL + "/" + route
        if route.startswith("https://"):
            url = route

        headers: Dict[str, Any] = {aiohttp.hdrs.USER_AGENT: self.user_agent}
        data = None
        # Sometimes the API returns None for some reason 
        # so we have to wait until we actually have some data, this is not due to ratelimits.
        while not data:
            try:
                async with self.session.get(url, headers=headers, params=params) as response:
                    data = await json_or_text(response)
                    return data
            except aiohttp.ClientConnectionError:
                pass

    async def close(self):
        if not self.session.closed:
            await self.session.close()

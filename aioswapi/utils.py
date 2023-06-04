from typing import Dict, Any
import aiohttp
import json

async def json_or_text(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    text = await response.text(encoding="utf-8")

    if response.headers["content-type"] == "application/json":
        return json.loads(text)

    return text

def copy_doc(func_with_doc):
    def wrapper(func):
        func.__doc__ = getattr(func_with_doc, "__doc__", None)
        return func

    return wrapper

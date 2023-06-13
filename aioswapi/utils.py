from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Any, Callable, TypeVar

    T = TypeVar("T")

import json

import aiohttp


async def json_or_text(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    text = await response.text(encoding="utf-8")

    if response.headers["content-type"] == "application/json":
        return json.loads(text)

    return text


def copy_doc(func_with_doc: Callable[..., Any]) -> Callable[[T], T]:
    def wrapper(func: T) -> T:
        func.__doc__ = getattr(func_with_doc, "__doc__", None)
        return func

    return wrapper

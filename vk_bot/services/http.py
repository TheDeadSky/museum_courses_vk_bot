from typing import Mapping, SupportsInt, Sequence, Any

import aiohttp

ParamsMapping = Mapping[str, str | SupportsInt | float | Sequence[str | SupportsInt | float]]
ParamsSequence = Sequence[tuple[str, str | SupportsInt | float | Sequence[str | SupportsInt | float]]]

class HttpService:
    @staticmethod
    async def get(
        url: str,
        *,
        params: None | str | ParamsMapping | ParamsSequence = None,
        **kwargs
    ) -> aiohttp.ClientResponse:
        """
        Makes a GET request to the url.
        It supports all arguments of 'aiohttp.ClientSession.get'.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, **kwargs) as response:
                return response

    @staticmethod
    async def post(
        url: str,
        *,
        params: None | str | ParamsMapping | ParamsSequence = None,
        json: Any = None,
        **kwargs
    ):
        """
        Makes a POST request to the url.
        It supports all arguments of 'aiohttp.ClientSession.post'.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, params=params, json=json) as response:
                return response

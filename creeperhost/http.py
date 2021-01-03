from creeperhost.errors import Forbidden, HTTPException, NotFound, ServerError
import aiohttp
import asyncio
import logging
import json

from .client import Client


log = logging.getLogger(__name__)


async def json_or_text(response):
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['Content-Type'] == 'application/json':
            return json.loads(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text


class ApiRoute:
    BASE = "https://api.creeper.host"

    def __init__(self, verb: str, path: str):
        self.verb = verb
        self.path = path
    
    @property
    def url(self) -> str:
        """
        Returns the desired request route url
        """

        return self.BASE + self.path

    def __str__(self) -> str:
        """
        Returns the HTTP Verb associated with the request and
        the full request route url
        """

        return f"{self.verb} {self.url}"


class Http:
    def __init__(self, client: Client, apikey: str, apisecret: str):
        self.client = client
        self.__apikey = apikey
        self.__apisecret = apisecret
        self.__session = None

    async def __create_session(self) -> None:
        """
        Creates the aiohttp Client Session for the http client

        This has to be here to prevent aiohttp from screaming at us about session creation
        being outside of a coroutine
        """

        if self.__session is None:
            self.__session = aiohttp.ClientSession


    async def __request(self, route: ApiRoute, **kwargs) -> None:
        """
        Sends an HTTP request to the particular API Route specified
        """

        headers = {
            "Content-Type": "application/json",
            "apikey": self.__apikey,
            "apisecret": self.__apisecret
        }

        if "body" in kwargs:
            body=kwargs.pop("body")
        else:
            body = None
        
        for attempts in range(5):
            try:
                async with self.__session.request(route.verb, route.url, headers=headers, data=body) as response:
                    log.debug(f"{route}{f' with data {body}' if body is not None else ''} returned {response.status} ({response.reason})")

                    data = await json_or_text(response)
                
                if response.status == 429:
                    # we're being rate limitted
                    # as far as I know there really isn't any specified rate
                    # limits with the api so this just uses a generic exponential
                    # backoff calculation

                    retry_after = 1 + attempts * 2
                    log.warning(f"We've been rate limited. Retrying in {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                
                if 200 >= response.status < 300:
                    log.debug(f"{route} returned with data {data}")
                    return data
                
                if response.status == 403:
                    raise Forbidden

                if response.status == 404:
                    raise NotFound

                if response.status >= 500:
                    raise ServerError

                raise HTTPException
            except OSError as e:
                # connection reset by peer
                if attempts < 4 and e.errno in (54, 10054):
                    continue
                raise

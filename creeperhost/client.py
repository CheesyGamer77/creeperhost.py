import aiohttp
import asyncio

from .http import Http


class Client:
    def __init__(self, *, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.__session = None  # defined in self.__create_session

    async def __create_session(self) -> aiohttp.ClientSession:
        """
        Creates the aiohttp ClientSession for the client

        This has to be done otherwise aiohttp will scream at us saying that the client session
        was created outside of a coroutine
        """

        self.__session = aiohttp.ClientSession(self.loop)

    async def login(self, apikey: str, apisecret: str) -> None:
        """
        Creates the aiohttp ClientSession for the client
        """
        
        await self.__create_session()
        self.__http = Http(self, apikey, apisecret)

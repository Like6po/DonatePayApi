import asyncio
import json
import sys
from typing import Union, List

import aiohttp
from pydantic import ValidationError
from cachetools import TTLCache

from DonationPayApi.api import API
from DonationPayApi.models import User, Transaction, ListOfTransactions


class Client:
    def __init__(self, token, session=None, timeout=30, is_use_cache=True):
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.cache = TTLCache(9600, 180)
        self.session = session if session else aiohttp.ClientSession(loop=self.loop)
        self.headers = {'User-Agent': 'donatepayapi_tk (Python {0[0]}.{0[1]})'.format(sys.version_info)}
        self.is_use_cache = is_use_cache
        self.timeout = timeout
        self.api = API(token)

    async def close(self):
        return await self.session.close()

    def _resolve_cache(self, url):
        data = self.cache.get(url)
        if not data:
            return None
        return data

    async def _request_get(self, url, use_cache=None):

        """Async method to request a url"""
        if use_cache is None:
            use_cache = self.is_use_cache
        if use_cache:
            cache = self._resolve_cache(url)
        else:
            cache = None

        if cache is not None:
            return cache

        async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
            try:
                data = json.loads(await resp.text())
            except json.JSONDecodeError:
                data = await resp.text()
        self.cache[url] = data

        if data['status'] == 'success':
            return data['data']
        else:
            return data['message']

    async def _request_post(self, url, use_cache=None, data=None):

        """Async method to request a url"""
        if use_cache is None:
            use_cache = self.is_use_cache
        if use_cache:
            cache = self._resolve_cache(url)
        else:
            cache = None

        if cache is not None:
            return cache

        if not data:
            data = self.headers

        async with self.session.post(url, timeout=self.timeout, data=data) as resp:
            try:
                data = json.loads(await resp.text())
            except json.JSONDecodeError:
                data = await resp.text()
        self.cache[url] = data

        return data['message']

    async def get_user(self) -> Union[str, User, None]:
        url = self.api.USER
        data = await self._request_get(url)

        if isinstance(data, str):
            return data
        try:
            return User.parse_obj(data)
        except ValidationError as e:
            return f"Ошибка валидации {e}"

    async def get_transactions(self, **kwargs) -> Union[List[Transaction], str, None]:
        url = self.api.TRANSACTIONS
        url += f"&{'&'.join([f'{name}={value}' for name, value in kwargs.items()])}" if kwargs else ""
        data = await self._request_get(url)
        if isinstance(data, str):
            return data
        try:
            return ListOfTransactions(data)
        except ValidationError as e:
            return f"Ошибка валидации {e}"

    async def set_notification(self, **kwargs):
        url = self.api.NOTIFICATIONS
        kwargs.update({'access_token': self.token})
        data = await self._request_post(url, data=kwargs)
        return data
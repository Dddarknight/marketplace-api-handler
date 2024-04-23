from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from aiohttp import ClientSession

from src.config import get_settings
from src.consts import SECONDS_IN_MINUTE
from src.responses_schemas import OrderModel, SalesModel


class ApiAdapter:
    def __init__(self):
        self.config = get_settings()
        self.orders_url = self.config.marketplace_url + self.config.orders_path
        self.sales_url = self.config.marketplace_url + self.config.sales_path
        self.flag = 0
        self.headers = {'Authorization': f'ApiKey {self.config.api_key}'}

    @asynccontextmanager
    async def session(self):
        async with ClientSession(headers=self.headers) as session:
            yield session

    def get_date_from(self):
        """Gets the current server date."""
        return (datetime.now(tz=self.config.server_timezone) - timedelta(
            minutes=self.config.requests_periodicity / SECONDS_IN_MINUTE)).replace(tzinfo=None)

    async def get_data(self):
        """Gets the main business data."""
        orders_data = await self.get(self.orders_url)
        orders = [OrderModel(**order) for order in orders_data]
        sales_data = await self.get(self.sales_url)
        sales = [SalesModel(**sales_entry) for sales_entry in sales_data]
        return orders, sales

    async def get(self, path):
        """API request."""
        async with self.session() as session, session.get(
            path,
            params={'dateFrom': self.get_date_from().strftime('%Y-%m-%d %H:%M:%S'), 'flag': self.flag},
        ) as response:
            return await response.json()

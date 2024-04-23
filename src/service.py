from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database import AsyncSessionManager
from src.api import ApiAdapter
from src.config import Settings
from src.file_handler import FileHandler
from src.repository import Repository
from src.responses_schemas import OrderModel, SalesModel


class DataService:

    def __init__(self, session_factory: AsyncSessionManager, bot: Bot, config: Settings):
        self.session_factory = session_factory
        self.repository = Repository()
        self.file_handler = FileHandler()
        self.api_adapter = ApiAdapter()
        self.bot = bot
        self.report_file_name = 'report.xlsx'
        self.config = config

    async def process_data(self):
        """The main business flow: gets data from marketplace API -> saves to DB -> the sends report."""
        orders, sales = await self.api_adapter.get_data()
        async with self.session_factory() as session:
            await self.save_products(session=session, orders=orders)
            existing_orders = await self.repository.get_orders(session=session)
            await self.save_or_update_orders(session=session, orders=orders, existing_orders=existing_orders)
            await self.save_or_update_sales(session=session, sales=sales, existing_orders=existing_orders)
            await self.file_handler.save_to_excel(orders, sales, self.report_file_name)
            await self.bot.send_document(
                chat_id=self.config.chat_id,
                document=FSInputFile(self.report_file_name)
            )

    async def save_products(self, session: AsyncSession, orders: list[OrderModel]):
        """Checks if products already exist in the database and saves them."""
        existing_products = await self.repository.get_products(session=session)
        existing_products_ids = [product.nm_id for product in existing_products]
        new_products = []
        for order in orders:
            product = order.extract_product_data()
            if order.nm_id not in existing_products_ids and product not in new_products:
                new_products.append(product)
        await self.repository.insert_products(session=session, values=new_products)

    async def save_or_update_orders(
        self,
        session: AsyncSession,
        orders: list[OrderModel],
        existing_orders,
    ):
        """Checks if orders already exist in the database and saves or updates them."""
        orders_ids = {order.srid for order in existing_orders}
        orders_to_insert, orders_to_update = [], []
        for order in orders:
            data = order.to_orm_model()
            if order.srid not in orders_ids:
                orders_to_insert.append(data)
            else:
                orders_to_update.append(data)
        if orders_to_insert:
            await self.repository.insert_orders(session=session, values=orders_to_insert)
        if orders_to_update:
            await self.repository.update_orders(session=session, values=orders_to_update)

    async def save_or_update_sales(
        self,
        session: AsyncSession,
        sales: list[SalesModel],
        existing_orders,
    ):
        """Checks if sales already exist in the database and saves or updates them."""
        sales_ids = {
            sales.sale_id
            for order in existing_orders
            for sales in order.sales
        }
        sales_to_insert, sales_to_update = [], []
        for sales_item in sales:
            data = sales_item.to_orm_model()
            if sales_item.sale_id not in sales_ids:
                sales_to_insert.append(data)
            else:
                sales_to_update.append(data)
        if sales_to_insert:
            await self.repository.insert_sales(session=session, values=sales_to_insert)
        if sales_to_update:
            await self.repository.update_sales(session=session, values=sales_to_update)

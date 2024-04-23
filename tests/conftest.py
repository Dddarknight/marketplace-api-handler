import pytest_asyncio
from sqlalchemy import select

from src.db_models.orders import Orders, Sales
from src.db_models.products import Products


@pytest_asyncio.fixture()
async def assert_data(orders, sales):
    async def inner(session):
        stmt = select(Orders.srid)
        db_orders = (await session.execute(stmt)).all()
        assert {order.srid for order in db_orders} == {order.srid for order in orders}
        stmt = select(Sales.sale_id)
        db_sales = (await session.execute(stmt)).all()
        assert {sales_item.sale_id for sales_item in db_sales} == {sales_item.sale_id for sales_item in sales}
        stmt = select(Products.nm_id)
        db_products = (await session.execute(stmt)).all()
        assert {product.nm_id for product in db_products} == {order.nm_id for order in orders}
    return inner

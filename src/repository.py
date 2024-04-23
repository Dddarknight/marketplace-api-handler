from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from src.db_models.orders import Orders, Sales
from src.db_models.products import Products


class Repository:

    def __init__(self):
        super().__init__()

    async def get_orders(
        self,
        session: AsyncSession,
    ):
        """Gets orders."""
        stmt = (
            select(Orders)
            .join(Orders.sales)
            .options(contains_eager(Orders.sales))
        )
        return (await session.execute(stmt)).unique().scalars().all()

    async def get_products(
        self,
        session: AsyncSession,
    ):
        """Gets products."""
        stmt = select(Products)
        return (await session.execute(stmt)).unique().scalars().all()

    async def insert_products(
        self,
        session: AsyncSession,
        values: list[dict],
    ):
        """Creates products."""
        stmt = insert(Products).values(values)
        await session.execute(stmt)

    async def insert_orders(
        self,
        session: AsyncSession,
        values: list[dict],
    ):
        """Creates orders."""
        stmt = insert(Orders).values(values)
        await session.execute(stmt)

    async def update_orders(
        self,
        session: AsyncSession,
        values: list[dict],
    ):
        """Updates orders."""
        for value in values:
            stmt = update(Orders).values(value).where(Orders.srid == value['srid'])
            await session.execute(stmt)

    async def insert_sales(
        self,
        session: AsyncSession,
        values: list[dict],
    ):
        """Creates sales."""
        stmt = insert(Sales).values(values)
        await session.execute(stmt)

    async def update_sales(
        self,
        session: AsyncSession,
        values: list[dict],
    ):
        """Updates sales."""
        for value in values:
            stmt = update(Sales).values(value).where(Sales.sale_id == value['sale_id'])
            await session.execute(stmt)

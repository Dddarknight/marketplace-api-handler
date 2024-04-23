import json
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from src.adapters.database import Database
from src.responses_schemas import OrderModel, SalesModel
from src.service import DataService


@pytest.fixture()
def orders():
    with open('tests/fixtures/order.json') as f:
        orders_data = json.load(f)
        return [OrderModel(**orders_data)]


@pytest.fixture()
def sales():
    with open('tests/fixtures/sales.json') as f:
        sales_data = json.load(f)
        return [SalesModel(**sales_data)]


@pytest.fixture()
def fake_api(orders, sales):
    fake_api_adapter = AsyncMock()
    fake_api_adapter.get_data.return_value = orders, sales
    yield fake_api_adapter


@pytest_asyncio.fixture()
async def prepare(envs):
    test_db = Database(db_url=envs.database.test_url)
    await test_db.create_database()
    fake_bot = AsyncMock()

    async def fake_send_document(chat_id, document):
        pass

    fake_bot.send_document = fake_send_document
    yield test_db, DataService(test_db.async_session, fake_bot, envs)
    await test_db.drop_database()


@pytest.mark.asyncio()
async def test_process_data(
    prepare,
    fake_api,
    assert_data,
):
    test_db, service = prepare
    service.api_adapter = fake_api
    await service.process_data()
    async with test_db.async_session() as session:
        await assert_data(session)

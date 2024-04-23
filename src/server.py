import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from functools import partial
from logging import Logger

from aiohttp import web

from src.config import get_settings, Settings
from src.adapters.database import Database
from src.logger import setup_logging
from src.service import DataService


async def make_requests(service: DataService, logger: Logger, config: Settings):
    while True:
        try:
            await service.process_data()
        except Exception as e:
            logger.error(f'Error fetching data {str(e)}')
        await asyncio.sleep(config.requests_periodicity)


async def start_background_tasks(app, service: DataService, logger: Logger, config: Settings):
    if 'tasks' not in app:
        app['tasks'] = asyncio.create_task(make_requests(service, logger, config))
    else:
        logger.info("Background task already running.")


async def cleanup_background_tasks(app):
    app['tasks'].cancel()
    await app['tasks']


async def init_db(app, db: Database):
    await db.create_database()


async def bot_polling(app, dp, bot) -> None:
    await dp.start_polling(bot)


async def start_bot_and_tasks(
    app,
    dp: Dispatcher,
    service: DataService,
    logger: Logger,
    config: Settings,
    bot: Bot,
):
    asyncio.create_task(dp.start_polling(bot))
    await start_background_tasks(app, service, logger, config)


def main():
    logger = setup_logging()
    config = get_settings()
    db = Database(config.database.url)

    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    service = DataService(db.async_session, bot, config)

    app = web.Application()

    app.on_startup.append(partial(init_db, db=db))
    app.on_startup.append(partial(
        start_bot_and_tasks, dp=dp, service=service, logger=logger, config=config, bot=bot))
    app.on_cleanup.append(cleanup_background_tasks)

    web.run_app(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()

from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseConfig(BaseSettings):
    url: str = Field(validation_alias='DATABASE_URL')
    test_url: str = Field(validation_alias='DATABASE_TEST_URL')


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    server_timezone: ZoneInfo = Field(default=ZoneInfo('Europe/Moscow'))
    requests_periodicity: int = Field(default=1800, validation_alias='REQUESTS_PERIODICITY')
    bot_token: str = Field(validation_alias='TG_API_TOKEN')
    marketplace_url: str = Field(validation_alias='MARKETPLACE_URL')
    orders_path: str = Field(validation_alias='ORDERS_PATH')
    sales_path: str = Field(validation_alias='SALES_PATH')
    api_key: str = Field(validation_alias='API_KEY')
    chat_id: int = Field(validation_alias='CHAT_ID')


def get_settings():
    return Settings()

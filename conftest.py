import sys
import os
import pytest

from src.config import Settings
from dotenv import load_dotenv


load_dotenv()
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='session')
def envs():
    return Settings()

from typing import Any, AsyncGenerator

import nest_asyncio
import pytest
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import AsyncClient
# from tortoise import Tortoise
# from tortoise.contrib.test import finalizer, initializer
from redis.asyncio import ConnectionPool
from sqlalchemy.engine import create_engine

from yummy_pizza_api_service.db.config import database
from yummy_pizza_api_service.db.utils import create_database, drop_database
from yummy_pizza_api_service.services.redis.dependency import get_redis_pool
from yummy_pizza_api_service.settings import settings
from yummy_pizza_api_service.web.application import get_app

nest_asyncio.apply()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Create models and databases.

    :yield: new engine.
    """
    from yummy_pizza_api_service.db.meta import meta  # noqa: WPS433
    from yummy_pizza_api_service.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    create_database()

    engine = create_engine(str(settings.db_url))
    with engine.begin() as conn:
        meta.create_all(conn)

    engine.dispose()

    await database.connect()

    yield

    await database.disconnect()
    drop_database()


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
def fastapi_app(fake_redis_pool: ConnectionPool) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

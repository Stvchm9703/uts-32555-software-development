import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("create_dummy_model")
    test_object = {
        'name': "pizza-a",
        'description' : 'pizza description',
        'item_type' : 'single',
        'category': 'pizza,chicken',
        'kal': 1000.2,
        'price_value': 1.23,
        'rate': 0.015
    }
    response = await client.put(
        url,
        json=test_object,
    )
    assert response.status_code == status.HTTP_200_OK
    dao = ProductDAO()
    instances = await dao.filter(name=test_object['name'])
    assert instances[0] == test_object

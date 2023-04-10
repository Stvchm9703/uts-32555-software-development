import uuid

import pytest
import unittest
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
    url = fastapi_app.url_path_for("create_product_model")
    test_object = {
        'name': "pizza-a",
        'description': 'pizza description',
        'item_type': 'single',
        'category': 'pizza,chicken',
        'kal': 1000.2,
        'price_value': 1.23,
        'rate': 0.015
    }
    response = await client.post(url, json=test_object)
    assert response.status_code == status.HTTP_200_OK
    dao = ProductDAO()
    instances = await dao.filter(keyword=test_object['name'])
    assert instances[0].name == test_object['name']
    assert instances[0].description == test_object['description']
    assert instances[0].item_type == test_object['item_type']
    

@pytest.mark.anyio
async def test_creation_with_option(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("create_product_model")
    test_object = {
        'name': "pizza-b",
        'description': 'suprema pizza, with extra meat',
        'item_type': 'single',
        'category': 'pizza,chicken',
        'kal': 1000.2,
        'price_value': 1.23,
        'rate': 0.015,
        'options': [
            {
                'name': 'pizza saurce',
                'description': 'pizza size',
                'extra_charge': 1.2,
                'option_kind': 'favour',
                'kal': 120,
                'option_sets': ['tomato sauce', 'BBQ sauce']
            },
            {
                'name': 'pizza size',
                'description': 'pizza size',
                'extra_charge': 1.2,
                'option_kind': 'size',
                'max_count': 2,
                'min_count': -1,
                'kal': 120,
                'option_sets': ['small (8 Inch)', 'Large (11 Inch)', 'Extra Large (12 Inch)']
            },
            {
                'name': 'pizza chilli souce',
                'description': 'pizza chili souce, it can be extra, or just remove',
                'extra_charge': 0,
                'option_kind': 'extra_or_reduce',
                'max_count': 1,
                'min_count': -1,
                'kal': 30
            },
            {
                'name': 'chicken meat amount',
                'description': 'chicken meat on top of pizza, it can be extra with numbers of 100 grams.',
                'extra_charge': 1.25,
                'option_kind': 'number_count',
                'max_count': 5,
                'min_count': 0,
                'kal': 130
            },
            # {
            #     'name': 'pizza favour',
            #     'description': '',
            #     'option_kind': 'favour',
            #     'max_count': 5,
            #     'min_count': 0,
            #     'kal': 130,
            #     'option_sets': ['supreme','sausage sizzle', 'Hawaiian', 'chicken','veggie lovers']
            # },
        ]
    }
    print(url)
    response = await client.post(url, json=test_object)
    assert response.status_code == status.HTTP_200_OK
    dao = ProductDAO()
    instances = await dao.filter(keyword=test_object['name'])
    assert instances[0].name == test_object['name']
    assert len(instances[0].options) == len(test_object['options'])


import json
import pytest
import unittest

from typing import List
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from yummy_pizza_api_service.web.api.order.schema import OrderInputDTO
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.product_option_model import ProductOption
from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.dao.order_dao import OrderDAO
from yummy_pizza_api_service.db.models.order_model import OrderType, OrderStatus, OrderDeliveryType


async def prebuild_products() -> List[Product]:
    dao = ProductDAO()
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
        ]
    }
    await dao.create(test_object)
    return await dao.filter(keyword=test_object['name'], limit=1)
   

@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("create_order")
    test_object = {
        'contact_type': "walk_in",
        'deliver_type': 'dine_in',
        'customer_name': 'Albert K',
        'customer_contact': 435623453,
        'customer_address': 'NSW 2070, St John st',
        'staff': 'steve'
    }
    response = await client.post(url, json=test_object)
    assert response.status_code == status.HTTP_200_OK
    print(response)
    dao = OrderDAO()
    instances = await dao.filter(customer_contact=435623453)
    print(instances)
    assert instances[0].contact_type == OrderType.walk_in.value
    assert instances[0].deliver_type == OrderDeliveryType.dine_in.value
    assert instances[0].status == OrderStatus.created.value
    assert instances[0].customer_name == test_object['customer_name']
    assert instances[0].customer_contact == test_object['customer_contact']
    assert instances[0].customer_address == test_object['customer_address']
    assert instances[0].staff == test_object['staff']


@pytest.mark.anyio
async def test_cancel(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("cancel_order")
    test_object = {
        'contact_type': "walk_in",
        'deliver_type': 'dine_in',
        'customer_name': 'Albert.K',
        'customer_contact': 435623453,
        'customer_address': 'NSW 2070, St John st',
        'staff': 'steve',
    }
    dao = OrderDAO()
    await dao.create(**test_object)
    instances = await dao.filter(keyword=test_object['customer_name'])
    inst_obj = instances[0]

    response = await client.post(url, json={**inst_obj.dict()})
    assert response.status_code == status.HTTP_200_OK
    result = await dao.filter(id=inst_obj.id)
    assert result[0].status == OrderStatus.void.value


@pytest.mark.anyio
async def test_add_item(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    

    """Tests product instance creation."""
    url = fastapi_app.url_path_for("add_item")

    test_object = {
        'contact_type': OrderType.phone_in.value,
        'deliver_type': 'dine_in',
        'customer_name': 'Albert.K',
        'customer_contact': 435623453,
        'customer_address': 'NSW 2070, St John st',
        'staff': 'steve',
    }
    system_resp = await client.post(fastapi_app.url_path_for("create_order"), json=test_object)
    resp_dt = system_resp.json()
    print(system_resp)
    product_list = await prebuild_products()
    response = await client.post(url, json={
        'id': resp_dt['id'],
        'product': {
            'id': product_list[0].id
        },
        'extra_options' : [
            {
                'id' : product_list[0].options[0].id,
                'option': 'tomato sauce'
            }
        ],
        'quality': 1
    })
    assert response.status_code == status.HTTP_200_OK

    dao = OrderDAO()
    instances = await dao.filter(id=resp_dt['id'])
    inst_obj = instances[0]

    # assert inst_obj.items = 

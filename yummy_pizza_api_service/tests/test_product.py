import uuid
import json
import pytest
import unittest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from yummy_pizza_api_service.web.api.product.schema import ProductModelInputDTO
# from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.product_option_model import ProductOption
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
        ]
    }
    response = await client.post(url, json=test_object)
    assert response.status_code == status.HTTP_200_OK
    dao = ProductDAO()
    instances = await dao.filter(keyword=test_object['name'])
    instance_set = await instances[0].load_all()
    assert instance_set.name == test_object['name']
    assert len(instance_set.options) == len(test_object['options'])


@pytest.mark.anyio
async def test_update(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("update_product_model")
    test_object = {
        'name': "pizza-a",
        'description': 'pizza description',
        'item_type': 'single',
        'category': 'pizza,chicken',
        'kal': 1000.2,
        'price_value': 1.23,
        'rate': 0.015
    }
    dao = ProductDAO()
    await dao.create(test_object)
    stored_object = await dao.filter(keyword=test_object['name'], limit=1)
    stored_object_s = json.loads(stored_object[0].json())
    # print(stored_object_s)
    test_updated_obj = {
        **stored_object_s,
        'name': 'pizza-bb',
        'description': 'new pizza description',
    }
    k = ProductModelInputDTO(**test_updated_obj)

    response = await client.post(url, json=k.dict())
    assert response.status_code == status.HTTP_200_OK
    instances = await dao.get(id=stored_object[0].id)
    assert instances.id == stored_object[0].id
    assert instances.name == test_updated_obj['name']
    assert instances.description == test_updated_obj['description']


@pytest.mark.anyio
async def test_update_with_option(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests product instance creation."""
    url = fastapi_app.url_path_for("update_product_model")
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
    dao = ProductDAO()
    await dao.create(test_object)
    stored_object_set = await dao.filter(keyword=test_object['name'], limit=1)
    stored_object = stored_object_set[0]
    test_updated_obj_option = []
    for index, item in enumerate(stored_object.options):
        new_item = item.dict()
        if index % 2 == 0:
            new_item['name'] = '{} - (mod 2)'.format(new_item['name'])
        del new_item['created_date']
        del new_item['updated_date']

        test_updated_obj_option.append(new_item)

    test_updated_obj_option.append({
        'name': 'extra smile',
        'description': 'Happy smile.',
        'extra_charge': 0,
        'option_kind': 'extra_or_reduce',
    })
    # print(test_updated_obj_option)
    stored_object.name = 'pizza-bb'
    stored_object.description = 'new pizza description'
    ll = {
        **stored_object.dict(), 'options': test_updated_obj_option
    }
    k = ProductModelInputDTO(**ll)
    response = await client.post(url, json=k.dict())
    assert response.status_code == status.HTTP_200_OK
    instances = await dao.get(id=stored_object.id)
    assert instances.id == stored_object.id
    assert instances.name == stored_object.name
    assert instances.description == stored_object.description
    # last ok
    instances = await instances.load_all()
    
    assert len(instances.options) == len(test_updated_obj_option)
    for index, opt_item in enumerate(instances.options):
        assert opt_item.name == test_updated_obj_option[index]['name']

@pytest.mark.anyio
async def test_deletion(
    fastapi_app: FastAPI,
    client: AsyncClient,
):
    url = fastapi_app.url_path_for("delete_product_model")
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
    dao = ProductDAO()
    await dao.create(test_object)
    stored_object_set = await dao.filter(keyword=test_object['name'], limit=1)
    stored_object = stored_object_set[0]

    response = await client.post(url, json={"id": stored_object.id})
    assert response.status_code == status.HTTP_200_OK
    
    instances = await dao.get(id=stored_object.id)
    assert instances == None or instances == []
    instances_opts = await ProductOption.objects.filter(option_for_product=stored_object.id).all()
    assert instances_opts == None or instances_opts == []
    pass
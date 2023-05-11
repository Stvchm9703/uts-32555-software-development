from typing import List, Optional, Union
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind
import json


class ProductDAO:
    """Class for accessing product table."""

    async def create(
            self,
            product: dict
    ) -> None:
        """
        ### Create product with data. ###
        :param product : `Product` / `dict`

        create product by provided product-like object
        """
        if 'options' in product and product['options'] != None:
            new_product_options = []
            for item in product['options']:
                prof_option = ProductOption(**item)
                new_product_options.append(prof_option)
            # print(new_product_options)
            new_product = Product(**{**product, 'options': new_product_options})
            await new_product.save_related(follow=True, save_all=True)
        else:
            new_product = Product(**product)
            await new_product.save_related(follow=True, save_all=True)
        return

    async def get(self, id=int) -> Optional[Product]:
        """
        ### Get product by product id. ###
        :param id : record's id
        :return: product models (`Product` or `None`).

        get products by id
        """
        return await Product.objects.select_all(follow=True).get_or_none(id=id)

    async def get_all_products(self, limit: int = 15, offset: int = 0) -> List[Product]:
        """
        ### Get all product. ###
        :param limit : limit the records result in a number
        :param offset : skip a offset row count for the records
        :return: product models (`List[Product]`).

        get all products (with a paganation)
        """
        return await Product.objects\
            .select_all()\
            .limit(limit)\
            .offset(offset)\
            .all()

    async def filter(
        self,
        limit: int = 15,
        offset: int = 0,
        **search_query
    ) -> List[Product]:
        """
        ### Get specific product models. ###
        Filters products based on the given search query and returns a list of products.

        :param limit: The maximum number of products to return. Default is 15.
        :type limit: int
        :param offset: The number of products to offset the start of the returned list. Default is 0.
        :type offset: int
        :param search_query: A dictionary containing the search parameters.
        :type search_query: dict
            - `keyword` (str): A string to search for in the product name or description.
            - `prod_type` (str): The product type to filter by.
            - `price_max_range` (float): The maximum product price value.
            - `price_min_range` (float): The minimum product price value.
        :return: A list of Product objects based on the search query.
        :rtype: List[Product]


        filter with provided params
        """

        query = Product.objects.select_all(follow=True)
        if 'id' in search_query:
            query = query.filter(
                Product.id == (search_query['id'])
            )
        if 'keyword' in search_query:
            # query = query.filter(ProductModel.name == keyword)
            query = query.filter(
                Product.name.icontains(search_query['keyword'])
                | Product.description.icontains(search_query['keyword'])
            )
        if 'prod_type' in search_query:
            query = query.filter(
                Product.item_type == search_query['prod_type']
            )
        if 'price_max_range' in search_query:
            query = query.filter(
                Product.price_value <= search_query['price_max_range']
            )
        if 'price_min_range' in search_query:
            query = query.filter(
                Product.price_value >= search_query['price_min_range']
            )

        return await query.limit(limit).offset(offset).all()

    async def update(self, product: Product) -> Optional[Product]:
        """
        Updates a product in the database with the given product object. Returns the updated product
        if successful, or None if the product with the given ID does not exist in the database.

        :param product: The product object with updated properties.
        :type product: Product

        :return: The updated product object if successful, or None if the product with
            the given ID does not exist in the database.
        :rtype: Optional[Product]
        """
        tar = await Product.objects.select_all(follow=True).get(id=product.id)
        if tar:
            await tar.update(**(product.dict()))
            print('here')
            for item in product.options:
                await ProductOption.objects.update_or_create(**(item.dict()), option_for_product=tar)
            return tar
        return None

    async def delete(self, product: Product) -> Optional[int]:
        """
        delete product

        :params product: Product like object

        """
        tar = await Product.objects.select_all(follow=True).get(id=product.id)
        if tar:
            tar_id = tar.id
            # await ProductOption.objects.delete(option_for_product=tar)
            await tar.options.clear(keep_reversed=False)
            await tar.delete()
            return tar_id
        return None

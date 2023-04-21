from typing import List, Optional, Union
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind
import json


class ProductDAO:
    """Class for accessing product table."""

    async def create(
            self,
            product: Union[Product, dict]
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

    async def get(self, id=int) -> Product:
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
        keyword: str = None,
        prod_type: ProductType = None,
        price_max_range: float = None,
        price_min_range: float = None,
        limit: int = 15,
        offset: int = 0
    ) -> List[Product]:
        """
        ### Get specific product models. ###
        :param keyword: search with any name or description of product instance.
        :param prod_type: search with specific item-type, see also : `ProductType`
        :param price_max_range : search with maximium cap of price
        :param price_min_range : search with minimium cap of price
        :param limit : limit the records result in a number
        :param offset : skip a offset row count for the records
        :return: product models (`List[Product]`).

        filter with provided params
        """
        query = Product.objects.select_all(follow=True)
        if keyword:
            # query = query.filter(ProductModel.name == keyword)
            query = query.filter(
                Product.name.contains(keyword)
                | Product.description.contains(keyword)
            )
        if prod_type:
            query = query.filter(
                Product.item_type == prod_type.value
            )
        if price_max_range:
            query = query.filter(
                Product.price_value <= price_max_range
            )
        if price_min_range:
            query = query.filter(
                Product.price_value >= price_min_range
            )

        return await query.limit(limit).offset(offset).all()

    async def update(self, product: Product) -> None:
        tar = await Product.objects.select_all(follow=True).get(id=product.id)
        if tar:
            await tar.update(**(product.dict()))
            print('here')
            for item in product.options:
                await ProductOption.objects.update_or_create(**(item.dict()), option_for_product=tar)
            return tar.id
        return None

    async def delete(self, product: Product) -> None:
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

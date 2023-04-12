from typing import List, Optional, Union
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind
import json


class ProductDAO:
    """Class for accessing dummy table."""

    async def create(
            self,
            product: Union[Product, dict]
    ) -> None:
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
        return await Product.objects.select_all(follow=True).get_or_none(id=id)

    async def get_all_products(self, limit: int = 15, offset: int = 0) -> List[Product]:
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
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
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
        print(tar.json())
        if tar:
            await tar.update(**(product.dict()))
            print('here')
            for item in product.options:
                await ProductOption.objects.update_or_create(**(item.dict()), option_for_product=tar)

        pass

    async def delete(self, product: Product) -> None:
        tar = await Product.objects.get(id=product.id)
        if tar:
            await tar.delete()

from typing import List, Optional
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind


class ProductDAO:
    """Class for accessing dummy table."""

    async def create(
            self,
            product: Product
    ) -> None:
        new_product = Product(**product)
        await new_product.save_related(follow=True, save_all=True)
        return

    async def create_option(
        self,
        name: str,
        description: str,
        extra_charge: float,
        option_kind: ProductOptionKind,
        max_count: int,
        min_count: int,
        kal: float,
        related_prod: Product = None
    ):
        if related_prod is not None:
            await ProductOption.objects.create(
                name,
                description,
                extra_charge,
                max_count,
                min_count,
                kal,
                option_kind=option_kind.value,
                option_for_product=related_prod
            )
            return
        await ProductOption.objects.create(
            name,
            description,
            extra_charge,
            max_count,
            min_count,
            kal,
            option_kind=option_kind.value,
        )
        return

    async def get_all_products(self, limit: int = 15, offset: int = 0) -> List[Product]:

        return await Product.objects\
            .limit(limit)\
            .offset(offset)\
            .all()

    async def filter(
        self,
        keyword: str = None,
        prod_type: ProductType = None,
        price_max_range: float = None,
        price_min_range: float = None,
        limit: int = 15, offset: int = 0
    ) -> List[Product]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = Product.objects
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
        tar = await Product.objects.get(product)
        if tar:
            await product.save_related(follow=True)
        pass

    async def delete(self, product: Product) -> None:
        tar = await Product.objects.get(**product)
        if tar:
            await tar.delete()

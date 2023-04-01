from typing import List, Optional
from yummy_pizza_api_service.db.models.product_model import ProductModel, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOptionModel, ProductOptionKind


class ProductDAO:
    """Class for accessing dummy table."""

    async def create(
            self,
            product: ProductModel
    ) -> None:
        new_product = ProductModel(**product)
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
        related_prod: ProductModel = None
    ):
        if related_prod is not None:
            await ProductOptionModel.objects.create(
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
        await ProductOptionModel.objects.create(
            name,
            description,
            extra_charge,
            max_count,
            min_count,
            kal,
            option_kind=option_kind.value,
        )
        return

    async def get_all_products(self, limit: int = 15, offset: int = 0) -> List[ProductModel]:

        return await ProductModel.objects\
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
    ) -> List[ProductModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = ProductModel.objects
        if keyword:
            # query = query.filter(ProductModel.name == keyword)
            query = query.filter(
                ProductModel.name.contains(keyword)
                | ProductModel.description.contains(keyword)
            )
        if prod_type:
            query = query.filter(
                ProductModel.item_type == prod_type.value
            )
        if price_max_range:
            query = query.filter(
                ProductModel.price_value <= price_max_range
            )
        if price_min_range:
            query = query.filter(
                ProductModel.price_value >= price_min_range
            )

        return await query.limit(limit).offset(offset).all()

    async def update(self, product: ProductModel) -> None:
        tar = await ProductModel.objects.get(product)
        if tar:
            await product.save_related(follow=True)
        pass

    async def delete(self, product: ProductModel) -> None:
        tar = await ProductModel.objects.get(**product)
        if tar:
            await tar.delete()

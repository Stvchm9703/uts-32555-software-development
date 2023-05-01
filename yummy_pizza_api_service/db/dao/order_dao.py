from typing import List, Optional, Union
from yummy_pizza_api_service.db.models.order_model import Order, OrderType, OrderStatus, OrderDeliveryType
from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from yummy_pizza_api_service.db.models.order_product_option_model import OrderProductOption
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind
import json


class OrderDAO:
    """Class for accessing dummy table."""

    async def create(
            self,
            order: dict
    ) -> None:
        # if 'options' in product and product['options'] != None:
        #     new_product_options = []
        #     for item in product['options']:
        #         prof_option = ProductOption(**item)
        #         new_product_options.append(prof_option)
        #     # print(new_product_options)
        #     new_product = Product(**{**product, 'options': new_product_options})
        #     await new_product.save_related(follow=True, save_all=True)
        # else:
        #     new_product = Product(**product)
        #     await new_product.save_related(follow=True, save_all=True)

        new_order = Order(**order)
        await new_order.save_related(follow=True, save_all=True)
        return

    async def get(self, id=int) -> Order:
        return await Order.objects.select_all(follow=True).get_or_none(id=id)
        return

    async def get_latest_order(self, limit: int = 15, offset: int = 0) -> List[Order]:
        return await Order.objects\
            .select_all()\
            .order_by("-created_date")\
            .limit(limit)\
            .offset(offset)\
            .all()

    async def filter(
        self,
        query: dict = {},
        limit: int = 15,
        offset: int = 0
    ) -> List[Order]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = Order.objects.select_all(follow=True)
        if 'id' in query:
            query = query.filter(
                Order.id == (query['id'])
            )
        if 'keyword' in query:
            # query = query.filter(ProductModel.name == keyword)
            query = query.filter(
                Order.customer_name.contains(query['keyword'])
                | Order.customer_address.contains(query['keyword'])
            )
        if 'staff' in query:
            query = query.filter(
                Order.customer_name.contains(query['staff'])
            )
        if 'customer_contact' in query:
            query = query.filter(
                Order.customer_contact.contains(query['customer_contact'])
            )
        if 'order_number' in query:
            query = query.filter(
                Order.order_number == query['order_number']
            )
        if 'status' in query:
            query = query.filter(
                Order.status == query['status']
            )

        return await query.limit(limit).offset(offset).all()

    async def update(self, order: Order) -> None:
        # tar = await Product.objects.select_all(follow=True).get(id=product.id)
        # if tar:
        #     await tar.update(**(product.dict()))
        #     for item in product.options:
        #         await ProductOption.objects.update_or_create(**(item.dict()), option_for_product=tar)
        #     return tar.id
        return None

    async def delete(self, order: Order) -> None:
        # tar = await Product.objects.select_all(follow=True).get(id=product.id)
        # if tar:
        #     tar_id = tar.id
        #     # await ProductOption.objects.delete(option_for_product=tar)
        #     await tar.options.clear(keep_reversed=False)
        #     await tar.delete()
        #     return tar_id
        return None

    async def delete_by_id(self, order_id: int) -> None:
        # tar = await Product.objects.select_all(follow=True).get(id=product.id)
        # if tar:
        #     tar_id = tar.id
        #     # await ProductOption.objects.delete(option_for_product=tar)
        #     await tar.options.clear(keep_reversed=False)
        #     await tar.delete()
        #     return tar_id
        return None

    async def add_item(self, order: Order, new_products: OrderProduct) -> Order:
        return None

    async def remove_item(self):
        return None

    async def update_item(self, order: Order, tar_item: OrderProduct):
        return None

from typing import List, Optional, Union
from yummy_pizza_api_service.db.models.order_model import Order, OrderType, OrderStatus, OrderDeliveryType
from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from yummy_pizza_api_service.db.models.order_product_option_model import OrderProductOption
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.product_option_model import ProductOption, ProductOptionKind
import json
import ormar
from datetime import datetime


class OrderDAO:

    async def create(
            self,
            order: dict
    ) -> Order:
        """
        Create a new order in the database.

        :param order: The order to create.
        :type order: dict
        :return: Order
        :rtype: Order
        """
        latest_order = await Order.objects.order_by("-order_number").get_or_none()
        order_num = 1
        if latest_order != None and latest_order.order_number != 999:
            order_num = latest_order.order_number + 1

        deliver_type = OrderDeliveryType.dine_in.value
        if order['deliver_type'] != None and order['deliver_type'] in OrderDeliveryType._value2member_map_:
            deliver_type = order['deliver_type']

        return await Order.objects.create(**{
            **order,
            'deliver_type': deliver_type,
            'order_number': order_num,
            'status': OrderStatus.created.value
        })

    async def get(self, id=int) -> Optional[Order]:
        return await Order.objects.select_all(follow=True).get_or_none(id=id)

    async def get_latest_order(self, limit: int = 15, offset: int = 0) -> List[Order]:
        """
        Retrieve an Order object by its id.

        :param id: The id of the Order object to retrieve.
        :type id: int

        :return: The Order object with the given id, or None if it does not exist.
        :rtype: Optional[Order]
        """
        return await Order.objects\
            .select_all()\
            .order_by("-created_date")\
            .limit(limit)\
            .offset(offset)\
            .all()

    async def filter(
        self,
        limit: int = 15,
        offset: int = 0,
        **search_query
    ) -> List[Order]:
        """
        Filters Order objects based on the provided search query.

        :param limit: The maximum number of objects to return. Defaults to 15.
        :type limit: int
        :param offset: The number of objects to skip before starting to return them. Defaults to 0.
        :type offset: int
        :param search_query: A dictionary containing the search parameters. Can include any of the following keys:
            - id (int): The ID of the order.
            - keyword (str): A search string to match against the customer name or address.
            - staff (str): The name of the staff member associated with the order.
            - customer_contact (str): The contact information of the customer.
            - order_number (str): The order number.
            - status (str): The status of the order.
        :type search_query: dict
        :return: A list of Order objects that match the search query.
        :rtype: List[Order]
        """
        query = Order.objects.select_all(follow=True)
        if 'id' in search_query:
            query = query.filter(
                Order.id == (search_query['id'])
            )
        if 'keyword' in search_query:
            # query = query.filter(ProductModel.name == keyword)
            query = query.filter(
                Order.customer_name.icontains(search_query['keyword'])
                | Order.customer_address.icontains(search_query['keyword'])
            )
        if 'staff' in search_query:
            query = query.filter(
                Order.staff.icontains(search_query['staff'])
            )
        if 'customer_contact' in search_query:
            query = query.filter(
                Order.customer_contact == search_query['customer_contact']
            )
        if 'order_number' in search_query:
            query = query.filter(
                Order.order_number == search_query['order_number']
            )
        if 'status' in search_query:
            query = query.filter(
                Order.status.icontains(search_query['status'])
            )

        kk = await query.limit(limit).offset(offset).all()
        return kk

    async def update(self, inupdated_order: Order) -> None:
        """
        Updates the database with the given order information.

        :param order: The order object to update the database with.
        :type order: Order

        :returns: None
        """
        tar = await Order.objects.get_or_none.get(id=inupdated_order.id)
        if tar:
            await tar.update(**(inupdated_order.dict()))
            for item in inupdated_order.items:
                await OrderProduct.objects.update_or_create(**(item.dict()), for_order=tar)
            return tar.id
        return None

    async def delete(self, order: Order) -> Optional[int]:
        """
        Deletes an order and returns its ID if it exists, otherwise returns None.

        :param order: The order to be deleted.
        :type order: Order
        :return: The ID of the deleted order, or None if the order does not exist.
        :rtype: Optional[int]
        """
        tar = await Order.objects.get_or_none(id=order.id)
        if tar:
            tar_id = tar.id
            await tar.load_all()
            await tar.items.clear(keep_reversed=False)
            await tar.delete()
            return tar_id
        return None

    async def delete_by_id(self, order_id: int) -> Optional[int]:
        """
        Deletes an order by its ID.

        :param order_id: the ID of the order to delete.
        :type order_id: int
        :return: the ID of the deleted order or None if the order doesn't exist.
        :rtype: Optional[int]
        """
        tar = await Order.objects.select_all(follow=True).get_or_none(id=order_id)
        if tar:
            tar_id = tar.id
            await tar.load_all()
            await tar.items.clear(keep_reversed=False)
            await tar.delete()
            return tar_id
        return None

    async def void_order(self, order_id: int) -> Optional[Order]:
        """
        Void the order with the given ID and return it if it exists.

        :param order_id: An integer representing the ID of the order to be voided.
        :return: An instance of Order representing the voided order, or None if the order doesn't exist.
        """
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if (tar.status != OrderStatus.void.value
                and tar.status != OrderStatus.completed.value
                    and tar.status != OrderStatus.delivering.value):
                await tar.update_status(OrderStatus.void)

        return tar

    async def confirm_order(self, order_id: int) -> Optional[Order]:
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if tar.status == OrderStatus.created.value:
                await tar.update_status(OrderStatus.unpaid)
                # start payment
                await tar.request_payment()
            await tar.load_all(follow=True)
            # await tar.update()
        return tar

    async def request_payment_order(self, order_id: int) -> Optional[Order]:
        """

        """
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if tar.status == OrderStatus.unpaid.value:
                await tar.update_status(OrderStatus.paid)
            await tar.load_all(follow=True)
            # await tar.update()
        return tar

    async def producing_order(self, order_id: int) -> Optional[Order]:
        """

        """
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if tar.status == OrderStatus.paid.value:
                await tar.update_status(OrderStatus.producing)
                # 
            await tar.load_all(follow=True)
            # await tar.update()
        return tar


    async def sending_order(self, order_id: int) -> Optional[Order]:
        """

        """
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if tar.status == OrderStatus.producing.value:
                await tar.update_status(OrderStatus.delivering)
                # 
            await tar.load_all(follow=True)
            # await tar.update()
        return tar
    

    async def complete_order(self, order_id: int) -> Optional[Order]:
        """

        """
        tar = await Order.objects.get_or_none(id=order_id)
        if tar:
            if tar.status == OrderStatus.delivering.value:
                await tar.update_status(OrderStatus.completed)
            # start payment
            # await tar.request_payment()
            await tar.load_all(follow=True)
            # await tar.update()
        return tar

    """
    # item related
    """

    async def add_item(self, base_order: dict, input_order_option: dict) -> Order:
        """
        Add an item to an existing order.

        :param base_order: the existing order to add the item to
        :type base_order: Order
        :param input_order_option: the item to add to the order
        :type input_order_option: OrderProduct
        :return: the updated order with the added item
        :rtype: Order
        :raises: Exception if the provided base_order does not exist
        """
        existed = None
        if 'id' in base_order:
            existed = await Order.objects.get_or_none(id=base_order['id'])
        elif 'order_number' in base_order:
            existed = await Order.objects.get_or_none(order_number=base_order['order_number'])

        if existed is None:
            raise "request order is not single one"  # type: ignore

        existed_prod = await Product.objects.get(id=input_order_option['product']['id'])
        order_prod_set = await OrderProduct.objects.create(
            base_referance=existed_prod,
            for_order=existed,
        )
        for input_extra_opt in input_order_option['extra_options']:
            existed_prod_opt = await ProductOption.objects.get(id=input_extra_opt['option_referance']['id'])
            new_save = OrderProductOption(
                for_order=order_prod_set.pk,
                option=str(input_extra_opt['option']),
                count=input_extra_opt['count'],
                option_referance=existed_prod_opt.pk
            )
            await new_save.save_related()

        return await existed.load_all(follow=True, exclude=[
            "items__base_referance__options",
            "items__extra_options__for_order",
            "items__extra_options__option_referance__option_for_product"
        ])

    async def remove_item(self, base_order: dict) -> Order:
        """
        Remove an item from an existing order.

        :param base_order: The existing order to remove an item from.
        :type base_order: Order
        :param input_order_option: The item to remove from the order.
        :type input_order_option: OrderProduct
        :return: The updated order object with the item removed.
        :rtype: Order
        :raises str: If the request order is not a single one.
        """
        # print(base_order)
        existed = None
        if base_order['id'] != None:
            existed = await Order.objects.get_or_none(id=base_order['id'])

        elif base_order['order_number'] != None:
            existed = await Order.objects.get_or_none(order_number=base_order['order_number'])

        if existed is None:
            raise "request order is not single one"  # type: ignore

        # print(base_order['items'])
        ids = [s['id'] for s in base_order['items']]
        existed_items = await OrderProduct.objects.filter(ormar.and_(for_order__id=existed.id, id__in=ids)).all()
        for option_prod in existed_items:
            await option_prod.extra_options.clear(keep_reversed=False)
            await option_prod.delete()

        # existed.save_related()
        return await existed.load_all(follow=True, exclude=[
            "items__base_referance__options",
            "items__extra_options__for_order",
            "items__extra_options__option_referance__option_for_product"
        ])

    async def update_item(self, order: Order, tar_item: OrderProduct):
        return None

from typing import List, Dict

from fastapi import APIRouter, status, HTTPException, Response
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from yummy_pizza_api_service.web.api.based import MESSAGE_SETTING, Message


from yummy_pizza_api_service.db.dao.order_dao import OrderDAO
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.db.models.order_model import Order
from yummy_pizza_api_service.db.models.order_product_model import OrderProduct

from yummy_pizza_api_service.web.api.order.schema import (
    OrderInputDTO,
    OrderDTO,
    OrderRefProductDTO,
    OrderProductDTO
)

router = APIRouter()


@router.get("/list",
            response_model=List[OrderDTO],
            responses={**MESSAGE_SETTING}  # type: ignore
            )
async def get_latest_orders(
    limit: int = 15,
    offset: int = 0,
    order_dao: OrderDAO = Depends()
):
    """
    Retrieve a list of latest orders.

    :param limit: The maximum number of orders to retrieve.
    :type limit: int
    :param offset: The number of orders to skip.
    :type offset: int
    :param order_dao: The dependency injection for the OrderDAO class.
    :type order_dao: OrderDAO
    :return: A list of OrderDTO objects.
    :rtype: List[OrderDTO]
    """
    try:
        return await order_dao.get_latest_order(limit=limit, offset=offset)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/create",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}  # type: ignore
             )
async def create_order(
    new_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Creates a new order using the provided input data and saves it to the database.

    :param new_order: The input data for the new order.
    :type new_order: OrderInputDTO
    :param order_dao: The DAO object to use for interacting with the database. Defaults to Depends().
    :type order_dao: OrderDAO, optional
    :return: The newly created order.
    :rtype: Order
    """
    return await order_dao.create(order=new_order.dict())


@router.post("/search",
             response_model=List[OrderDTO],
             responses={**MESSAGE_SETTING}  # type: ignore
             )
async def filter_order_models(
    order_filter_query: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Filter order models based on the given filter query.

    :param order_filter_query: An instance of OrderInputDTO containing filter parameters.
    :param order_dao: An instance of OrderDAO to perform the filtering.
    :return: A list of Order models that match the filter query.
    """
    # try:
    return await order_dao.filter(**order_filter_query.dict())
    # except Exception as e:
    #     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/cancel",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}  # type: ignore
             )
async def cancel_order(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Cancel an order in the database.

    :param target_order: The order to be canceled.
    :type target_order: OrderInputDTO
    :param order_dao: The data access object for orders.
    :type order_dao: OrderDAO
    :return: A dictionary containing the edited status and the "complete" string.
    :rtype: dict
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.void_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )
    return result


@router.post("/confirm",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def confirm_order(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Confirms an order given an OrderInputDTO and an OrderDAO.

    :param target_order: an OrderInputDTO representing the order to be confirmed
    :type target_order: OrderInputDTO
    :param order_dao: an OrderDAO object to access the database
    :type order_dao: OrderDAO

    :return: an OrderDTO representing the confirmed order
    :rtype: OrderDTO

    :raises HTTPException 404: if the target_order.id does not exist or the order is not found
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.confirm_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )

    return result


@router.post("/payment_order",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def payment_order(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Endpoint for processing payment orders.

    :param target_order: An instance of OrderInputDTO class representing the payment order to be processed.
    :type target_order: OrderInputDTO
    :param order_dao: An instance of OrderDAO class for communicating with the database.
    :type order_dao: OrderDAO
    :return: An instance of OrderDTO class representing the result of the payment order processing.
    :rtype: OrderDTO
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.request_payment_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )

    return result


@router.post("/payment_complete",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def payment_complete(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Receives a POST request from the payment gateway confirming the completion of payment.
    If the order with the given ID is not found, or the ID is empty, returns a JSONResponse
    with the appropriate status and error message. Otherwise, returns the result of the
    producing_order method from the OrderDAO.

    :param target_order: An instance of OrderInputDTO representing the order that was paid for.
    :type target_order: OrderInputDTO
    :param order_dao: An instance of OrderDAO used to interact with the database.
    :type order_dao: OrderDAO
    :return: An instance of OrderDTO representing the order that was paid for.
    :rtype: OrderDTO
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.producing_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )

    return result


@router.post("/start_deliver",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def deliver_order(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Starts the delivery process of a given order.

    :param target_order: The order to be delivered.
    :type target_order: OrderInputDTO
    :param order_dao: The data access object for orders.
    :type order_dao: OrderDAO

    :return: The updated order with new delivery status.
    :rtype: OrderDTO

    :raises:
        - HTTPException: If the order id is empty or the order is not found.
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.sending_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )

    return result


@router.post("/complete",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def complete_order(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Send a POST request to complete an order and returns the completed order.

    :param target_order: an instance of OrderInputDTO representing the order to be completed.
    :param order_dao: an instance of OrderDAO used to interact with the database.
    :return: an instance of Order representing the completed order.
    :raises HTTPException: if the target_order id is None or if the order is not found in the database.
    """
    if target_order.id == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("id is empty"))
        )

    result = await order_dao.complete_order(target_order.id)
    if result == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Message(status="error", reason=str("order is not found")).dict()
        )

    return result


@router.post("/get_recept",
             response_model=Dict,
             responses={**MESSAGE_SETTING}
             )
async def get_recept(
    target_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Retrieves a recept for the given target order.

    :param target_order: The order input DTO to retrieve the recept for.
    :type target_order: OrderInputDTO
    :param order_dao: The order data access object to use.
    :type order_dao: OrderDAO
    :return: A dictionary containing the export text for the recept.
    :rtype: Dict
    :raises: HTTPException(404) if the target order is not found.
    """
    return {"export_text": ""}


"""
# Item related
"""


@router.post("/item/add",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def order_add_item(
    updated_order: OrderRefProductDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Add an item to the order with the provided `updated_order` data.

    :param updated_order: The updated order information.
    :type updated_order: OrderRefProductDTO
    :param order_dao: The data access object for orders.
    :type order_dao: OrderDAO
    :return: The updated order.
    :rtype: Order
    :raises HTTPException: If the precondition fails while adding the item.
    """
    return await order_dao.add_item(
        base_order=updated_order.dict(),  # type: ignore
        input_order_option=updated_order.dict()  # type: ignore
    )


@router.post("/item/remove",
             response_model=OrderDTO,
             responses={**MESSAGE_SETTING}
             )
async def order_remove_item(
    updated_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
):
    """
    Remove an item from an order.

    :param updated_order: The updated order reference product.
    :type updated_order: OrderRefProductDTO
    :param order_dao: The order data access object, defaults to Depends()
    :type order_dao: OrderDAO, optional
    :return: The updated order.
    :rtype: Order
    :raises HTTPException: If the precondition fails.
    """
    return await order_dao.remove_item(
        base_order=updated_order.dict(),  # type: ignore
    )
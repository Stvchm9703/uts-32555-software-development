import { Order, Product, OrderProduct, OrderContactType, OrderDeliveryType, OrderRefProductDTO } from "./type";
import cloneDeep from 'lodash/cloneDeep';


/**
 * Fetches a list of products from the API.
 * @param page_number - Optional page number to fetch. Defaults to 1.
 * @returns A promise that resolves to an array of products.
 */
export const fetchProduct = async (page_number?: number): Promise<Array<Product>> => {
  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");

  const requestOptions: RequestInit = {
    method: 'GET',
    headers: requestHeader,
    redirect: 'follow',
    // body: JSON.stringify(params),
  };

  const page_size = 50;
  let link = `http://localhost:8000/api/product/?limit=${page_size}`;
  if (page_number && page_number > 1) {
    link += '&offset=' + page_number * 50;
  }
  const result = await fetch(link, requestOptions);
  return await result.json();
}



/**
 * Sends a POST request to create a new order with the given input order.
 * @param inputOrder - The order to create.
 * @returns A Promise that resolves to the created order.
 */
export const fetchOrderList = async (page_number?: number) => {
  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");

  const requestOptions: RequestInit = {
    method: 'GET',
    headers: requestHeader,
    redirect: 'follow',
    // body: JSON.stringify(params),
  };

  const page_size = 50;
  let link = `http://localhost:8000/api/order/list?limit=${page_size}`;
  if (page_number && page_number > 1) {
    link += '&offset=' + page_number * 50;
  }
  const result = await fetch(link, requestOptions);
  return await result.json();
}


/**
 * Creates an order by sending a POST request to the server at `http://localhost:8000/api/order/create`.
 * The request body is a JSON representation of the input order object. The `items` property is removed from the
 * input object before sending the request.
 * @param {Order} inputOrder - The input order object to be sent to the server.
 * @returns {Promise<Order>} - A promise that resolves with the newly created order object returned by the server.
 */
export const createOrder = async (inputOrder: Order): Promise<Order> => {

  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");
  requestHeader.append("Content-Type", "application/json");
  const _cloned: {} = cloneDeep(inputOrder);

  delete _cloned['items']
  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(_cloned),
  };
  const result = await fetch(`http://localhost:8000/api/order/create`, requestOptions);
  return await result.json();
}


/**
 * Send a request to cancel an order to the API and return the updated order.
 * @param inputOrder - The order to cancel.
 * @returns A promise that resolves to the updated order after it has been cancelled.
 */
export const voidOrder = async (inputOrder: Order): Promise<Order> => {

  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");
  requestHeader.append("Content-Type", "application/json");
  const _cloned: {} = cloneDeep(inputOrder);

  delete _cloned['items']
  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(_cloned),
  };
  const result = await fetch(`http://localhost:8000/api/order/cancel`, requestOptions);
  return await result.json();
}

/**
 * Adds an item to an order and returns the updated order.
 * @param inputOrder - The order to add the item to.
 * @param inputOrderItem - The item to add to the order.
 * @returns A Promise that resolves to the updated order.
 */
export const orderAddItem = async (inputOrder: Order, inputOrderItem: OrderProduct): Promise<Order> => {
  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");
  requestHeader.append("Content-Type", "application/json");

  const tyu: OrderRefProductDTO = {
    order_number: inputOrder.order_number,
    quality: inputOrderItem.quality || 1,
    product: inputOrderItem.product,
    extra_options: inputOrderItem.extra_option,
    remark: inputOrderItem.remark,
  }

  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(tyu),
  };
  const result = await fetch(`http://localhost:8000/api/order/item/add`, requestOptions);
  return await result.json();
}

/**
 * Confirm an order by sending a POST request to the API endpoint.
 * The input order is deep cloned and modified to exclude items before being sent.
 * @param inputOrder The order to be confirmed.
 * @returns A promise that resolves to the confirmed order as JSON.
 */
export const confirmOrder = async (inputOrder: Order): Promise<Order> => {

  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");
  requestHeader.append("Content-Type", "application/json");
  const _cloned: {} = cloneDeep(inputOrder);

  delete _cloned['items']
  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(_cloned),
  };
  const result = await fetch(`http://localhost:8000/api/order/confirm`, requestOptions);
  return await result.json();
}



/**
 * Sends a payment request to the server for the given `inputOrder` object and returns the updated order.
 * @param {Order} inputOrder The order to be paid.
 * @returns {Promise<Order>} A Promise resolving to the updated order object.
 */
export const payOrder = async (inputOrder: Order): Promise<Order> => {

  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");
  requestHeader.append("Content-Type", "application/json");
  const _cloned: {} = cloneDeep(inputOrder);

  delete _cloned['items']
  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(_cloned),
  };
  const result = await fetch(`http://localhost:8000/api/order/payment_order`, requestOptions);
  return await result.json();
}


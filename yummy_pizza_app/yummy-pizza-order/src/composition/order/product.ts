import { Order, Product, OrderProduct, OrderContactType, OrderDeliveryType } from "./type";

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




const createOrder = async (params: Order): Promise<Order> => {

  const requestHeader = new Headers();
  requestHeader.append("Accept", "application/json");

  const requestOptions: RequestInit = {
    method: 'POST',
    headers: requestHeader,
    redirect: 'follow',
    body: JSON.stringify(params),
  };
  const result = await fetch(`http://localhost:8000/api/order/create`, requestOptions);
  return await result.json();
}

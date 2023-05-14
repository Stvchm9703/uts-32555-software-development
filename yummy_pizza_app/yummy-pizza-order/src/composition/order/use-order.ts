import { createStore } from "solid-js/store";
import { Order, Product, OrderProduct, OrderContactType, OrderDeliveryType, ExtraOption, OptionKind } from "./type";
import { createUniqueId } from "solid-js";
import {
  createOrder as fetchCreateOrder,
  confirmOrder as fetchConfirmOrder,
  payOrder as fetchPayOrder,
  voidOrder as fetchVoidOrder,
  orderAddItem as fetchOrderAddItem,


} from './product';
import cloneDeep from 'lodash/cloneDeep';
export const createOrderObject = (i_contact_type?: OrderContactType, i_deliver_tyoe?: OrderDeliveryType): Order => ({
  // status:"created",
  staff: "pos",
  contact_type: i_contact_type || "walk_in",
  deliver_type: i_deliver_tyoe || "dine_in",
  items: [],
});


export const createExtraOption = (option_id: number, option_kind: OptionKind, option_value: any, charge: number): ExtraOption => {
  if (option_kind === "favour" || option_kind === 'size') {
    return {
      option: option_value as string,
      option_referance: {
        id: option_id
      },
      charge
    }
  }
  return {
    count: parseInt(option_value) as number,
    option_referance: {
      id: option_id
    },
    charge
  }
}

export const createOrderProduct = (product_id: number): OrderProduct => {
  return {
    product: {
      id: product_id,
    },
    quality: 1,
    remark: "",
    extra_option: [],
    _id: createUniqueId()
  } as OrderProduct
}

export default (user_order: Order, involve_api: boolean | undefined = false) => {
  const baseOrder: Order = {
    ...(createOrderObject()),
    ...user_order,
  }
  const [currentOrder, setOrder] = createStore(baseOrder);
  const involved_api = involve_api ?? false;


  const setCustomer = (customer_name?: string, customer_contact?: number, customer_address?: string): Order => {
    if (customer_name) setOrder({ customer_name });
    if (customer_contact) setOrder({ customer_contact });
    if (customer_address) setOrder({ customer_address });
    return currentOrder;
  };

  const addExtraOption = (ref_item_id: number, option_id: number, option_kind: OptionKind, option_value: any): ExtraOption => {
    return createExtraOption(option_id, option_kind, option_value);
  }

  const addItem = (product: Product, extra_option: Array<ExtraOption>) => {
    if (!product.id) throw "missing_product_id";
    // let item = currentOrder.items.find(elm => elm.product && elm.product.id === product.id);
    // if (item && product.options && product.options.length !== 0) throw "exist_product";

    const itemT = createOrderProduct(product.id);
    if (!itemT.extra_option) itemT.extra_option = [];
    if (extra_option) {
      itemT.extra_option.push(...(extra_option.filter(elm => elm && elm.option_referance && elm.option_referance.id)));
    }

    setOrder('items', ls => [...ls, itemT]);
  }

  const removeItem = (product: OrderProduct) => {
    setOrder('items', list => list.filter(elm => !(elm._id === product._id)))
  }

  const currentOrderTotal = (menu) => {
    const item_sub = currentOrder.items.map(elm => {
      const prod = menu.find(m => m.id === elm.product?.id)
      return (prod.price_value * (1 + prod.rate)) + (elm.extra_option || []).reduce((a, b) => (a + (b.count || 1) * (b.charge || 0)), 0);
    })
    return Math.round(item_sub.reduce((a, b) => a + b, 0) * 100) / 100
  }

  const commitOrder = () => new Promise(async (res, rej) => {
    let result = await fetchCreateOrder(currentOrder);
    let updated_result;
    for (const y of currentOrder.items) {
      updated_result = await fetchOrderAddItem(result, y);
    }
    setOrder({ ...updated_result, items: updated_result.items.map(elm => ({ ...elm, product: elm.base_referance })) });
    return res(updated_result);
  })

  const confirmOrder = () => new Promise(async (res, rej) => {
    let result = await fetchConfirmOrder(currentOrder);
    setOrder({ ...result, items: result.items.map(elm => ({ ...elm, product: elm.base_referance })) });
    return res(result);
  })

  const payOrder = () => new Promise(async (res, rej) => {
    let result = await fetchPayOrder(currentOrder);
    setOrder({ ...result, items: result.items.map(elm => ({ ...elm, product: elm.base_referance })) });
    return res(result);
  })

  const resetOrder = () => setOrder(createOrderObject());
  const voidOrder = () => new Promise(async (res, rej) => {
    let result = await fetchVoidOrder(currentOrder);
    // setOrder({ ...result, items: result.items.map(elm => ({ ...elm, product: elm.base_referance })) });
    setOrder(createOrderObject());
    return res(result);
  })
  const setDelivery = (deliver_type) => {
    if (["dine_in", "take_away", "remote_delivery"].includes(deliver_type) === false)
      throw "no exist";
    setOrder({ deliver_type })
  }
  return {
    currentOrder,
    createOrderObject,
    setCustomer,
    addExtraOption,
    addItem, removeItem,
    currentOrderTotal,
    resetOrder,
    commitOrder,
    confirmOrder,
    payOrder,
    setDelivery,
    voidOrder
  }
}



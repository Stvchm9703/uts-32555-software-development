import { createStore } from "solid-js/store";
import { Order, Product, OrderProduct, OrderContactType, OrderDeliveryType, ExtraOption, OptionKind } from "./type";

export const createOrderObject = (i_contact_type?: OrderContactType, i_deliver_tyoe?: OrderDeliveryType): Order => ({
  // status:"created",
  contact_type: i_contact_type || "walk_in",
  deliver_type: i_deliver_tyoe || "dine_in",
  items: [],
});


export const createExtraOption = (option_id: number, option_kind: OptionKind, option_value: any): ExtraOption => {
  if (option_kind === "favour") {
    return {
      option: option_value as string,
      option_referance: {
        id: option_id
      },
    }
  }
  return {
    count: option_value as number,
    option_referance: {
      id: option_id
    },

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
    // const 
    return currentOrder;
  };


  const addExtraOption = (ref_item_id: number, option_id: number, option_kind: OptionKind, option_value: any): ExtraOption => {
    const extraopt = createExtraOption(option_id, option_kind, option_value);

    if (involved_api) {
      // do fetch 
    }
    return extraopt;
  }

  const removeExtraOption = (ref_item_id: number, option_id: number) => {
    
  }

  const addItem = (product: Product, extra_option: Array<ExtraOption>) => {
    if (!product.id) throw "missing_product_id";
    let item = currentOrder.items.find(elm => elm.product && elm.product.id === product.id);
    if (item) throw "exist_product";

    const itemT = createOrderProduct(product.id);
    if (!itemT.extra_option) itemT.extra_option = [];
    if (extra_option) {
      itemT.extra_option.push(...(extra_option.filter(elm => elm && elm.option_referance && elm.option_referance.id)));
    }
    if (involved_api) {
      // do fetch 

    } else {
      setOrder('items', ls => [...ls, itemT]);
    }
  }

  const removeItem = (product: Product | number) => {
    if (!involved_api) {


      if (Number.isInteger(product)) {
        setOrder('items', list => list.filter(elm => !(elm.product?.id === (product as number))))
      }
      if ((product as Product).id !== undefined) {
        setOrder('items', list => list.filter(elm => !(elm.product?.id === (product as Product).id)))
      }
    } else {
      // do api fetch
    }
  }


  return {
    currentOrder,
    createOrderObject,
    setCustomer,
    addExtraOption,
    addItem,
  }
}



export type OrderContactType = "walk_in" | "phone_in" | "online_system";

export type OrderStatus = "created" | "void" | "paid" | "unpaid" | "producing" | "delivering" | "completed";


export type OrderDeliveryType = "dine_in" | "take_away" | "remote_delivery";

export interface Order {
  id?: number;
  contact_type?: OrderContactType;
  status?: OrderStatus;
  deliver_type?: OrderDeliveryType;
  customer_name?: string;
  customer_contact?: number;
  customer_address?: string;
  order_number?: number;
  staff?: string;
  items: OrderProduct[];
  transaction?: any;
}

export interface Product {
  id?: number;
  name?: string;
  description?: string;
  item_type?: ItemType | string;
  category?: string;
  kal?: number;
  price_value?: number;
  rate?: number;
  options?: ProductOption[];
}

export type ItemType = "single" | "side";

export interface ProductOption {
  id?: number;
  name?: string;
  description?: string;
  extra_charge?: number;
  option_kind?: OptionKind;
  max_count?: number | null;
  min_count?: number | null;
  kal?: number;
  option_sets?: string[] | null;
}

export type OptionKind = "favour" | "size" | "number_count";



// for order
export interface OrderProduct {
  product?: Product;
  id?: number;
  quality?: number;
  extra_option?: ExtraOption[];
  remark?: string;
  _id?: string;
}

export interface ExtraOption {
  id?: number;
  option?: string;
  count?: number;
  charge?: number;
  option_referance?: ProductOption;
}



export interface OrderRefProductDTO {

  id?: number,
  order_number?: number,
  quality?: number,
  product?: Product | {
    id?: number,
  },
  extra_options?: Array<ExtraOption>,
  remark?: string,
}
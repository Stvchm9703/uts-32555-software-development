import { } from '../order/type';



export interface TableAppointment {
  id?: number
  appointment_reference?: string
  order_number?: number
  customer_name?: string
  customer_contact?: number
  customer_address?: string
  people_count?: number

  staff?: string
  timeslot_start?: string
  timeslot_end?: string
  transaction?: any
}
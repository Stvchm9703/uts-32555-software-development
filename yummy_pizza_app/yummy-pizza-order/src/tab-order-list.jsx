import InputField from "./input-set";
// import Dialog from "./dialog";
import { For, Show, Suspense, lazy, createSignal, onMount, createEffect } from "solid-js";
// import { OrderDialog } from "./order-dialog";
const OrderDialog = lazy(() => import('./order-dialog'))
const OrderSearchTableContainer = ({ children }) => (
  <div class="mt-2 relative overflow-x-auto">
    <table class="rounded-md border-solid border-[#e2e8f0] border py-2.5 px-5 flex flex-col gap-0 items-start justify-start min-h-75vh relative" >
      <thead class="block w-full text-xs text-gray-700">
        <tr class="border-solid border-[#cbd5e1] border-b-1 py-1.5 px-0  flex flex-row gap-2 items-center justify-start self-stretch shrink-0 h-10 relative">
          <th scope="col" className="p-1 pl-0 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[70px] relative">
            <span className="text-dark-600 text-left relative font-semibold" > Order No. </span>
          </th>
          <th scope="col" className="p-1 flex flex-row gap-2.5 items-center justify-start flex-1 relative">
            <span className="text-dark-600 text-center relative flex items-center justify-center font-semibold" > Customer name </span>
          </th>

          <th scope="col" className="p-1 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[300px] relative">
            <span className="text-dark-600 text-left relative flex-1 h-5 flex items-center justify-start font-semibold" > Customer Contact </span>
          </th>

          <th scope="col" className="p-1 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[120px] relative">
            <span className="text-dark-600 text-center relative flex items-center justify-center font-semibold" > Order Status </span>
          </th>

          <th scope="col" className="p-1 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[120px] relative">
            <span className="text-dark-600 text-center relative flex items-center justify-center font-semibold" > Delivery </span>
          </th>
        </tr>
      </thead>
      <tbody className="block w-full overflow-y-scroll scrollbar-hide">
        {children}
      </tbody>
    </table>
  </div>
);


const OrderSearchTableItem = ({ tableData /** @type Order*/, onTableRowClick }) => (
  <tr
    className="border-solid border-[#cbd5e1] border-b-1 py-1.5 px-0 flex flex-row gap-2 items-center justify-start shrink-0 w-full h-15"
    onClick={onTableRowClick}
  >
    <td className=" p-1 pl-0 flex flex-row gap-2.5 items-center justify-start shrink-0 w-17 relative">
      <span className="text-dark-600 text-left relative" > {tableData.order_number} </span>
    </td>

    <td className="p-1 flex flex-row gap-2.5 items-center justify-start flex-1 relative">
      <span className="text-dark-600 text-center relative flex items-center justify-center" > {tableData.customer_name} </span>
    </td>

    <td className="p-1 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[300px] relative">
      <span className="text-dark-600 text-left relative flex-1 h-5 flex items-center justify-start" > {tableData.customer_contact} </span>
    </td>

    <td className=" rounded py-1.5 px-2 flex flex-row gap-2.5 items-center justify-start shrink-0 min-w-30 relative"
      classList={{
        'bg-[#59c857]': tableData.status === 'completed',
        'bg-[#c99c58]': tableData.status === 'delivering',
        'bg-[#b82626]': tableData.status === 'producing',
      }}
    >
      <span className="text-light-100 text-center relative flex items-center justify-center" > {tableData.status} </span>
    </td>

    <td className="p-1 flex flex-row gap-2.5 items-center justify-start shrink-0 w-[120px] relative">
      <span className="text-dark-600 text-center relative flex items-center justify-center" > {tableData.deliver_type} </span>
    </td>
  </tr>
);



export default ({ createOrderIsOpen, setCreateOrderIsOpen }) => {
  // const [dialogShow, setDialogShow] = createMemo();
  // console.log(createOrderIsOpen(), setCreateOrderIsOpen);
  // const setDialogShow = (value) => setCreateOrderOoen(value)
  const [order_list, setOrderList] = createSignal([]);
  const onSearchEnter = (keyword) => { }
  const onTableRowClick = () => {

  }


  const [tabOrderIsOpen, setTabOrderIsOpen] = createSignal(false);
  createEffect(() => {
    if (createOrderIsOpen()) {
      setTabOrderIsOpen(true);
    }
  }, createOrderIsOpen());

  const onSetTabOrderIsOpen = (value) => {
    if (value === false) {
      setCreateOrderIsOpen(false);
      setTabOrderIsOpen(false);
    }
  }

  onMount(async() => {
    
    setOrderList([{
      id: 1,
      contact_type: "walk_in",
      status: "completed",
      deliver_type: "dine_in",
      customer_name: "John Smith",
      customer_contact: 435123434,
      customer_address: "",
      order_number: 1,
      staff: "steven",
      items: []
    }]);
  })

  return (
    <>
      <InputField onSearchEnter={onSearchEnter} />
      <OrderSearchTableContainer>
        <Suspense fallback={(<p> loading </p>)}>
          <For each={order_list()}>
            {(order_set) => (
              <OrderSearchTableItem tableData={order_set} onTableRowClick={onTableRowClick}/>
            )}
          </For>
        </Suspense>
      </OrderSearchTableContainer>
      <Show when={tabOrderIsOpen()}>
        <OrderDialog setCreateOrderIsOpen={onSetTabOrderIsOpen} />
      </Show>
    </>
  )
}

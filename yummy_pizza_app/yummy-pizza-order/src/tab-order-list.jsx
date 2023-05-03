import { Portal } from "solid-js/web";
import InputField from "./input-set";
import spinner from "./spinner";
// import Dialog from "./dialog";
import { Show, createMemo, createResource, createSignal, lazy } from "solid-js";
const Dialog = lazy(() => import('./dialog'))
const OrderSearchTableContainer = ({ children, tableKey }) => {
  return (
    <div class="relative overflow-x-auto">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <For each={tableKey}>
              {(column, index) =>
                <th scope="col" class="px-6 py-3" data-index={index} data-column={column.key}>
                  {column.label}
                </th>
              }
            </For>
          </tr>
        </thead>
        <tbody>
          {children}
        </tbody>
      </table>
    </div>
  )
};

const OrderSearchTableItem = ({ tableData }) => {
  return (
    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
    </tr>
  )
}


const CreateOrderDialog = ({ setCreateOrderIsOpen }) => {
  const fetchUser = async () => (await fetch(`https://swapi.dev/api/people/1/`)).json()
  // const [d, set_d] = createSignal()
  const [options, { mutate, refetch }] = createResource("", fetchUser);

  return (
    <Portal>
      <Dialog title="Create Order" onCloseClick={() => setCreateOrderIsOpen(false)} >
        <div className="flex py-1.5" >
          <div className="flex flex-col w-65%">
            <Suspense fallback={spinner}>
              {!options.loading && (
                <p>
                  {JSON.stringify(options(), null, 2)}
                </p>
              )}
            </Suspense>
          </div>

          <div className="border-l-1 border-coolGray p-4"></div>
        </div>
      </Dialog>
    </Portal>

  )
}


export default ({ createOrderIsOpen, setCreateOrderIsOpen }) => {
  // const [dialogShow, setDialogShow] = createMemo();
  // console.log(createOrderIsOpen(), setCreateOrderIsOpen);
  // const setDialogShow = (value) => setCreateOrderOoen(value)
  return (
    <>
      <InputField />
      <OrderSearchTableContainer tableKey={[]}>
        <OrderSearchTableItem></OrderSearchTableItem>
      </OrderSearchTableContainer>
      <Show when={createOrderIsOpen()}>
        <CreateOrderDialog setCreateOrderIsOpen={setCreateOrderIsOpen} />
      </Show>
    </>
  )
}

// (


//   <div
//     class="pt-5 pr-0 pb-0 pl-0 flex flex-col gap-2 items-start justify-start w-[1160px] h-[952px] relative"
//   >
//     <div
//       class="pt-0 pr-0 pb-[136px] pl-0 flex flex-row gap-2 items-start justify-start self-stretch shrink-0 h-[42px] relative overflow-hidden"
//     >
//       <div
//         class="bg-slate-100 rounded-md p-[5px] flex flex-row gap-0 items-start justify-start flex-1 relative"
//       >
//         <div
//           class="bg-[#ffffff] rounded-[3px] pt-1.5 pr-3 pb-1.5 pl-3 flex flex-row gap-2.5 items-start justify-start shrink-0 relative"
//         >
//           <div
//             class="text-slate-900 text-left relative"
//             style="font: var(--subtle-medium, 500 14px/20px 'Inter', sans-serif)"
//           >
//             Order List
//           </div>
//         </div>

//         <div
//           class="rounded-[3px] pt-1.5 pr-3 pb-1.5 pl-3 flex flex-row gap-2.5 items-start justify-start shrink-0 relative"
//         >
//           <div
//             class="text-slate-700 text-left relative"
//             style="font: var(--subtle-medium, 500 14px/20px 'Inter', sans-serif)"
//           >
//             Create Order
//           </div>
//         </div>
//       </div>

//       <div
//         class="bg-slate-900 rounded-md pt-2 pr-4 pb-2 pl-4 flex flex-row gap-0 items-center justify-end shrink-0 h-[42px] relative"
//       >
//         <div
//           class="text-[#ffffff] text-left relative"
//           style="font: var(--body-medium, 500 14px/24px 'Inter', sans-serif)"
//         >
//           Continue
//         </div>
//       </div>
//     </div>

//     <div class="self-stretch shrink-0 h-[884px] relative"></div>
//   </div>
// )
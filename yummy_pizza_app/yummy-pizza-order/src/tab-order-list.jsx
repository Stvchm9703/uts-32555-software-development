import InputField from "./input-set";


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


export default () => {
  return (
    <>
      <InputField />
      <OrderSearchTableContainer>
        <OrderSearchTableItem></OrderSearchTableItem>
      </OrderSearchTableContainer>
    </>
  )
}
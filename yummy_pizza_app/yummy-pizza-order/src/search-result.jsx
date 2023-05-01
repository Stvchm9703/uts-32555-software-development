import { For, children, createEffect } from "solid-js";

const SearchTableContainer = ({ children, tableKey }) => {

  <div className="overflow-x-auto">

    <div class="relative overflow-x-auto">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
           
            <th scope="col" class="px-6 py-3">
              Product name
            </th>
            <th scope="col" class="px-6 py-3">
              Color
            </th>
            <th scope="col" class="px-6 py-3">
              Category
            </th>
            <th scope="col" class="px-6 py-3">
              Price
            </th>
          </tr>
        </thead>
        <tbody>
          {props.children}
        </tbody>
      </table>
    </div>

  </div>;
};

const SearchTableItem = (props) => (
  <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
      Apple MacBook Pro 17"
    </th>
    <td class="px-6 py-4">
      Silver
    </td>
    <td class="px-6 py-4">
      Laptop
    </td>
    <td class="px-6 py-4">
      $2999
    </td>
    <td class="px-6 py-4 text-right">
      <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a>
    </td>
  </tr>
)

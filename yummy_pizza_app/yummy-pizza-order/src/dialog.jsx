export default ({ children, isActive, onCloseClick, title, onConfirmClick, onCancelClick }) => {

  return (
    <div id="extralarge-modal" tabindex="-1" class="fixed inset-0 z-50 w-full p-4 overflow-hidden h-[calc(100%-1rem)] max-h-screen">
      <div class="relative w-full max-w-7xl max-h-screen m-auto">
        <div class="bg-white rounded-lg shadow dark:bg-gray-700">
          <div class="flex items-center justify-between p-5 border-b rounded-t dark:border-gray-600">
            <h3 class="text-xl font-medium text-gray-900 dark:text-white">
              {title}
            </h3>
            <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="extralarge-modal" onClick={onCloseClick}>
              <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
              <span class="sr-only">Close modal</span>
            </button>
          </div>
          <div class="p-6 space-y-6  flex max-h-80vh">
            {children}
          </div>
          <div class="flex items-center justify-center p-6 space-x-2 border-t border-gray-200 rounded-b dark:border-gray-600">
            <button data-modal-hide="extralarge-modal" type="button" class="text-white bg-slate-900 hover:bg-slate-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center" onClick={onConfirmClick}>Confirm</button>
            <button data-modal-hide="extralarge-modal" type="button" class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-600" onClick={onCancelClick}>Cancel</button>
          </div>
        </div>
      </div>
    </div>
  )
}
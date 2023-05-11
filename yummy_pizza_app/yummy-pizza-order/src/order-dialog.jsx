import { Portal } from "solid-js/web";
import spinner from "./spinner";
import { For, Suspense, createResource, Show, Switch, createSignal, lazy } from "solid-js";
import createOrder from "./composition/order/use-order";
import { fetchProduct } from "./composition/order/product";
import Dialog from "./dialog";
// export const Dialog = lazy(() => import('./dialog'));
export const fetchMenu = async (page_number) => {
  try {
    return await fetchProduct(page_number);
  } catch {
    return (await import('./assets/deno-product.json')).default;
  }
}
export const ProductListItem = ({ item, onItemAddClick }) => {
  const [isActive, setActive] = createSignal(false);
  const onAccordionClick = () => {
    setActive(!isActive());
  };
  // onItemClick(item.id);
  const category_list = () => item.category.split(',') || [];
  const setExtraOption = (key_name, value) => { };
  return (
    <div>
      <h2 class="flex sticky top-0 bg-white z-50">
        <button type="button" class="flex items-center justify-start w-full py-5 font-medium text-left text-gray-500 border-b border-gray-200 dark:border-gray-700 dark:text-gray-400" aria-expanded={isActive()} aria-controls="accordion-flush-body-1" onClick={onAccordionClick}>
          <span className="badge mr-4" classList={{
            'badge-primary': item.item_type === 'single',
            'badge-secondary': item.item_type === 'side',
            'badge-accent': item.item_type === 'combo_set',
            'bg-red-500': item.item_type === 'discount',
          }}> {item.item_type} </span>
          <span className="text-lg">{item.name}</span>
          <svg data-accordion-icon class="ml-auto mr-3 w-6 h-6  shrink-0" classList={{ 'rotate-180': isActive() }} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button>

      </h2>
      <div id="accordion-flush-body-1" classList={{ 'hidden': !isActive() }} aria-labelledby="accordion-flush-heading">
        <div className="flex pr-2 py-4">
          <For each={category_list()}>
            {(cat) => (
              <span className="badge badge-outline mx-1">{cat}</span>
            )}
          </For>
        </div>
        <div class="py-5 border-b border-gray-200 dark:border-gray-700">
          <p class="mb-2 text-gray-500 dark:text-gray-400">{item.description}</p>

          <Show when={item.options && item.options.length > 0}>
            <div className="block w-full h-auto bg-gray-100 rounded py-2 px-3">
              <h3 className="text-xl py-1 pl-3">Other custom options</h3>
              <For each={item.options}>
                {(sub_opt) => (
                  <div className="flex flex-col px-1 py-3 border-t-1 border-gray-400">
                    <h4 className="text-lg">{sub_opt.name}</h4>
                    <span className="text-sm my-1"> {sub_opt.description} </span>
                    <span className="text-sm my-1"> kal : {sub_opt.kal} </span>
                    <Switch>
                      <Match when={sub_opt.option_kind === 'number_count'}>
                        <div className="flex items-center">
                          <kbd class="kbd bg-gray-200">-</kbd>
                          <div class="w-full px-2">
                            <input type="range" min={sub_opt.min_count} max={sub_opt.max_count} value={1} class="range" step="1" />
                          </div>
                          <kbd class="kbd bg-gray-200">+</kbd>
                        </div>
                      </Match>
                      <Match when={sub_opt.option_kind === 'favour'}>
                        <ul class="grid w-full gap-6 md:grid-cols-2">
                          <For each={sub_opt.option_sets}>
                            {(favor, fid) => (
                              <li>
                                <input id={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} type="radio" name={sub_opt.name} value={favor} class="hidden peer" />
                                <label for={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} class="block w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700">
                                  <span class="block w-full text-lg font-semibold"> {favor} </span>
                                  <span class="block w-full text-sm font-semibold text-right">(extra charge: {sub_opt.extra_charge})</span>
                                </label>
                              </li>
                            )}
                          </For>
                        </ul>
                      </Match>
                      <Match when={sub_opt.option_kind === 'size'}>
                        <ul class="grid w-full gap-6 md:grid-cols-2">
                          <For each={sub_opt.option_sets}>
                            {(favor, fid) => (
                              <li>
                                <input id={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} type="radio" name={sub_opt.name} value={favor} class="hidden peer" />
                                <label for={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} class="block w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700">
                                  <span class="block w-full text-lg font-semibold"> {favor} </span>
                                  <span class="block w-full text-sm font-semibold"> {sub_opt.extra_charge} </span>
                                </label>
                              </li>
                            )}
                          </For>
                        </ul>
                      </Match>
                    </Switch>
                  </div>
                )}
              </For>
            </div>
          </Show>
          <div class="flex mb-2 text-gray-500 dark:text-gray-400 pt-3 pb-2 px-2 sticky bottom-0 bg-white">
            <div className="px-5 py-2 flex item-center rounded bg-gray-200">
              Kal :   {item.kal}
            </div>
            <div className="ml-auto mr-2 px-5 py-2 flex item-center rounded bg-gray-200">
              $   {item.price_value} (with tax: {Math.round(item.price_value * (1 + item.rate) * 100) / 100}, rate : {item.rate})
            </div>
            <button type="button" class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded text-sm px-5 py-2 mr-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  );
};




export default ({ setCreateOrderIsOpen, existOrder }) => {
  const [options, { mutate, refetch }] = createResource(1, fetchMenu);
  const onItemAddClick = () => { };
  const onItemRemoveClick = () => { };
  const { currentOrder } = createOrder(existOrder);
  return (
    <Portal>
      <Dialog title="Create Order" onCloseClick={() => setCreateOrderIsOpen(false)}>
        <div className="max-h-full flex py-1.5 w-full">
          <div className=" flex flex-col  w-65% overflow-y-scroll bg-white dark:bg-gray-900 text-gray-900 dark:text-white ">
            <Suspense fallback={spinner}>
              <For each={options()}>
                {(option_item, i) => (<ProductListItem
                  item={option_item}
                  onItemAddClick={onItemAddClick}
                  onItemRemoveClick={onItemRemoveClick} />)}
              </For>
            </Suspense>
          </div>

          <div className="border-l-1 border-coolGray w-35% flex flex overflow-y-scroll">
            <Suspense fallback={spinner}>
              <For each={currentOrder.items}>
                {(order_item, i) => (
                  <PendingOrderProductItem item={order_item} />
                )}
              </For>
            </Suspense>
          </div>
        </div>
      </Dialog>
    </Portal>

  );
};

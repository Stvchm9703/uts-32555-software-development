import { Portal } from "solid-js/web";
import spinner from "./spinner";
import { For, Suspense, createResource, Show, Switch, createSignal, lazy, createEffect, Match } from "solid-js";
import createOrder, { createOrderProduct, createExtraOption } from "./composition/order/use-order";
import { fetchProduct } from "./composition/order/product";
import Dialog from "./dialog";
import { createStore } from "solid-js/store";
// export const Dialog = lazy(() => import('./dialog'));
export const fetchMenu = async (page_number) => {
  try {
    return await fetchProduct(page_number);
  } catch {
    return (await import('./assets/deno-product.json')).default;
  }
}




export const ProductListItem = ({ item, onItemAddClick, currentOrder }) => {
  // let input_ref = [];
  let inputGroupElem;
  const [isActive, setActive] = createSignal(false);
  const onAccordionClick = () => setActive(!isActive());
  // onItemClick(item.id);
  const category_list = () => item.category.split(',') || [];
  const [activeOption, setOption] = createSignal([] /** @type ExtraOption */);
  const _subTotal = () => (Math.round((item.price_value * (1 + item.rate)) * 100) / 100);

  const [subTotal, setSubTotal] = createSignal(_subTotal())
  const setExtraOption = (subOption, value) => {
    const { id: key_name, option_kind: kind, extra_charge: charge } = subOption;
    setOption(
      (arr) => {
        const isExisted = arr.findIndex(elm => elm.option_referance && elm.option_referance.id === key_name)
        if (isExisted > -1) {
          arr[isExisted] = createExtraOption(key_name, kind, value, charge)
        } else {
          arr.push(createExtraOption(key_name, kind, value, charge))
        }
        return arr
      }
    )
    setSubTotal(
      Math.round((
        _subTotal() +
        activeOption().reduce((a, b) => a + ((b.count || 1) * b.charge), 0)
      ) * 100) / 100
    )
  }


  const onItemAddToCart = () => {
    // const op = createOrderProduct(item.id);
    // console.log(op)
    // const op_ex = 
    onItemAddClick(item, activeOption());
    // instance reset
    setActive(false);
    setTimeout(() => {
      setOption([]);
      if (inputGroupElem) {
        inputGroupElem.reset();
      }
    }, 500);
  }

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
          <svg data-accordion-icon class="ml-auto mr-3 w-6 h-6 shrink-0 transition transition-all" classList={{ 'rotate-180': isActive() }} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button>

      </h2>
      <div id="accordion-flush-body-1" classList={{ 'hidden': !isActive() }} aria-labelledby="accordion-flush-heading">
        <div className="flex pr-2 py-4">
          <For each={category_list()}>
            {(cat) => (<span className="badge badge-outline mx-1">{cat}</span>)}
          </For>
          <div className="ml-auto ml-auto mr-2 px-5 py-2 flex item-center rounded bg-gray-200">
            Orignal: ${item.price_value}, with tax rate: {item.rate}
          </div>
        </div>
        <div class="py-5 border-b border-gray-200 dark:border-gray-700">
          <p class="mb-2 text-gray-500 dark:text-gray-400">{item.description}</p>

          <Show when={item.options && item.options.length > 0}>
            <form ref={inputGroupElem} className="block w-full h-auto bg-gray-100 rounded py-2 px-3">
              <h3 className="text-xl py-1 pl-3">Other custom options</h3>
              <For each={item.options}>
                {(sub_opt, sub_index) => (
                  <div className="flex flex-col px-1 py-3 border-t-1 border-gray-400">
                    <h4 className="text-lg">{sub_opt.name}</h4>
                    <span className="text-sm my-1"> {sub_opt.description} </span>
                    <span className="text-sm my-1"> kal : {sub_opt.kal} </span>
                    <Switch>
                      <Match when={sub_opt.option_kind === 'number_count'}>
                        <div className="flex items-center">
                          <kbd class="kbd bg-gray-200">-</kbd>
                          <div class="w-full px-2">
                            <input type="range" min={sub_opt.min_count} max={sub_opt.max_count}
                              value={1} name={`${sub_opt.name}-${sub_opt.id}`}
                              onChange={(e) => setExtraOption(sub_opt, e.target.value)} class="range" step="1" />
                          </div>
                          <kbd class="kbd bg-gray-200">+</kbd>
                        </div>
                      </Match>
                      <Match when={sub_opt.option_kind === 'favour'}>
                        <ul class="grid w-full gap-6 md:grid-cols-2">
                          <For each={sub_opt.option_sets}>
                            {(favor, fid) => (
                              <li>
                                <input id={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} type="radio" name={`${sub_opt.name}-${sub_opt.id}`}
                                  value={favor}
                                  onChange={(e) => setExtraOption(sub_opt, e.target.value)}
                                  class="hidden peer" />
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
                                <input id={`opt--${sub_opt.option_kind}-${sub_opt.id}--${fid()}`} type="radio" name={`${sub_opt.name}-${sub_opt.id}`} value={favor}
                                  onChange={(e) => setExtraOption(sub_opt, e.target.value)}
                                  class="hidden peer" />
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
            </form>
          </Show>
          <div class="flex mb-2 text-gray-500 dark:text-gray-400 pt-3 pb-2 px-2 sticky bottom-0 bg-white">
            <div className="px-5 py-2 flex item-center rounded bg-gray-200">
              Kal : {item.kal}
            </div>
            <div className="ml-auto mr-2 px-5 py-2 flex item-center rounded bg-gray-200">
              Subtotal : ${subTotal()}
            </div>
            <button type="button" class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded text-sm px-5 py-2 mr-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
              onClick={onItemAddToCart} >Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  );
};



const OrderInPending = ({ item, referMenu, onItemRemoveClick }) => {
  const displayItem = () => referMenu.find(elm => elm.id == (item.product || item.base_referance).id);
  const displayOption = () => (item.extra_option || []).map(elm => {
    const ploymer = displayItem().options.find(ee => ee.id === elm.option_referance.id);
    return { ...elm, option_referance: ploymer, };
  });
  const subTotal = () => {
    return Math.round(
      ((displayItem().price_value * (1 + displayItem().rate)) +
        (displayOption() || []).reduce((a, b) => a + ((b.count || 1) * b.option_referance.extra_charge), 0))
      * 100
    ) / 100
  }
  const [isActive, setActive] = createSignal(false);

  return (
    <div className="rounded-md border-solid border-[#cbd5e1] border mb-2 p-2 flex flex-col gap-2.5 items-start justify-start self-stretch shrink-0 h-auto relative overflow-hidden">
      <h3 className="text-dark-600 text-left relative self-stretch h-5 text-lg font-light" > {displayItem().name} </h3>
      <button className="rounded transition-color bg-red-500 hover:bg-red-700 h-8 w-8 flex items-center justify-center fill-white text-white absolute right-1 top-1" onClick={() => onItemRemoveClick(item)}>
        <svg class="scale-60" focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="32" height="32" viewBox="0 0 32 32" aria-hidden="true"><path d="M12 12H14V24H12zM18 12H20V24H18z"></path><path d="M4 6V8H6V28a2 2 0 002 2H24a2 2 0 002-2V8h2V6zM8 28V8H24V28zM12 2H20V4H12z"></path><title>Trash can</title></svg>
      </button>
      <div className="self-stretch shrink-0 h-5 relative">
        <span className="badge mr-4" classList={{
          'badge-primary': displayItem().item_type === 'single',
          'badge-secondary': displayItem().item_type === 'side',
          'badge-accent': displayItem().item_type === 'combo_set',
          'bg-red-500': displayItem().item_type === 'discount',
        }}> {displayItem().item_type} </span>
      </div>
      <Show when={isActive() && item.extra_option.length > 0}>
        <div
          className="border-solid border-[rgba(0,0,0,0.20)] border-y-1  py-1 px-2 flex flex-col gap-1 items-start justify-start self-stretch shrink-0 max-h-61 relative overflow-y-scroll scrollbar-hide"
        >
          <For each={displayOption()}>
            {(opt) => (
              <div
                className="border-solid border-[#cbd5e1] border-b-1 py-1 px-0 flex flex-row gap-2.5 items-start justify-start self-stretch shrink-0 relative overflow-hidden"
              >
                <span className="text-dark-600 text-left relative flex-1 flex items-center justify-start" >
                  {opt.option || opt.option_referance.name}
                </span>
                <Show when={opt.count} >
                  <span className="text-dark-600 text-left relative w-[60px] flex items-center justify-start" > x {opt.count} </span>
                </Show>
                <span className="text-dark-600 text-right relative w-[60px] h-[22px] flex items-center justify-end" >
                  $ {opt.count ? opt.count * opt.option_referance.extra_charge : opt.option_referance.extra_charge}
                </span>
              </div>
            )}
          </For>

        </div>
      </Show>

      <div className="flex flex-row gap-2.5 items-end justify-start shrink-0 w-full h-6 ">
        <span className="text-dark-600 text-left relative flex-1 flex items-center justify-start font-bold text-sm" >
          Sub-total : ${subTotal()}
        </span>
      </div>
      <Show when={item.extra_option && item.extra_option.length > 0}>
        <button
          onClick={() => setActive(!isActive())}
          className="rounded  block w-9.5 h-9.5  items-end justify-end shrink-0 absolute right-0 bottom-0 overflow-visible transition transition-all"
          classList={{
            'rotate-180': !isActive()
          }}
        >
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" >
            <rect x="36" y="36" width="36" height="36" rx="4" fill="#CBD5E1" fillOpacity="0.1" /> <path fillRule="evenodd" clipRule="evenodd" d="M22.7072 20.6947C22.5197 20.8822 22.2654 20.9875 22.0002 20.9875C21.735 20.9875 21.4807 20.8822 21.2932 20.6947L18.0002 17.4017L14.7072 20.6947C14.615 20.7902 14.5046 20.8664 14.3826 20.9188C14.2606 20.9712 14.1294 20.9988 13.9966 20.9999C13.8638 21.0011 13.7322 20.9758 13.6093 20.9255C13.4864 20.8752 13.3747 20.801 13.2808 20.7071C13.1869 20.6132 13.1127 20.5015 13.0624 20.3787C13.0121 20.2558 12.9868 20.1241 12.988 19.9913C12.9891 19.8585 13.0167 19.7273 13.0691 19.6053C13.1215 19.4833 13.1977 19.3729 13.2932 19.2807L17.2932 15.2807C17.4807 15.0932 17.735 14.9879 18.0002 14.9879C18.2654 14.9879 18.5197 15.0932 18.7072 15.2807L22.7072 19.2807C22.8947 19.4682 23 19.7225 23 19.9877C23 20.2529 22.8947 20.5072 22.7072 20.6947Z" fill="black" /> </svg>
        </button>
      </Show>

    </div>
  );
};

const CustomerInfoInput = ({ onAddClick }) => {
  let nameRef, contactRef, addressRef;
  const onAClick = () => {
    onAddClick([
      (nameRef.value || ""),
      (contactRef.value || 0),
      (addressRef.value || "")
    ])
  }
  return (
    <div className="flex flex-col flex-1 px-2 border-gray-3 border-r-1 gap-4">
      <h3 className="text-dark-600 text-center relative text-lg" > for take away or remote delivery </h3>
      <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
        <span className="text-dark-600 text-left relative min-w-21 font-medium" > Name </span>
        <input ref={nameRef} className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
      </div>

      <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
        <span className="text-dark-600 text-left relative min-w-21 font-medium" > Contact </span>
        <input ref={contactRef} type="number" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
      </div>
      <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
        <span className="text-dark-600 text-left relative min-w-21 font-medium" > Address </span>
        <input ref={addressRef} className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
      </div>
      <button onClick={onAClick} className="text-white bg-slate-900 hover:bg-slate-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-auto">Add Info</button>
    </div>
  )
}

export default ({ setCreateOrderIsOpen, existOrder }) => {
  const [options, { mutate, refetch }] = createResource(1, fetchMenu);
  const {
    currentOrder, setCustomer, addExtraOption,
    addItem, removeItem, currentOrderTotal,
    commitOrder, resetOrder, setDelivery,
    confirmOrder, payOrder, voidOrder
  } = createOrder(existOrder);
  // create / customer / order_sending
  const [stage, setStage] = createSignal('create');
  const onConfirmClick = () => {
    if (stage() === 'create') {
      setStage('customer');
    }
    else if (stage() === 'customer') {
      onCustomerInfoDineIn();
    }
    else if (stage() === 'payment_success' || stage() === 'payment_fail') {
      setCreateOrderIsOpen(false)
    }
    // commitOrder().then()
  };
  const onCancelClick = () => {

    if (stage() === 'create' || stage() === 'customer' || stage() === 'payment_success') {
      resetOrder();
    } else {
      voidOrder();
    }
    setTimeout(() => setCreateOrderIsOpen(false), 100);

  }
  const onItemAddClick = (product, extra_option) => {
    addItem(product, extra_option);
  };
  const onItemRemoveClick = (order_item) => {
    // console.log(order_item)
    removeItem(order_item);
  };


  // customer info 
  const onCustomerInfoAdd = (info) => {
    setCustomer(...info);
    setDelivery("take_away")
    setStage('order_sending');
    commitOrder().then(() => {
      confirmOrder().then((r) => {
        setStage('payment')
      })
    })
  }
  const onCustomerInfoDineIn = () => {
    setCustomer("-", -1, "-");
    setDelivery("dine_in");
    setStage('order_sending');
    commitOrder().then(() => {
      confirmOrder().then((r) => {
        setStage('payment')
      })
    })
  }


  // /payment
  const onDebitCardClick = () => {
    payOrder().then(() => {
      setStage('payment_success')
    }).catch(() => {
      setStage('payment_fail')
    })
  }


  return (
    <Portal>
      <Dialog title="Create Order"
        onCloseClick={onCancelClick}
        onCancelClick={onCancelClick}
        onConfirmClick={onConfirmClick}
      >
        <div className="max-h-full min-h-50vh flex py-1.5 w-full">
          <Switch>
            <Match when={['payment', 'payment_success', 'payment_fail'].includes(stage()) === false}>

              <div className="flex flex-col  w-65% overflow-y-scroll scrollbar-hide bg-white dark:bg-gray-900 text-gray-900 dark:text-white ">
                <Switch>
                  <Match when={stage() === 'create'}>

                    <Suspense fallback={spinner}>
                      <For each={options()}>
                        {(option_item, i) => (
                          <ProductListItem
                            item={option_item}
                            currentOrder={currentOrder}
                            onItemAddClick={onItemAddClick}
                          />)}
                      </For>
                    </Suspense>
                  </Match>
                  <Match when={stage() === 'customer'}>
                    <h2 className="text-dark-600 text-left relative text-lg" > Customer Detail </h2>
                    <div class="flex w-full py-2 h-full">
                      <CustomerInfoInput onAddClick={onCustomerInfoAdd} />
                      <div className="flex flex-col flex-1 px-2">
                        <h3 className="text-dark-600 text-center  relative text-lg"> Just Dine in </h3>
                        <button onClick={onCustomerInfoDineIn} className="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-600 mt-auto">Dine in</button>
                      </div>
                    </div>
                  </Match>
                  <Match when={stage() === 'order_sending'}>
                    <spinner></spinner>
                    <span>loading</span>
                  </Match>
                  <Match when={stage() === 'order_fail'}>
                    <spinner></spinner>
                    <span>Fail</span>
                  </Match>
                </Switch>
              </div>
              <div className="border-l-1 border-coolGray w-35% flex flex-col pl-1">
                <div className="flex flex-col grow-1 overflow-y-auto scrollbar-hide">
                  <Suspense fallback={spinner}>
                    <For each={currentOrder.items}>
                      {(order_item, i) => (
                        <OrderInPending
                          item={order_item}
                          referMenu={options()}
                          onItemRemoveClick={onItemRemoveClick} />)}
                    </For>
                  </Suspense>
                </div>
                <div className="bg-light-100 border-t-1 border-b-1 border-solid items-center border-[#cbd5e1] pt-0 pr-2 pb-0 pl-2 flex flex-row gap-0 items-start justify-start w-[392px] h-[59px] relative overflow-hidden" >
                  <span className="text-dark-600 self-center  text-left p-l-2 h-6 flex items-center justify-start" > Total: </span>
                  <span className="text-dark-600 text-right line-height-relaxed ml-auto mr-2 min-w-[150px] h-6 flex items-center justify-end" > ${currentOrderTotal(options())}</span>
                </div>
              </div>
            </Match>

            <Match when={stage() === 'payment'}>
              <div className="bg-[#ffffff] rounded-md px-4 flex flex-row gap-0 items-center self-stretch flex-1 relative overflow-hidden">
                <div className="pt-2.5 pr-3 pb-2.5 pl-3 w-auto flex flex-1 flex-col gap-[21px] items-center justify-center shrink-0 relative">
                  <svg
                    className="flex flex-col gap-2.5 items-center justify-center shrink-0 relative overflow-visible"
                    style={{}}
                    width="200"
                    height="200"
                    viewBox="0 0 200 200"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M161.286 49H38.7143C36.0053 49 33.4072 50.0746 31.4917 51.9875C29.5761 53.9004 28.5 56.4948 28.5 59.2V140.8C28.5 143.505 29.5761 146.1 31.4917 148.012C33.4072 149.925 36.0053 151 38.7143 151H161.286C163.995 151 166.593 149.925 168.508 148.012C170.424 146.1 171.5 143.505 171.5 140.8V59.2C171.5 56.4948 170.424 53.9004 168.508 51.9875C166.593 50.0746 163.995 49 161.286 49ZM161.286 59.2V74.5H38.7143V59.2H161.286ZM38.7143 140.8V84.7H161.286V140.8H38.7143Z"
                      fill="black"
                    />
                    <path d="M48.9286 120.4H100V130.6H48.9286V120.4Z" fill="black" />
                  </svg>

                  <div className="text-[#000000] text-center relative w-full h-20 flex items-center justify-center text-xl" >
                    Pay with card
                  </div>

                  <button onClick={onDebitCardClick} className="bg-slate-900 rounded-md pt-2 pr-4 pb-2 pl-4 flex flex-row gap-2.5 items-center justify-center shrink-0 w-[150px] relative">
                    <span className="text-[#ffffff] text-left relative font-medium" > OK </span>
                  </button>
                </div>

                <div className="border-solid border-[#cbd5e1] w-auto pt-2.5 pr-3 pb-2.5 pl-3 flex flex-1 flex-col gap-[21px] items-center justify-center shrink-0 relative border-l-1" >
                  <svg className="shrink-0 relative overflow-visible" width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" > <path d="M29 130.5H171V140.667H29V130.5ZM29 150.833H171V161H29V150.833ZM140.571 69.5C138.565 69.5 136.604 70.0963 134.936 71.2134C133.268 72.3305 131.968 73.9183 131.201 75.7761C130.433 77.6338 130.232 79.6779 130.623 81.6501C131.015 83.6222 131.981 85.4338 133.399 86.8556C134.818 88.2774 136.625 89.2457 138.593 89.638C140.56 90.0303 142.6 89.8289 144.453 89.0594C146.306 88.29 147.89 86.9869 149.005 85.315C150.119 83.6431 150.714 81.6774 150.714 79.6667C150.714 76.9703 149.646 74.3844 147.744 72.4777C145.841 70.5711 143.261 69.5 140.571 69.5ZM100 100C95.9879 100 92.0658 98.8075 88.7299 96.5732C85.3939 94.339 82.7938 91.1633 81.2584 87.4479C79.7231 83.7325 79.3213 79.6441 80.1041 75.6998C80.8868 71.7555 82.8188 68.1325 85.6558 65.2888C88.4928 62.4452 92.1074 60.5086 96.0425 59.724C99.9775 58.9395 104.056 59.3421 107.763 60.8811C111.47 62.4201 114.638 65.0263 116.867 68.3701C119.096 71.7139 120.286 75.6451 120.286 79.6667C120.28 85.0575 118.14 90.2259 114.337 94.0378C110.534 97.8497 105.378 99.9939 100 100ZM100 69.5C97.9939 69.5 96.0329 70.0963 94.3649 71.2134C92.6969 72.3305 91.3969 73.9183 90.6292 75.7761C89.8615 77.6338 89.6607 79.6779 90.052 81.6501C90.4434 83.6222 91.4094 85.4338 92.8279 86.8556C94.2464 88.2774 96.0537 89.2457 98.0212 89.638C99.9887 90.0303 102.028 89.8289 103.882 89.0594C105.735 88.29 107.319 86.9869 108.433 85.315C109.548 83.6431 110.143 81.6774 110.143 79.6667C110.14 76.9711 109.071 74.3868 107.169 72.4807C105.268 70.5747 102.689 69.5027 100 69.5ZM59.4286 69.5C57.4225 69.5 55.4615 70.0963 53.7935 71.2134C52.1255 72.3305 50.8255 73.9183 50.0578 75.7761C49.2901 77.6338 49.0892 79.6779 49.4806 81.6501C49.872 83.6222 50.838 85.4338 52.2565 86.8556C53.675 88.2774 55.4823 89.2457 57.4498 89.638C59.4173 90.0303 61.4567 89.8289 63.3101 89.0594C65.1634 88.29 66.7475 86.9869 67.862 85.315C68.9766 83.6431 69.5714 81.6774 69.5714 79.6667C69.5714 76.9703 68.5028 74.3844 66.6007 72.4777C64.6985 70.5711 62.1186 69.5 59.4286 69.5Z" fill="black" /> <path d="M160.857 120.333H39.1429C36.4549 120.326 33.879 119.253 31.9783 117.348C30.0776 115.443 29.0068 112.861 29 110.167V49.1667C29.0068 46.4724 30.0776 43.8904 31.9783 41.9853C33.879 40.0802 36.4549 39.0068 39.1429 39H160.857C163.545 39.0068 166.121 40.0802 168.022 41.9853C169.922 43.8904 170.993 46.4724 171 49.1667V110.167C170.996 112.862 169.927 115.446 168.025 117.352C166.124 119.257 163.546 120.33 160.857 120.333ZM160.857 49.1667H39.1429V110.167H160.857V49.1667Z" fill="black" /> </svg>

                  <div className="text-[#000000] text-center relative w-full h-20 flex items-center justify-center text-xl" >
                    Pay with Cash
                  </div>

                  <button onClick={onDebitCardClick} className="bg-slate-900 rounded-md pt-2 pr-4 pb-2 pl-4 flex flex-row gap-2.5 items-center justify-center shrink-0 w-[150px] relative">
                    <span className="text-[#ffffff] text-left relative font-medium" > OK
                    </span>
                  </button>
                </div>
              </div>
            </Match>
            <Match when={stage() === 'payment_success'}>
              <div class="flex flex-col m-auto self-center justify-self-center">
                <svg className="mx-auto w-15 h-15 my-2 overflow-visible" width="240" height="240" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg" > <path d="M105 160.605L67.5 123.097L78.0975 112.5L105 139.395L161.887 82.5L172.5 93.1125L105 160.605Z" fill="black" /> <path d="M120 15C99.233 15 78.9323 21.1581 61.6651 32.6957C44.398 44.2332 30.9399 60.632 22.9927 79.8182C15.0454 99.0045 12.9661 120.116 17.0175 140.484C21.069 160.852 31.0693 179.562 45.7538 194.246C60.4383 208.931 79.1475 218.931 99.5155 222.982C119.884 227.034 140.996 224.955 160.182 217.007C179.368 209.06 195.767 195.602 207.304 178.335C218.842 161.068 225 140.767 225 120C225 92.1523 213.938 65.4451 194.246 45.7538C174.555 26.0625 147.848 15 120 15ZM120 210C102.2 210 84.7991 204.722 69.9987 194.832C55.1983 184.943 43.6627 170.887 36.8508 154.442C30.039 137.996 28.2567 119.9 31.7293 102.442C35.202 84.9836 43.7737 68.9471 56.3604 56.3604C68.9471 43.7737 84.9836 35.202 102.442 31.7293C119.9 28.2567 137.996 30.039 154.442 36.8508C170.887 43.6627 184.943 55.1983 194.832 69.9987C204.722 84.7991 210 102.2 210 120C210 143.869 200.518 166.761 183.64 183.64C166.761 200.518 143.869 210 120 210Z" fill="black" /> </svg>
                <h3 className="text-[#000000] text-center w-auto h-10 flex items-center justify-center text-xl" > Order Created </h3>
                <button className="bg-slate-900 rounded-md pt-2 pr-4 pb-2 pl-4 flex flex-row gap-2.5 items-center justify-center w-[150px] ">
                  <span className="text-[#ffffff] text-left relative font-medium" > OK </span>
                </button>
              </div>
            </Match>
            <Match when={stage() === 'payment_fail'}>
              <div class="flex flex-col  m-auto self-center justify-self-center">
                <svg className="mx-auto w-15 h-15 my-2 overflow-visible" width="240" height="240" viewBox="0 0 240 240" fill="none" xmlns="http://www.w3.org/2000/svg" > <path d="M105 160.605L67.5 123.097L78.0975 112.5L105 139.395L161.887 82.5L172.5 93.1125L105 160.605Z" fill="black" /> <path d="M120 15C99.233 15 78.9323 21.1581 61.6651 32.6957C44.398 44.2332 30.9399 60.632 22.9927 79.8182C15.0454 99.0045 12.9661 120.116 17.0175 140.484C21.069 160.852 31.0693 179.562 45.7538 194.246C60.4383 208.931 79.1475 218.931 99.5155 222.982C119.884 227.034 140.996 224.955 160.182 217.007C179.368 209.06 195.767 195.602 207.304 178.335C218.842 161.068 225 140.767 225 120C225 92.1523 213.938 65.4451 194.246 45.7538C174.555 26.0625 147.848 15 120 15ZM120 210C102.2 210 84.7991 204.722 69.9987 194.832C55.1983 184.943 43.6627 170.887 36.8508 154.442C30.039 137.996 28.2567 119.9 31.7293 102.442C35.202 84.9836 43.7737 68.9471 56.3604 56.3604C68.9471 43.7737 84.9836 35.202 102.442 31.7293C119.9 28.2567 137.996 30.039 154.442 36.8508C170.887 43.6627 184.943 55.1983 194.832 69.9987C204.722 84.7991 210 102.2 210 120C210 143.869 200.518 166.761 183.64 183.64C166.761 200.518 143.869 210 120 210Z" fill="black" /> </svg>
                <h3 className="text-[#000000] text-center w-auto h-10 flex items-center justify-center text-xl" > Order Fail </h3>
                <button className="bg-slate-900 rounded-md pt-2 pr-4 pb-2 pl-4 flex flex-row gap-2.5 items-center justify-center w-[150px] ">
                  <span className="text-[#ffffff] text-left relative font-medium" > OK </span>
                </button>
              </div>
            </Match>

          </Switch>
        </div>
      </Dialog>
    </Portal >

  );
};

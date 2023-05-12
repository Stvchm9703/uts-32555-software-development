import { createEffect, createSignal, onMount } from "solid-js";

export const TabNameList = [
  { name: 'order_list', display: 'Order List' },
  { name: 'appointment_list', display: 'Appointment List' },
  { name: 'product_list', display: 'Product List' },
  { name: 'setting', display: 'Setting' }
]
const TabButton = ({ children, onclick, currentTab, tabName }) => {
  //  createEffect(()=>console.log(isActive) , isActive)
  const isActive = () => currentTab() === tabName
  return (
    <button
      class="rounded py-1.5 px-3 flex flex-row gap-2.5 items-start justify-start shrink-0 relative"
      classList={{ 'bg-light-100': isActive() }}
      onClick={onclick}
    >
      <span
        class=" text-slate-700 text-left relative font-sans text-ui"
        classList={{ 'text-slate-700': !isActive(), 'text-slate-900': isActive() }}
      >
        {children}
      </span>
    </button>
  )
}
const TabList = ({ children, onTabChange, onCreateClick }) => {
  const [currentTab, setCurrentTab] = createSignal("order_list")
  const onTabClick = (state) => {
    setCurrentTab(state)
    onTabChange(state);
  };
  onMount(() => {
    onTabChange(currentTab())
  })

  return (
    <div
      class="px-0 py-2 flex flex-row gap-2 items-start justify-start self-stretch shrink-0 h-auto relative overflow-hidden align-baseline items-center"
    >
      <div class="bg-slate-100 rounded-md p-[5px] flex flex-row gap-0 items-start justify-start flex-1 relative">
        <For each={TabNameList}>
          {(tab_set) => (<TabButton onclick={() => onTabClick(tab_set.name)} tabName={tab_set.name} currentTab={currentTab} >{tab_set.display}</TabButton>)}
        </For>
      </div>
      <button
        class="bg-slate-900 rounded py-2 px-4 flex flex-row gap-0 items-center justify-end shrink-0 h-auto relative"
      >
        <span
          class="text-light-100 text-center relative font-medium text-ui"
          onClick={onCreateClick}
        >
          Create Order
        </span>
      </button>

    </div>

  )
}

export default TabList


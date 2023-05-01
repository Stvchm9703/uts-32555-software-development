import { createSignal, onMount } from "solid-js";

const TabList = ({ children, onTabChange }) => {
  const [currentTab, setCurrentTab] = createSignal("order_list")
  const onTabClick = (state) => {
    setCurrentTab(state)
    onTabChange(state);
  };
  onMount(()=>{
    onTabChange(currentTab())
  })

  return (
    <div class="tabs">
      <div class="tab tab-bordered" classList={{ "tab-active": currentTab() === 'order_list' }} onclick={() => onTabClick('order_list')} >Order List</div>
      <div class="tab tab-bordered" classList={{ "tab-active": currentTab() === 'create_order' }} onclick={() => onTabClick('create_order')}>Create Order</div>
      <div class="tab tab-bordered" classList={{ "tab-active": currentTab() === 'setting' }} onclick={() => onTabClick('setting')} >Setting</div>
    </div>
  )
}

export default TabList
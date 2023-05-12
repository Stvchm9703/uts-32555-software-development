import { Show, createSignal } from "solid-js";
import TabList from "./tab";
import { Dynamic } from "solid-js/web";
import { lazy } from "solid-js";

// import 'flowbite';

const tabPageSetting = {
  order_list: lazy(() => import("./tab-order-list")),
  // create_order: lazy(() => import('./tab-create-order')),
  appointment_list: lazy(()=> import('./tab-table-appointment')),
  
}

function App() {
  const [greetMsg, setGreetMsg] = createSignal("");
  const [name, setName] = createSignal("");
  const [tabPage, setTabPage] = createSignal("");
  const [createOrderIsOpen, setCreateOrderIsOpen] = createSignal(false);
  const onTabChange = (val) => {
    setCreateOrderIsOpen(false);
    setTabPage(val);
  }

  return (
    <div class="container max-w-288 w-full mx-auto p-2 block">
      <TabList onTabChange={onTabChange} onCreateClick={() => setCreateOrderIsOpen(true)} />

      <div class="py-2">
        <Dynamic
          component={tabPageSetting[tabPage()]}
          createOrderIsOpen={createOrderIsOpen}
          setCreateOrderIsOpen={setCreateOrderIsOpen} />

      </div>

      {tabPage()}

    </div>
  );
}






export default App;

import { Show, createSignal } from "solid-js";
import TabList from "./Tab";
import { Dynamic } from "solid-js/web";
import { lazy } from "solid-js";

const tabPageSetting = {
  order_list: lazy(() => import("./tab-order-list")),
  create_order: lazy(() => import('./tab-create-order')),
}

function App() {
  const [greetMsg, setGreetMsg] = createSignal("");
  const [name, setName] = createSignal("");
  const [tabPage, setTabPage] = createSignal("");
  return (
    <div class="container max-w-288 w-full mx-auto p-2 block">
      <TabList onTabChange={setTabPage} />

      <div class="py-2">
        <Dynamic component={tabPageSetting[tabPage()]}></Dynamic>

      </div>

      {tabPage()}

    </div>
  );
}






export default App;

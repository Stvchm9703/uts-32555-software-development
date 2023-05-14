
import { Portal } from "solid-js/web";
import spinner from "./spinner";
import { For, Suspense, createResource, Show, Switch, createSignal, lazy } from "solid-js";
import createOrder from "./composition/order/use-order";
import { fetchProduct } from "./composition/order/product";
import Dialog from "./dialog";

export default ({ setCreateOrderIsOpen }) => {
  const onFormSubmit = ({ }) => { }
  const onCancelClick = () => {
    setCreateOrderIsOpen(false)
  }
  return (
    <Portal>
      <Dialog title="Create Appointment"
        onCloseClick={() => setCreateOrderIsOpen(false)}
        onCancelClick={onCancelClick}
      >
        <div className="max-h-full flex py-1.5 w-full">
          <div className=" flex flex-col  w-65% overflow-y-scroll bg-white dark:bg-gray-900 text-gray-900 dark:text-white scrollbar-hide">

            <div className="flex flex-col gap-2 items-start justify-start self-stretch shrink-0 relative">
              <h2 className="text-dark-600 text-left relative self-stretch font-medium" > Appointment Information </h2>
              <span className="text-slate-400 text-left relative self-stretch text-md" > Set the Customer Information for Table Appointment </span>
            </div>

            <div className="py-3 px-0 flex flex-col gap-2 items-start justify-start shrink-0 w-full h-auto relative">
              <h3 className="text-dark-600 text-left relative text" > Customer Detail </h3>
              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > Name </span>
                <input className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>

              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > Contact </span>
                <input type="number" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>
              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > Address </span>
                <input className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>
            </div>
            <div className="py-3 px-0 flex flex-col gap-2 items-start justify-start shrink-0 w-full relative">
              <h3 className="text-dark-600 text-left relative" > Appointment Detail </h3>
              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > Count </span>
                <input type="number" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>

              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > Start time </span>
                <input type="datetime-local" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>
              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > End time </span>
                <input type="datetime-local" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>
            </div>

            <div className="pt-[18px] pr-0 pb-[18px] pl-0 flex flex-col gap-2 items-start justify-start shrink-0 w-[706px] h-[191px] relative">
              <h3 className="text-dark-600 text-left relative" > Other </h3>
              <div className="flex flex-row gap-4 items-center justify-start self-stretch shrink-0 relative">
                <span className="text-dark-600 text-left relative min-w-21 font-medium" > remark </span>
                <textarea type="text" height="40px" className="bg-light-100 rounded-md border-solid border-[#cbd5e1] border pt-2 pr-14 pb-2 pl-3 flex flex-row gap-0 items-center justify-start self-stretch shrink-0 relative text-slate-900 text-left" />
              </div>
            </div>
          </div>

          <div className="border-l-1 border-coolGray w-35% flex flex-col overflow-y-scroll">
            <div className="flex flex-1 flex-col overflow-y-auto scrollbar-hide">

            </div>
            <div className="bg-light-100 border-t-1 border-b-1 border-solid items-center border-[#cbd5e1] pt-0 pr-2 pb-0 pl-2 flex flex-row gap-0 items-start justify-start w-[392px] h-[59px] relative overflow-hidden" >
              <span className="text-dark-600 self-center  text-left p-l-2 h-6 flex items-center justify-start" >
                Total:
              </span>
              <span className="text-dark-600 text-right line-height-relaxed ml-auto mr-2 min-w-[150px] h-6 flex items-center justify-end" >
                $25
              </span>
            </div>

          </div>
        </div>
      </Dialog>
    </Portal>

  );
}
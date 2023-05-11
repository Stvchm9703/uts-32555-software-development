import { createSignal } from "solid-js";

const InputField = ({ onSearchEnter }) => {

  let input_ref;
  const onSearchClick = () => {
    onSearchEnter && onSearchEnter(input_ref.value);
  }
  const onInputEnter = (e) => (e.key === 'Enter') && onSearchClick();

  return (
    <div
      class="rounded  flex flex-col gap-2.5 items-start justify-start shrink-0 w-full relative"
    >
      <div
        class="bg-slate-100 rounded-md py-2.5 pr-2 pl-4 flex flex-row gap-2 items-center justify-start self-stretch shrink-0 h-11 relative"
      >
        <svg
          class="shrink-0 relative overflow-visible"
          style=""
          width="17"
          height="17"
          viewBox="0 0 17 17"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M7.83333 13.1667C10.7789 13.1667 13.1667 10.7789 13.1667 7.83333C13.1667 4.88781 10.7789 2.5 7.83333 2.5C4.88781 2.5 2.5 4.88781 2.5 7.83333C2.5 10.7789 4.88781 13.1667 7.83333 13.1667Z"
            stroke="#0F172A"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M14.5 14.5L11.6 11.6"
            stroke="#0F172A"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <input
          ref={input_ref}
          class="text-slate-400 bg-slate-100 text-left relative shrink-0 grow-1 border-0 h-10"
          type="search"
          placeholder="Type a command or search..."
          onKeyDown={onInputEnter}
        >
          Type a command or search...
        </input>
        <button class="text-white  font-medium rounded-md text-sm px-4 py-1 bg-slate-900" onClick={onSearchClick}>Search</button>
      </div>
    </div>

  );
};

export default InputField;

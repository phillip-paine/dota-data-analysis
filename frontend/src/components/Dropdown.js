import React, { useState, useEffect, useRef } from "react";
import "../styles/Dropdown.css";

const Icon = () => {
  return (
    <svg height="20" width="20" viewBox="0 0 20 20">
      <path d="M4.516 7.548c0.436-0.446 1.043-0.481 1.576 0l3.908 3.747 3.908-3.747c0.533-0.481 1.141-0.446 1.574 0 0.436 0.445 0.408 1.197 0 1.615-0.406 0.418-4.695 4.502-4.695 4.502-0.217 0.223-0.502 0.335-0.787 0.335s-0.57-0.112-0.789-0.335c0 0-4.287-4.084-4.695-4.502s-0.436-1.17 0-1.615z"></path>
    </svg>
  );
};

const Dropdown = ({ placeHolder, options, isSearchable }) => {
  const [showMenu, setShowMenu] = useState(false);
  const [selectedValue, setSelectedValue] = useState(null); /* select dropdown value */
  const [searchValue, setSearchValue] = useState("");
  const searchRef = useRef();
  const inputRef = useRef(); /* issue is here if we have two dropdown lists then e.stopPropagation
  will prevent the eventListener from being activated again if dropdown 1 already open and we want to open another */
  /* useEffect contents are executed when specified, e.g. useEffect(() => { function contents.. }, []
  means that the function contents are executed on load of the page (e.g. refresh) (empty array() = on load) */
  /* this function inside useEffect will set the showMenu to False when the user clicks somewhere in the window */
  useEffect(() => {
   const handler = (e) => {
       if (inputRef.current && inputRef.current.contains(e.target)){
           setShowMenu(false);
       }
   };

   window.addEventListener("click", handler);
   /* we attach the EventListener on click to setShowMenu to False then we detach because window is now closed
   and we will want to be able to attach it again later if the menu is reopened */
   return () => {
    window.removeEventListener("click", handler);
   };
  });
  /* this function is for the search in the dropdown list - the code inside useEffect is executed when
   showMenu is true, e.g. when it is opened */
  useEffect(() => {
   setSearchValue("");
   if (showMenu && searchRef.current){
    searchRef.current.focus();
   }
  }, [showMenu]);

  /* add the search handlers - these deal with what happens when we are searching the dropdown list */
  const onSearch = (e) => {
   setSearchValue(e.target.value);
  };

  const getOptions = () => {
   if (!searchValue){ /*if nothing searched yet then return all options */
    return options;
   }
   return options.filter((option) =>
        option.label.toLowerCase().indexOf(searchValue.toLowerCase()) >= 0);
  };


  const handleInputClick = (e) => {
   setShowMenu(!showMenu); /* this no longer needs stopPropagation because the inputRef in the handler */
  };

  const getDisplay = () => {
    if (selectedValue) {
     return selectedValue.label;
    }
    return placeHolder;
  };

  const onItemClick = (option) => {
   setSelectedValue(option);
  };
  /* isSelected will check if option is the selected value, if so it returns true, else false */
  const isSelected = (option) => {
    if(!selectedValue) {
     return false;
    }

    return selectedValue.value == option.value;
  };
  /* map onto options a function which checks if any of the options are selected, if so highlights */

  return (
    <div className="dropdown-container">
      <div ref={inputRef} onClick={handleInputClick} className="dropdown-input">
        <div className="dropdown-selected-value">{getDisplay()}</div>
                <div className="dropdown-tools">
                  <div className="dropdown-tool">
                    <Icon />
                  </div>
                </div>
        {showMenu && (
         <div className="dropdown-menu">
            {isSearchable && (
                <div className="search-box">
                    <input onChange={onSearch} value={searchValue} ref={searchRef} />
                </div>
            )}
            {getOptions().map((option) => (
                <div
                    onClick={() => onItemClick(option)}
                    key={option.value}
                    className={`dropdown-item ${isSelected(option) && "selected"}`}>
                    {option.label}
                </div>
                )
            )}
        </div>
       )}
      </div>
    </div>
  );
};

export default Dropdown;
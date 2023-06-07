import './styles/App.css';
import './styles/DropdownSelect.css';
import { useState } from 'react';
import DropdownSelect from './components/DropdownSelect';

const App = () => {

    const options = [
        {value: 'chocolate', label: "Chocolate"},
        {value: 'vanilla', label: "Vanilla"}
    ]

    /* we don't want to be able to select hero more than once, so once selected in a dropdown
    we need to remove it from future dropdown selections */


    return (
        <div className="App">
            <h1>Welcome</h1>
            <div className="DropdownRow">
                <DropdownSelect options={options} placeholder="Select a hero" />
                <DropdownSelect options={options} placeholder="Select second hero" />
            </div>
        </div>
    );
}

export default App
import './styles/App.css';
import { useState } from 'react';
import DropdownSelect from './components/DropdownSelect';

const App = () => {

    const options = [
        {value: 'chocolate', label: "Chocolate"},
        {value: 'vanilla', label: "Vanilla"}
    ]

    return (
        <div className="App">
            <h1>Welcome</h1>
            <DropdownSelect options={options} placeholder="Select a hero" />
        </div>
    );
}

export default App
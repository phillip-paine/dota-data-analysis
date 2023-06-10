import './styles/App.css';
import { useState } from 'react';
import Dropdown from './components/Dropdown';

const App = () => {

    const options = [
        { value: "green", label: "Green" },
        { value: "blue", label: "Blue" },
        { value: "yellow", label: "Yellow" }
    ];

    return (
    <div className="App">
        <h1>Welcome</h1>
        <Dropdown isSearchable placeHolder="Select ..." options={options} />
    </div>
    );
}

export default App;
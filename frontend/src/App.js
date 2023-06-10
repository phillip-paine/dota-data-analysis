import './styles/App.css';
import { useState } from 'react';
import DropdownSelect from './components/DropdownSelect';

const App = () => {

    const [dropdownValue, setDropdownValue] = useState(null)
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
                <DropdownSelect
                    options={options}
                    isSearchable
                    placeholder="Radiant hero 1"
                />
                <DropdownSelect
                    options={options}
                    isSearchable
                    placeholder="Dire hero 1"
                />
            </div>
            <div className="DropdownRow">
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Radiant hero 2" />
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Dire hero 2" />
            </div>
            <div className="DropdownRow">
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Radiant hero 3" />
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Dire hero 3" />
            </div>
            <div className="DropdownRow">
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Radiant hero 4" />
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Dire hero 4" />
            </div>
            <div className="DropdownRow">
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Radiant hero 5" />
                <DropdownSelect options={options} isSearchable={true} isClearable placeholder="Dire hero 5" />
            </div>

        </div>
    );
}

export default App
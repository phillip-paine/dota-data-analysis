import React, { useState } from 'react';
import Select from 'react-select';
import '../styles/DropdownSelect.css';


const DropdownSelect = ({ options, placeholder }) => {

    return (
        <Select
        className="basic-single"
        classNamePrefix="select"
        isSearchable
        placeholder={placeholder}
        options={options}
        />

    );
};

export default DropdownSelect;
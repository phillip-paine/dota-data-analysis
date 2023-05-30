import React, { useState } from 'react';
import Select from 'react-select';

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
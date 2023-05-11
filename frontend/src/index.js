import "../src/index.css";

import App from "../src/App";
import React from "react";
import ReactDOM from "react-dom";

ReactDOM.render(
    <React.StrictMode>
        <App />  // this is short hand for react.createElement(App) which will create the component App instance
        // and render it to the DOM
    </React.StrictMode>,
    document.getElementById("root")
);

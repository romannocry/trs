import React, { useState, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

function ClickCounter() {
    const [count, setCount] = useState(0);
   // const Form = RJSFSchema;
    console.log("loading counter");
    return (
    <div>
          <div>
          Timer
        <button onClick={() => setCount(count + 1)}>
          Clicked ${count} times
        </button>
      </div>
      </div>
    );
  }

export default ClickCounter;

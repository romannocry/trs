import React, { useState, useEffect, useRef } from 'react';
import { JsonForms } from '@jsonforms/react';
import { person } from '@jsonforms/examples';
import {
  materialRenderers,
  materialCells,
} from '@jsonforms/material-renderers';
import { BrowserRouter, HashRouter, Link, Route, useParams } from "react-router-dom";
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
//Goal of Model Links is to give the links to:
// - fast fill up to 2 attributes without seeing the form - close on post
// - fast fill up to 2 attributes and arrive on the form page for full completion
// - full form without fast fill

const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"

function Form()  {
    const [schema, setSchema] = useState({});
    const [model, setModel] = useState({});
    const [data, setData] = useState({});
    const componentIsMounted = useRef(true);
    const { objectModelId } = useParams();
    console.log("loading Form")
    useEffect(() => {
      fetch('http://'+prod_ip+':8000/api/models/'+objectModelId, {
        method: 'GET',
        headers: {
         'Content-Type': 'application/json',
         'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
        },
     })
     .then((response) => response.json())
     .then((data) => {
        console.log(data);
        setSchema(data.object_model)
        // Handle data
     })
     .catch((err) => {
        console.log(err.message);
     });
        return () => {
        componentIsMounted.current = false;
        };
    }, []);

    const handleSubmit = () =>{
        console.log(data)
    }
  return (
    <div>
          <JsonForms
              schema={schema}
              //uischema={uischema}
              data={data}
              renderers={materialRenderers}
              cells={materialCells}
              onChange={({ data, errors }) => setData(data)}
            />
          <Button variant="contained" endIcon={<SendIcon />} onClick={() => handleSubmit()}>
            Validate
          </Button>
    </div>

  );
}

export default Form;

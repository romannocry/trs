import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, HashRouter, Link, Route, useParams } from "react-router-dom";
import {Buffer} from 'buffer';

//Goal of Model Links is to give the links to:
// - fast fill up to 2 attributes without seeing the form - close on post
// - fast fill up to 2 attributes and arrive on the form page for full completion
// - full form without fast fill
const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"

const ModelLinks = (props:any) => {
    const [model, setModel] = useState<any>({});
    const componentIsMounted = useRef(true);
    const { objectModelId } = useParams();
    const encodedString = Buffer.from('your string here').toString('base64');


    console.log("loading model")
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
        setModel(data)
        // Handle data
     })
     .catch((err) => {
        console.log(err.message);
     });
        return () => {
        componentIsMounted.current = false;
        };
    }, []);
  return (
    <div>
        <>{JSON.stringify(model.object_model.properties)}
        {encodedString}
        </>
    </div>

  );
}

export default ModelLinks;

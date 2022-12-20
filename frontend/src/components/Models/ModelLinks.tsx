import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, HashRouter, Link, Route, useParams } from "react-router-dom";
import {Buffer} from 'buffer';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

//Goal of Model Links is to give the links to:
// - fast fill up to 2 attributes without seeing the form - close on post
// - fast fill up to 2 attributes and arrive on the form page for full completion
// - full form without fast fill
const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"

const ModelLinks = (props:any) => {
  const [firstSelection, setFirstSelection] = useState<any>();
  const [secondSelection, setSecondSelection] = useState<any>();
  const [model, setModel] = useState<any>({});
  const [modelProps, setModelprops] = useState<any>([]);
  const [test, setTest] = useState<any>([]);
  const componentIsMounted = useRef(true);
  const { objectModelId } = useParams();
  const encodedString = Buffer.from('your string here').toString('base64');


    console.log("loading model")
    useEffect(() => {
      test.push(1)
      console.log(test)
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
        let enum_options: any[] = []


        Object.keys(data.object_model['properties']).map((key, index) => {
          if ('enum' in data.object_model['properties'][key]) {
            console.log("enum value found in attribute "+key)
            enum_options.push({'key':key,'value':data.object_model['properties'][key]})
          }

        })
        console.log(enum_options)
        // check if key exists
        //const hasKey = 'name' in person;
          
        setModelprops(enum_options)
        //console.log(data.object_model['properties'])
        // Handle data
     })
     .catch((err) => {
        console.log(err.message);
     });
        return () => {
        componentIsMounted.current = false;
        };
    }, []);

    const handleChange1 = (event: SelectChangeEvent) => {
      console.log("1 change")
      setFirstSelection(event.target.value as string);
    };

    const handleChange2 = (event: SelectChangeEvent) => {
      console.log("2 change")
      setSecondSelection(event.target.value as string);
    };
  return (
    <div>
        <>
        <h1>Model</h1>
        <h4>{JSON.stringify(modelProps)}</h4>
        <h4>{typeof(modelProps)}</h4>
        <h4>{typeof(test)}</h4>
        {modelProps.map((item: any,index: any) => {
        return (
          <li key={index}>{item.key}</li>
        )     
        })}
        <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Second data point</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={secondSelection}
          label="Field 2"
          onChange={handleChange2}
        >
          {modelProps.map((item: any,index: any) => {
            return(
            <MenuItem  key={index} value={item.key}>{item.key}</MenuItem>
            )
          })}

        </Select>
        </FormControl>
        </>
    </div>

  );
}

export default ModelLinks;

/*
      <>
        <h1>Model</h1>
        <h4>{JSON.stringify(modelProps)}</h4>
        {modelProps.map((model:any) => {
        return (
          <div key={model.key}>
            <h2>k: {model.key}</h2>
            <h2>v: {model.value}</h2>

            <hr />
          </div>
          );
        })}
        <h1>Links of direct form</h1>
        <h4><a target='_blank' href={'http://localhost:3000/forms/' +objectModelId}>http://localhost:3000/forms/{objectModelId}</a></h4>
        <h1>Fast Voting (valid when 2 attributes of enum type)</h1>
        <h4>Select 1 or 2 </h4>
        <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">First data point</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={firstSelection}
          label="Field1"
          onChange={handleChange1}
        >

        </Select>
        </FormControl>

        <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Second data point</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={secondSelection}
          label="Field 2"
          onChange={handleChange2}
        >
          {Object.keys(modelProps).map((name) => (
            <MenuItem
              key={name}
              value={name}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
        </FormControl>
        Selection:
        - {firstSelection}
        - {secondSelection}

          {JSON.stringify(modelProps)}
 
        </>
*/
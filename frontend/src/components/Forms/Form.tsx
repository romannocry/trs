import React, { useState, useEffect, useRef } from 'react';
import { JsonForms } from '@jsonforms/react';
import { object, person } from '@jsonforms/examples';
import {
  materialRenderers,
  materialCells,
} from '@jsonforms/material-renderers';
import { BrowserRouter, HashRouter, Link, Route, useParams } from "react-router-dom";
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import CircularProgress from '@mui/material/CircularProgress';
import {Buffer} from 'buffer';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'


const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"

function Form()  {
    const [schema, setSchema] = useState({});
    const [model, setModel] = useState({});
    const [data, setData] = useState<any>({});
    const componentIsMounted = useRef(true);
    const { objectModelId } = useParams();
    const { payload } = useParams();
    const { type } = useParams();
    const typeRef = useRef(false);
    const [isLoading, setIsLoading] = useState(false);

    //console.log("loading Form")
    useEffect(() => {
      setIsLoading(true);
      fetch('http://'+prod_ip+':8000/api/models/'+objectModelId, {
        method: 'GET',
        headers: {
         'Content-Type': 'application/json',
         'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
        },
     })
     .then((response) => response.json())
     .then((data) => {
        setSchema(data.object_model)
        //setData(JSON.parse(Buffer.from(String(payload), 'base64').toString('ascii')))
        setIsLoading(false)   // Hide loading screen 
     })
     .catch((err) => {
        console.log(err.message);
        setIsLoading(false)   // Hide loading screen 
     });
        return () => {
        componentIsMounted.current = false;
        };
    }, []);

    useEffect(() => {
      if (typeRef.current) return;
      typeRef.current = true;
      //console.log(payload)
      //handleUrlSubmission(payload)
      //setData(JSON.parse(Buffer.from(String(payload), 'base64').toString('ascii')))
      switch(type) {
        case 'fast':
          console.log("fast")
          //handleSubmit(payload)
          break;
        case 'admin':
          console.log("admin")
          break;
        case 'moderator':
          console.log("moderator")
          break;
        default:
          console.log("default")
          break;
      }
    }, [type]);


    const handleUrlSubmission = (payload: any) =>{     
      const MySwal = withReactContent(Swal)
      console.log(payload)
      const encodedData = Buffer.from(JSON.stringify(payload)).toString('base64');
      //console.log(encodedData)
      fetch('http://localhost:8000/api/transaction/'+objectModelId+'/'+encodedData, {
        method: 'POST',
        headers: {
          'mode': 'no-cors',
         'Content-Type': 'application/json',
         'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
        },
        //body: JSON.stringify(trs_model)

     })
     .then((response) => response.json())
     .then((data) => {
        console.log(data);
        let timerInterval   
        MySwal.fire({
            //position: 'top-end',
            icon: 'success',
            title: 'Thanks for your input!',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            didOpen: () => {
              MySwal.showLoading(null);
            },
            didClose: () => {
              console.log('closing')
              //navigate('/links/'+data.$oid);
            }
          })
        
     })
     .catch((err) => {
        console.log(err.message);
        MySwal.fire({
          //position: 'top-end',
          icon: 'error',
          title: err.message,
          showConfirmButton: false,
          timer: 4000,
          timerProgressBar: true,
          didOpen: () => {
            MySwal.showLoading(null);
          },
          didClose: () => {
            console.log('closing')
            //navigate('/links/'+data.$oid);
          }
        })
     });
        return () => {
        //componentIsMounted.current = false;
        };
      
    };

    const handleSubmit = (closingParams: any) =>{     
      const MySwal = withReactContent(Swal)
      console.log(data)
      const encodedData = Buffer.from(JSON.stringify(data)).toString('base64');
      //console.log(encodedData)
      fetch('http://127.0.0.1:8000/api/transaction/'+objectModelId+'/'+encodedData, {
        method: 'POST',
        headers: {
         'Content-Type': 'application/json',
         'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
        },
        //body: JSON.stringify(trs_model)

     })
     .then((response) => response.json())
     .then((data) => {
        console.log(data);
        let timerInterval   
        MySwal.fire({
            //position: 'top-end',
            icon: 'success',
            title: 'Thanks for your input!',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
            didOpen: () => {
              MySwal.showLoading(null);
            },
            didClose: () => {
              console.log('closing')
              //navigate('/links/'+data.$oid);
            }
          })
        
     })
     .catch((err) => {
        console.log(err.message);
     });
        return () => {
        //componentIsMounted.current = false;
        };
      
    };


  return (
    <div>
          {isLoading ? <CircularProgress />: <JsonForms schema={schema} data={data} renderers={materialRenderers} cells={materialCells} onChange={({ data, errors }) => setData(data)}/>}
          
          <Button variant="contained" endIcon={<SendIcon />} onClick={() => handleSubmit(null)}>
            Validate
          </Button>
          <Button variant="contained" endIcon={<SendIcon />} onClick={() => handleUrlSubmission(data)}>
            handle URL submission
          </Button>
    </div>

  );
}

export default Form;

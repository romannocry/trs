'use strict';
const { createElement, useState, useEffect, useRef } = React;
const { withReactContent } = sweetalert2ReactContent;
const { BrowserRouter, HashRouter, Link, Route, NavLink, Switch, useParams} = ReactRouterDOM;
//import Form from "@rjsf/core"; // 4.2.2

//const { rjsf } = rjsf
//import AgGridReact from  'https://unpkg.com/@ag-grid-community/react@23.0.0/umd/ag-grid-react.min.js'
//const { columnDefs, rowData, AgGridReact as ''} = AgGridReact
//const { button, Tab, Tabs } = ReactBootstrap;
//const { Card } = ReactCardFlip;
//import CountryList from './CountryList' ;
const render = ReactDOM.render;
const html = htm.bind(createElement);
//const MySwal = withReactContent(Swal)
//import Swal from 'sweetalert2'
//const MySwal = withReactContent(Swal)


function ClickCounter(props) {
  const [count, setCount] = useState(0);
 // const Form = RJSFSchema;
  console.log("loading counter");
  console.log(props.params)
  const { test } = useParams();
  const { test1 } = useParams();
  console.log(test)
  console.log(test1)
  return html`
  <div>
        <div>
        Timer
      <button onClick=${() => setCount(count + 1)}>
        Clicked ${count} times
      </button>
    </div>
    </div>
  `;
}
function createModel(props) {
  const [count, setCount] = useState(0);
  console.log("loading counter");
  console.log(props.params)
  const { test } = useParams();
  const { test1 } = useParams();
  console.log(test)
  console.log(test1)
  return html`
  <div>
        <div>
        MODEL
      <button onClick=${() => setCount(count + 1)}>
        Clicked ${count} times
      </button>
    </div>
    </div>
  `;
}

function getModels() {
  const [models, setModels] = useState([]);

  const componentIsMounted = useRef(true);
  console.log("loading Models List")

  useEffect(() => {
    fetch('/api/models', {
      method: 'GET',
      /*body: JSON.stringify({
         title: title,
         body: body,
         userId: Math.random().toString(36).slice(2),
      }),*/
      headers: {
       'Content-Type': 'application/json',
       'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
      },
   })
   .then((response) => response.json())
   .then((data) => {
      console.log(data);
      
      setModels(data)
      // Handle data
   })
   .catch((err) => {
      console.log(err.message);
   });
      return () => {
      componentIsMounted.current = false;
      };
  }, []);
  
  return html`
  <div>
    ${models.map((model, index) => (
      html`<${Model} model=${model} key=${index}/>`
  ))}
  </div>
  `;
}

//Model Card component
const Model = props => {
  const [modelState, setModelState] = useState(props);
  //<ul class="c-table__row" onClick=${() => alert(modelState.index)}>
  return html`
  <div class="card" width='300px'>
  ${modelState.model.object_name}
  
  <a href="/transactions/${modelState.model._id_$oid}" class="card-link">${modelState.model._id_$oid}</a>

  </div>  
  
  `
};

function insertTransaction() {

  const { objectModelId } = useParams();
  const { payload } = useParams();

  // Using Fetch API
  fetch('/api/transaction/'+objectModelId+'/'+payload, {
     method: 'POST',
     /*body: JSON.stringify({
        title: title,
        body: body,
        userId: Math.random().toString(36).slice(2),
     }),*/
     headers: {
      'Content-Type': 'application/json',
      'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
     },
  })
  .then((response) => response.json())
  .then((data) => {
     console.log(data);
     // Handle data
  })
  .catch((err) => {
     console.log(err.message);
  });
  
  return html`
  <div>
    GRACIAS
    </div>
  `;
}

function showTansactions() {
  const { objectModelId } = useParams();
  const [transactions, setTransactions] = useState([]);
  const [socketMessage, setSocketMessage] = useState([]);
  const [defaultColDef, setDefaultColDef] = useState([]);
  const [rowData, setRowData] = useState([]);
  const [columnDefs, setColumnDefs] = useState([])
  const [gridOptions, setGridOptions] = useState([])
  const gridApiRef = useRef(null)
  const gridOptionsRef = useRef(null)
  const [count, setCount] = useState(0);
  const socketRef = useRef(false);
  const getGridData = (objectModelId) => {
      console.log("showTransaction")
      // Using Fetch API
      fetch('/api/transactions/'+objectModelId, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authorization': JSON.stringify({'id':1,'username':'roman','email':'babe'})        
        },
    })
    .then((response) => response.json())
    .then((data) => {
      //console.log( JSON.parse(data).data);
      setTransactions(JSON.parse(data).data)
      if (!Array.isArray(JSON.parse(data).data) || !JSON.parse(data).data.length) {
        // array does not exist, is not an array, or is empty
            console.log("empty")
            gridApiRef.current.setColumnDefs([])
            gridApiRef.current.setRowData([])
        } else {
            const colDefs = []//gridOptions.api.getColumnDefs();
            colDefs.length=0;
            const keys = Object.keys(JSON.parse(data).data[0])
            keys.forEach(key => colDefs.push({field : key}));
            gridApiRef.current.setColumnDefs(colDefs)
            gridApiRef.current.setRowData(JSON.parse(data).data)
            
      }    
    })
      
    .catch((err) => {
        console.log(err.message);
    });

  };

  const onGridReady = (params) => {
    params.api.resetRowHeights();
    console.log("grid ready")
    gridApiRef.current = params.api // <= assigned gridApi value on Grid ready
    gridOptionsRef.current = params
    getGridData(objectModelId);
    setDefaultColDef({
      sortable: true,
      filter: 'agTextColumnFilter',
      resizable: true
  })
}

useEffect(() => {
    if (socketRef.current) return;
    socketRef.current = true;
    console.log(transactions)
    var ws = new WebSocket(`ws://192.168.1.7:8000/feed/transactions/${objectModelId}`);
    ws.onmessage = function(event) {
      //console.log(gridOptionsRef.current)
      //console.log(gridApiRef.current)
      console.log(event)
      var eventData = JSON.parse(event.data);
      var renderedNodes = gridApiRef.current.getRenderedNodes()

      //if no data in array, initiate Grid with event
      if (!Array.isArray(renderedNodes) || !renderedNodes.length) {
        console.log("empty array")
        getGridData(objectModelId)
      } else {

        var lookup = renderedNodes.findIndex(x => x.data._id_$oid === eventData._id_$oid)
        console.log(renderedNodes)
        console.log(eventData._id_$oid)
        if (lookup != -1) {
          console.log("array not empty and previous transaction found")
          var rowNode = gridApiRef.current.getDisplayedRowAtIndex(lookup);
          rowNode.setData(eventData)
          // flash whole row, so leave column selection out
          gridApiRef.current.flashCells({ rowNodes: [rowNode] });  
        } else {
          console.log("array not empty and previous transaction NOT found")
          gridApiRef.current.updateRowData({add: [eventData],addIndex:0});
          // get row 0
          var rowNode1 = gridApiRef.current.getDisplayedRowAtIndex(0);
          // flash whole row, so leave column selection out
          gridApiRef.current.flashCells({ rowNodes: [rowNode1] }); 
        }

      }
      //gridApiRef.current.applyTransaction({add: [eventData],addIndex:0})
      // get row 0
      //var rowNode1 = gridApiRef.current.getDisplayedRowAtIndex(0);
      // flash whole row, so leave column selection out
      //gridApiRef.current.flashCells({ rowNodes: [rowNode1] });
    }
}, []);



  //rowData=${rowData} 
  //columnDefs=${columnDefs}>
  //</${AgGridReact}>
  return html`
  <h1>TABLE</h1>
  <div>
  
  <div class="ag-theme-alpine-dark">
    <${AgGridReact.AgGridReact} 
      onGridReady=${onGridReady} 
      ref=${gridApiRef} 
      gridOptions=${gridOptionsRef} 
      pagination=${true} 
      defaultColDef=${defaultColDef} 
      enableSorting=${true} 
      enableFilter=${true}
    </${AgGridReact.AgGridReact}>
  </div>
  </div>
  `;
}

function Thunder() {
  //Fire Sweet alert
  Swal.fire({
    //test: sendalert(),
    html:   '<div><table>'+

      '<tr><th>field1</th><th>value1</th></tr>'+
      '<tr><td>field1</td><th>value1</td></tr>'+
      '<tr><td>field1</td><th>value1</td></tr>'+
      '<tr><td>field1</td><th>value1</td></tr>'+

            '<table>'+
            '</div>',      
    position: 'center',
    icon: 'success',
    title: 'Your work has been saved',
    showConfirmButton: false,
    timer: 10000,
    backdrop: `
        rgba(0,0,123,0.4)
        url("/static/images/nyan-cat.gif")
        left top
        no-repeat
    `,
    didOpen: () => {

        
    },
    willClose: () => {
        //
    }
    }).then((result) => {
    /* Read more about handling dismissals below */

    if (result.dismiss === Swal.DismissReason.timer) {
        //console.log('I was closed by the timer')
    }
    })


  const [count, setCount] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      window.open("", "_self");
      window.close();
      console.log("Hello, World!")
    }
    , 3000);
    return () => clearTimeout(timer);
  }, []);
  
  return html`
  <div>
  Hello, World
</div>
  `;
}

function App() {

  let menuOptions = [{label:"Fast",path:"nav-home",component:Thunder},
                    {label:"Create a team",path:"nav-create-team",component:ClickCounter},
                    {label:"Join a random team",path:"nav-join-random-team",component:ClickCounter},
                    {label:"Leaderboard",path:"nav-leaderboard",component:ClickCounter}]

  const [active,setActive] = useState(menuOptions[0])
  const test = {component:ClickCounter}
  const options = [{"id":1,"value":"Roman","label":"Roman"},{"id":2,"value":"joe","label":"joe"},{"id":3,"value":"bengi","label":"bengi"},];
  return (html`
  <div class="container-fluid">
  
    <${HashRouter}>
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <${NavLink}
        className="navbar-item"
        activeClassName="is-active"
        to="/models"
        >
          Models
        </${NavLink}>

        <${NavLink}
        className="navbar-item"
        activeClassName="is-active"
        to="/new/model/"
        >
          Create Model
        </${NavLink}>
        <${NavLink}
        className="navbar-item"
        activeClassName="is-active"
        to="/new/timer/"
        >
          Create Model
        </${NavLink}>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">  
      <${Switch}>
      <${Route} path="/models">
        <${getModels}/>
      </${Route}>
      <${Route} path="/new/model/">
        <${createModel}/>
      </${Route}>
      <${Route} path="/new/timer/">
        <${ClickCounter}/>
      </${Route}>
      <${Route} path="/transactions/:objectModelId">
        <${showTansactions}/>
      </${Route}>
      </${Switch}>
    </div>
    </${HashRouter}>
    </div>
  `
  )}

    //Rendering
    render(html`<${App}/>`, document.getElementById("App"));
    
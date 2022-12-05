import React,{ useState } from 'react';
import logo from './logo.svg';
import './App.css';
import CollapsibleExample from './components/Navbar/main';
import Example from './components/Home/button';
import ShowModels from './components/Models/ShowModels';
import Models from './components/Models/Models';
import ShowTransactions from './components/Transactions/ShowTransactions';
import ClickCounter from './components/counter';
//import "react-toggle/style.css" // for ES6 modules
import { BrowserRouter as Router, Routes, HashRouter, Link, Route, NavLink } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import CreateModel from './components/Models/CreateModel';
import Form from './components/Forms/Form';
import ModelLinks from './components/Models/ModelLinks';

function App() {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  };
  return (
    <div className={`App ${theme}`}>
       <Router>
       <CollapsibleExample></CollapsibleExample>
       <Container fluid>
          <Routes>
          <Route path="/models" element={<Models/>}/>
          <Route path="/models/create" element={<CreateModel/>}/>
          <Route path="/links/:objectModelId" element={<ModelLinks/>}/>
          <Route path="/forms/:objectModelId" element={<Form/>}/>
          <Route path="/transactions/:objectModelId" element={<ShowTransactions/>}/>
        </Routes>
      </Container> 
    </Router>

    </div>
  );
}

export default App;

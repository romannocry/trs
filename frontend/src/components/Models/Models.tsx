import React, { useState, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { BrowserRouter, HashRouter, Link, Route, NavLink } from "react-router-dom";
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import BasicCard from './ModelCard';
import ShowModels from './ShowModels';
import ModelHeader from './ModelHeader';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import Divider from '@mui/material/Divider';

function Models() {

  return (
    <>
    <ModelHeader></ModelHeader>
    <Divider/>

    <ShowModels></ShowModels>
    </>
  );
}

export default Models;

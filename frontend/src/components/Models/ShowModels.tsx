import React, { useState, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { BrowserRouter, HashRouter, Link, Route, NavLink } from "react-router-dom";
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import BasicCard from './ModelCard';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton, { IconButtonProps } from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid'; // Grid version 1
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import ModelCard from './ModelCard';

const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"


function ShowModels() {
  // Declare a new state variable, which we'll call "count"
  const [models, setModels] = useState([]);
  const componentIsMounted = useRef(true);
  console.log("loading Models List")
  useEffect(() => {
    fetch('http://'+prod_ip+':8000/api/models', {
      method: 'GET',
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
  return (
    <Stack padding={1} direction="row" spacing={2}>
    {models.map((model,index) => {
      return (
          <ModelCard model={model} key={index}/>
      )     
      })}
    </Stack>
  );
}

export default ShowModels;

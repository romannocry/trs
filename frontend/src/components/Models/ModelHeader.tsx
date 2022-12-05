import React, { useState, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { BrowserRouter, HashRouter, Link, Route, NavLink } from "react-router-dom";
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button, { ButtonProps } from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid'; // Grid version 1
import Typography from '@mui/material/Typography';
import BasicCard from './ModelCard';
import ShowModels from './ShowModels';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import AddSharpIcon from '@mui/icons-material/AddSharp';

const ColorButton = styled(Button)<ButtonProps>(({ theme }) => ({
    color: theme.palette.getContrastText('#262627'),
    backgroundColor: '#262627',
    '&:hover': {
      backgroundColor: '#262627',
    },
  }));

function ModelHeader() {

  return (
    <Grid container padding={0.5}>
        <Link to={`/models/create`} style={{ textDecoration: 'none' }}>
            <ColorButton variant="outlined"  startIcon={<AddSharpIcon /> }>
            Create Model
            </ColorButton>
        </Link>
    </Grid>

  );
}

export default ModelHeader;

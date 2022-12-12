import React, { useState, useEffect, useRef } from 'react';
import { styled } from '@mui/material/styles';
import Grid from '@mui/material/Unstable_Grid2';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';



const prod_ip = "192.168.1.7"
const dev_ip = "172.0.0.1"


const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));
  
function Layout()  {

    
    useEffect(() => {
        console.log("layout loading")
    }, []);


  return (
    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 1, md: 1 }} spacing={1}>
        <Grid xs={6} md={3}>
            <Item>1</Item>
        </Grid>
        <Grid xs={6} md={3}>
            <Item>2</Item>
        </Grid>
        <Grid xs={6} md={3}>
            <Item>3</Item>
        </Grid>
        <Grid xs={6} md={3}>
            <Item>4</Item>
        </Grid>
    </Grid>

  );
}

export default Layout;

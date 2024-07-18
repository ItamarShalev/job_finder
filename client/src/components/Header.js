import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import PersonIcon from '@mui/icons-material/Person';

const Header = () => {
  return (
    <AppBar position="static" sx={{ width: '100%' }}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          JobFinder
        </Typography>
        <Box display="flex" alignItems="center">
          <IconButton color="inherit" component={Link} to="/login">
            <PersonIcon />
          </IconButton>
          <Typography variant="button" sx={{ marginLeft: 1 }}>
            Managers
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

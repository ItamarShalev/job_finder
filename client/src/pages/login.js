import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Box, TextField, Button, Typography, Alert } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import SignUpDialog from '../components/SignUpDialog';
import axios from 'axios';

const LoginPage = () => {
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [openSignUp, setOpenSignUp] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('user_name', userName);

      const response = await axios.post('http://localhost:8000/api/get_positions_by_user_name/', formData);
      if (response.status === 200) {
        setError('');
        navigate('/managers');
      } else {
        setError('Failed to login');
      }
    } catch (error) {
      setError('Failed to login');
      console.error('Login error:', error);
    }
  };

  const handleSignUpOpen = () => {
    setOpenSignUp(true);
  };

  const handleSignUpClose = () => {
    setOpenSignUp(false);
  };

  useEffect(() => {
    if (userName && password) {
      setError('');
    }
  }, [userName, password]);

  const isLoginEnabled = userName !== '' && password !== '';

  return (
    <Container maxWidth="xs">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
      >
        <LockIcon fontSize="large" color="primary" />
        <Typography variant="h5" component="h1" gutterBottom>
          Login
        </Typography>
        {error && (
          <Alert severity="error" style={{ width: '100%', marginBottom: 16 }}>
            {error}
          </Alert>
        )}
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="UserName"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            style={{ marginTop: 16 }}
            disabled={!isLoginEnabled}
          >
            Login
          </Button>
        </form>
        <Button
          fullWidth
          variant="text"
          sx={{ color: 'black', marginTop: 3, textTransform: 'none' }}
          onClick={handleSignUpOpen}
        >
          Sign Up
        </Button>
      </Box>
      <SignUpDialog open={openSignUp} onClose={handleSignUpClose} />
    </Container>
  );
};

export default LoginPage;

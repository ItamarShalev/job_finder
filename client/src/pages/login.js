import React, { useState } from 'react';
import { Container, Box, TextField, Button, Typography, Alert } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import SignUpDialog from '../components/SignUpDialog';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [openSignUp, setOpenSignUp] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // בדיקה פשוטה לדוגמה
    if (email === 'test@example.com' && password === 'password') {
      setError('');
      // נוודא שהמשתמש ניגש לדף הנכון לאחר הלוגין
      console.log('Logged in successfully');
    } else {
      setError('Invalid email or password');
    }
  };

  const handleSignUpOpen = () => {
    setOpenSignUp(true);
  };

  const handleSignUpClose = () => {
    setOpenSignUp(false);
  };

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
            label="Email Address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
          >
            Login
          </Button>
        </form>
        <Button
          fullWidth
          variant="text"
          sx={{ color: 'black', marginTop: 16, textTransform: 'none' }}
          style={{ marginTop: 16, textTransform: 'none' }}
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

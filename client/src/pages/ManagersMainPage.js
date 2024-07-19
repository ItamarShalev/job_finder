import React, { useState, useEffect } from 'react';
import { Container, Box, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material';
import Header from '../components/Header';
import ManagerDashboard from '../components/ManagerDashboard';
import axios from 'axios';
import AddIcon from '@mui/icons-material/Add';

const ManagersMainPage = () => {
  const [managerInfo, setManagerInfo] = useState(null);
  const [companyJobs, setCompanyJobs] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [url, setUrl] = useState('');

  useEffect(() => {
    const fetchPositions = async () => {
      try {
        const userName = 'JohnDoe'; // כאן יש להכניס את שם המשתמש הרלוונטי
        const response = await axios.post('http://localhost:8000/api/get_positions_by_user_name/', new URLSearchParams({ user_name: userName }));
        const data = response.data.result;
        setManagerInfo({
          name: data.user.name,
          company: data.user.company,
          role: 'HR Manager'
        });
        setCompanyJobs(data.positions);
      } catch (error) {
        console.error('Error fetching positions:', error);
      }
    };

    fetchPositions();
  }, []);

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setUrl('');
  };

  const handleSubmit = async () => {
    try {
      const userName = 'JohnDoe'; // כאן יש להכניס את שם המשתמש הרלוונטי
      await axios.post('http://localhost:8000/api/add_linkdin_company/', new URLSearchParams({
        company_linkdin_url: url,
        user_name: userName
      }));
      handleCloseDialog();
      // Refresh job positions after adding a new one
      const response = await axios.post('http://localhost:8000/api/get_positions_by_user_name/', new URLSearchParams({ user_name: userName }));
      setCompanyJobs(response.data.result.positions);
    } catch (error) {
      console.error('Error adding position:', error);
    }
  };

  if (!managerInfo) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Header />
      <Container maxWidth="lg">
        <Box mt={4} display="flex" justifyContent="space-between">
          <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpenDialog}>
            Add Job URL
          </Button>
        </Box>
        <Box mt={4}>
          <ManagerDashboard 
            managerInfo={managerInfo} 
            jobs={companyJobs}
          />
        </Box>
      </Container>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Add Job URL</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please enter the LinkedIn URL of the job you want to add.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="Job URL"
            type="url"
            fullWidth
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ManagersMainPage;

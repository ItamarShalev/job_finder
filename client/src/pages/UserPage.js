import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Box, Typography, Paper, Divider, Grid, Link } from '@mui/material';
import axios from 'axios';
import UserProcess from '../components/UserProcess';
import Header from '../components/Header';

const UserPage = () => {
  const { id } = useParams();
  const [activeStep, setActiveStep] = useState(0);
  const [userInfo, setUserInfo] = useState(null);
  const [stages, setStages] = useState([]);

  useEffect(() => {
    // Fetch candidate details and stages from the server
    const fetchCandidateData = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/get_stages_by_candidate/', new URLSearchParams({
          candidate_phone_number: id // assuming id is the candidate's phone number
        }));
        const candidateData = response.data;

        if (candidateData) {
          setUserInfo({
            name: candidateData.name,
            email: candidateData.email,
            phone: candidateData.phone,
            linkedin: candidateData.linkedin,
            aiInfo: {
              score: candidateData.aiScore || candidateData.stages.find(stage => stage.reviewer.type === 'AI')?.score,
              summary: candidateData.stages.find(stage => stage.reviewer.type === 'AI')?.summery
            },
            hrInfo: {
              name: candidateData.hrResponsible || 'HR Manager',
              comments: candidateData.stages.find(stage => stage.reviewer.type === 'HR')?.summery || 'The candidate has shown strong potential during the interviews and has the right qualifications for the role.'
            },
            teamLeadInfo: {
              name: candidateData.teamLeadResponsible || 'Team Lead',
              comments: candidateData.stages.find(stage => stage.reviewer.type === 'Team Lead')?.summery || 'The candidate is a team player and has demonstrated excellent technical skills.'
            }
          });

          setStages(candidateData.stages);
        }
      } catch (error) {
        console.error('Error fetching candidate data:', error);
      }
    };

    fetchCandidateData();
  }, [id]);

  const handleStepChange = (event, newValue) => {
    setActiveStep(newValue);
  };

  if (!userInfo) {
    return <Typography variant="h6">User not found</Typography>;
  }

  return (
    <>
      <Header />
      <Container maxWidth="md">
        <Box mt={4} component={Paper} p={3} textAlign="center">
          <Typography variant="h4" gutterBottom>Candidate Information</Typography>
          <Divider sx={{ mb: 2 }} />
          <Typography variant="h6" gutterBottom>Personal Information</Typography>
          <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} sm={6}>
              <Typography variant="body1"><strong>Name:</strong> {userInfo.name}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1"><strong>Email:</strong> {userInfo.email}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1"><strong>Phone:</strong> {userInfo.phone}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1">
                <strong>LinkedIn:</strong> 
                <Link href={userInfo.linkedin} target="_blank" rel="noopener noreferrer" sx={{ ml: 1 }}>
                  {userInfo.linkedin}
                </Link>
              </Typography>
            </Grid>
          </Grid>
          <Divider sx={{ my: 2 }} />
          <UserProcess 
            userInfo={userInfo} 
            activeStep={activeStep} 
            onStepChange={handleStepChange} 
            stages={stages} // pass stages to UserProcess component
          />
        </Box>
      </Container>
    </>
  );
};

export default UserPage;

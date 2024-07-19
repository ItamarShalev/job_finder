import React from 'react';
import { Box, Tabs, Tab, Container, Stepper, Step, StepLabel, Paper } from '@mui/material';
import UserTechnicalInfo from './UserTechnicalInfo';
import AIRecommendations from './AIRecommendations';
import HRInsights from './HRInsights';
import TeamLeadComments from './TeamLeadComments';

const UserProcess = ({ userInfo, activeStep, onStepChange, stages }) => {
  const processSteps = [
    'AI Recommendations',
    'HR Insights',
    'Team Lead Comments'
  ];

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 2, mb: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {processSteps.map((label, index) => (
            <Step key={index}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeStep} onChange={onStepChange} variant="scrollable" scrollButtons="auto">
          {processSteps.map((label, index) => (
            <Tab label={label} key={index} />
          ))}
        </Tabs>
      </Box>
      <Box sx={{ p: 3 }}>
        {activeStep === 0 && <AIRecommendations aiInfo={userInfo.aiInfo} />}
        {activeStep === 1 && <HRInsights hrInfo={userInfo.hrInfo} />}
        {activeStep === 2 && <TeamLeadComments teamLeadInfo={userInfo.teamLeadInfo} />}
      </Box>
      
    </Container>
  );
};

export default UserProcess;

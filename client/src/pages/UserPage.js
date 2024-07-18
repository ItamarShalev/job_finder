import React, { useState } from 'react';
import UserProcess from '../components/UserProcess';

const UserPage = () => {
  const [activeStep, setActiveStep] = useState(0);

  const userInfo = {
    name: 'Jane Doe',
    email: 'jane.doe@example.com',
    phone: '123-456-7890',
    linkedin: 'https://www.linkedin.com/in/janedoe/',
    aiInfo: {
      score: 85,
      summary: 'The AI has determined that Jane is a strong fit for the role based on her skills and experience.'
    },
    hrInfo: {
      name: 'HR Manager',
      comments: 'Jane has shown strong potential during the interviews and has the right qualifications for the role.'
    },
    teamLeadInfo: {
      name: 'Team Lead',
      comments: 'Jane is a team player and has demonstrated excellent technical skills.'
    }
  };

  const handleStepChange = (event, newValue) => {
    setActiveStep(newValue);
  };

  return (
    <UserProcess 
      userInfo={userInfo} 
      activeStep={activeStep} 
      onStepChange={handleStepChange} 
    />
  );
};

export default UserPage;

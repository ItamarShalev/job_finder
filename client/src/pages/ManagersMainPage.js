import React from 'react';
import { Container, Box } from '@mui/material';
import Header from '../components/Header';
import ManagerDashboard from '../components/ManagerDashboard';
import jobsData from '../db/jobs.json'; // נתיב הקובץ לפי המיקום שלו בפרויקט

const ManagersMainPage = () => {
  const managerInfo = {
    name: 'John Doe',
    company: 'Tech Solutions',
    role: 'HR Manager'
  };

  // סינון המשרות לפי החברה של המנהל
  const companyJobs = jobsData.filter(job => job.company === managerInfo.company);

  return (
    <>
      <Header />
      <Container maxWidth="lg">
        <Box mt={4}>
          <ManagerDashboard 
            managerInfo={managerInfo} 
            jobs={companyJobs}
          />
        </Box>
      </Container>
    </>
  );
};

export default ManagersMainPage;

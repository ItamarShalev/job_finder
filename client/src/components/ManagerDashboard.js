import React, { useState } from 'react';
import { Box, Typography } from '@mui/material';
import ManagerJobCard from './ManagerJobCard';

const ManagerDashboard = ({ managerInfo, jobs }) => {
  const [selectedJob, setSelectedJob] = useState(null);

  const handleJobSelect = (job) => {
    setSelectedJob(selectedJob === job ? null : job);
  };

  return (
    <Box p={3} textAlign="center">
      <Typography variant="h4" gutterBottom>
        Welcome, {managerInfo.name}
      </Typography>
      <Typography variant="h6" gutterBottom>
        Company: {managerInfo.company}
      </Typography>
      <Typography variant="h6" gutterBottom>
        Role: {managerInfo.role}
      </Typography>
      <Box mt={4}>
        <Typography variant="h5">Jobs</Typography>
        {jobs.map((job, index) => (
          <ManagerJobCard 
            key={index} 
            job={job} 
            onSelect={() => handleJobSelect(job)} 
            selected={selectedJob === job} 
          />
        ))}
      </Box>
    </Box>
  );
};

export default ManagerDashboard;

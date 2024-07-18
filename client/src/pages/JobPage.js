import React from 'react';
import { useParams } from 'react-router-dom';
import { Container, Box, Typography } from '@mui/material';
import jobsData from '../db/jobs.json'; // נתיב הקובץ לפי המיקום שלו בפרויקט

const JobPage = () => {
  const { id } = useParams();
  const job = jobsData.find(job => job.id === id); // וידוא שה- id הוא מחרוזת ולא מספר

  if (!job) {
    return <Typography variant="h6">Job not found</Typography>;
  }

  return (
    <Container maxWidth="lg">
      <Box mt={4}>
        <Typography variant="h4">{job.title}</Typography>
        <Typography variant="subtitle1">{job.company}</Typography>
        <Typography variant="body2">{job.location}</Typography>
        <Typography variant="body2">{job.description}</Typography>
        {job.stats && (
          <Box mt={2}>
            <Typography variant="h6">Applicant Information</Typography>
            <Typography variant="body2">Total Applicants: {job.stats.totalApplicants}</Typography>
            <Typography variant="body2">AI Passed: {job.stats.aiPassed} / {job.stats.totalApplicants}</Typography>
            <Typography variant="body2">HR Passed: {job.stats.hrPassed} / {job.stats.totalApplicants}</Typography>
            <Typography variant="body2">Team Lead Passed: {job.stats.teamLeadPassed} / {job.stats.totalApplicants}</Typography>
            <Typography variant="body2">Completed: {job.stats.completed} / {job.stats.totalApplicants}</Typography>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default JobPage;

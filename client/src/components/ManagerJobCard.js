import React, { useState } from 'react';
import { Card, CardContent, Typography, Collapse, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const ManagerJobCard = ({ job, onSelect, selected }) => {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate();

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleNavigate = (event) => {
    event.stopPropagation(); // כדי למנוע את הרחבת הכרטיס בעת לחיצה על הכפתור
    navigate(`/job/${job.id}`);
  };

  const { stats } = job;

  return (
    <Card
      variant="outlined"
      onClick={() => {
        onSelect();
        handleExpandClick();
      }}
      sx={{ 
        borderColor: selected ? 'primary.main' : 'grey.400',
        cursor: 'pointer',
        mb: 2
      }}
    >
      <CardContent>
        <Typography variant="h5">{job.title}</Typography>
        <Typography variant="subtitle1">{job.company}</Typography>
        <Typography variant="body2">{job.location}</Typography>
        <Typography variant="body2">{job.description}</Typography>
        <Button variant="contained" color="primary" onClick={handleNavigate}>
          POSITION PAGE
        </Button>
      </CardContent>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {stats ? (
            <Box mt={2}>
              <Typography variant="h6">Applicant Information</Typography>
              <Typography variant="body2">Total Applicants: {stats.totalApplicants}</Typography>
              <Typography variant="body2">AI Passed: {stats.aiPassed} / {stats.totalApplicants}</Typography>
              <Typography variant="body2">HR Passed: {stats.hrPassed} / {stats.totalApplicants}</Typography>
              <Typography variant="body2">Team Lead Passed: {stats.teamLeadPassed} / {stats.totalApplicants}</Typography>
              <Typography variant="body2">Completed: {stats.completed} / {stats.totalApplicants}</Typography>
            </Box>
          ) : (
            <Typography variant="body2">No applicant information available.</Typography>
          )}
        </CardContent>
      </Collapse>
    </Card>
  );
};

export default ManagerJobCard;

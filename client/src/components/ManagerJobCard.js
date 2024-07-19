import React, { useState } from 'react';
import { Card, CardContent, Typography, Collapse, Box, Button, IconButton } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import BusinessIcon from '@mui/icons-material/Business';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PageviewIcon from '@mui/icons-material/Pageview';

const ManagerJobCard = ({ job, onSelect, selected }) => {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate();

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleNavigate = (event) => {
    event.stopPropagation(); 
    navigate(`/job`);
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
        mb: 2,
        transition: 'transform 0.3s',
        '&:hover': {
          transform: 'scale(1.02)',
          boxShadow: '0 8px 16px rgba(0,0,0,0.2)'
        }
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1 }}>
            {job.title}
          </Typography>
          <IconButton onClick={handleExpandClick} sx={{ ml: 1 }}>
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>
        <Box display="flex" alignItems="center" mb={1}>
          <BusinessIcon sx={{ mr: 1, color: 'grey.600' }} />
          <Typography variant="subtitle1" component="div">
            {job.company}
          </Typography>
        </Box>
        <Box display="flex" alignItems="center" mb={1}>
          <LocationOnIcon sx={{ mr: 1, color: 'grey.600' }} />
          <Typography variant="body2" component="div">
            {job.location}
          </Typography>
        </Box>
        <Typography variant="body1" paragraph align="center" sx={{ fontSize: '1.2rem' }}>
          {job.description}
        </Typography>
        <Box display="flex" justifyContent="center" mt={2}>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={handleNavigate} 
            startIcon={<PageviewIcon />} 
            sx={{
              backgroundColor: '#3f51b5',
              '&:hover': {
                backgroundColor: '#303f9f'
              }
            }}
          >
            View Position
          </Button>
        </Box>
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

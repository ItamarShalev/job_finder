import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const JobCard = ({ job, onSelect, selected }) => {
  return (
    <Card
      variant="outlined"
      onClick={onSelect}
      sx={{ 
        borderColor: selected ? 'primary.main' : 'grey.400',
        backgroundColor: selected ? 'primary.light' : 'inherit',
        cursor: 'pointer'
      }}
    >
      <CardContent>
        <Typography variant="h5">{job.title}</Typography>
        <Typography variant="subtitle1">{job.company}</Typography>
        <Typography variant="body2">{job.location}</Typography>
        <Typography variant="body2">{job.description}</Typography>
      </CardContent>
    </Card>
  );
};

export default JobCard;

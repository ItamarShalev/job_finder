import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const JobCard = ({ job, onSelect, selected }) => {
  console.log('Job data:', job); 

  return (
    <Card
      variant="outlined"
      onClick={onSelect}
      sx={{
        borderColor: selected ? 'primary.main' : 'grey.400',
        cursor: 'pointer',
        mb: 2
      }}
    >
      <CardContent>
        <Typography variant="h5">{job.name}</Typography>
        <Typography variant="subtitle1">{job.company}</Typography>
        <Typography variant="body2">{job.location}</Typography>
        <Typography variant="body2">{job.description}</Typography>
        <Box mt={2}>
          <Typography variant="body2">Open by: {job.open_by}</Typography>
          <Typography variant="body2">
            <a href={job.linkdin_url} target="_blank" rel="noopener noreferrer">LinkedIn</a>
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default JobCard;

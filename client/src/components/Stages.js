import React from 'react';
import { Box, Typography } from '@mui/material';

const Stages = ({ stages }) => {
  return (
    <Box mt={4}>
      <Typography variant="h6">Stages Information</Typography>
      {stages.map((stage, index) => (
        <Box key={index} mt={2}>
          <Typography variant="body2">Stage: {stage.type}</Typography>
          <Typography variant="body2">Summary: {stage.summery}</Typography>
          <Typography variant="body2">Score: {stage.score}</Typography>
          <Typography variant="body2">Reviewed by: {stage.reviewer.name} ({stage.reviewer.type})</Typography>
        </Box>
      ))}
    </Box>
  );
};

export default Stages;

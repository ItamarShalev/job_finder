import React from 'react';
import { Box, Typography } from '@mui/material';

const AIRecommendations = ({ aiInfo }) => {
  return (
    <Box textAlign="center">
      <Typography variant="h5">AI Recommendations</Typography>
      <Typography variant="body1">AI Score: {aiInfo.score}</Typography>
      <Typography variant="body1">Summary: {aiInfo.summary}</Typography>
    </Box>
  );
};

export default AIRecommendations;

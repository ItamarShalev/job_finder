import React from 'react';
import { Box, Typography } from '@mui/material';

const HRInsights = ({ hrInfo }) => {
  return (
    <Box>
      <Typography variant="h5">HR Insights</Typography>
      <Typography variant="body1">Name: {hrInfo.name}</Typography>
      <Typography variant="body1">Comments: {hrInfo.comments}</Typography>
    </Box>
  );
};

export default HRInsights;

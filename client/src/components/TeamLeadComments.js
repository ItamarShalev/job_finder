import React from 'react';
import { Box, Typography } from '@mui/material';

const TeamLeadComments = ({ teamLeadInfo }) => {
  return (
    <Box>
      <Typography variant="h5">Team Lead Comments</Typography>
      <Typography variant="body1">Name: {teamLeadInfo.name}</Typography>
      <Typography variant="body1">Comments: {teamLeadInfo.comments}</Typography>
    </Box>
  );
};

export default TeamLeadComments;

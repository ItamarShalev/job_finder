import React from 'react';
import { Box, Typography, Link } from '@mui/material';

const UserTechnicalInfo = ({ userInfo }) => {
  return (
    <Box mt={4} textAlign="center">
      <Typography variant="h5">User Information</Typography>
      <Typography variant="body1">Name: {userInfo.name}</Typography>
      <Typography variant="body1">Email: {userInfo.email}</Typography>
      <Typography variant="body1">Phone: {userInfo.phone}</Typography>
      <Link href={userInfo.linkedin} target="_blank" rel="noopener">
        LinkedIn Profile
      </Link>
    </Box>
  );
};

export default UserTechnicalInfo;

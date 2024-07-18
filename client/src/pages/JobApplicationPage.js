import React, { useState } from 'react';
import { Container, Typography, Button, Box, Alert, CircularProgress } from '@mui/material';
import axios from 'axios';

const JobApplicationPage = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
    setUploadStatus(null); // Reset upload status on new file selection
    console.log('File selected:', file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!uploadedFile) {
      setUploadStatus('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setLoading(false);
      setUploadStatus('File uploaded successfully');
      console.log('File upload response:', response);
    } catch (error) {
      setLoading(false);
      setUploadStatus('File upload failed');
      console.error('File upload error:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Job Position
      </Typography>
      <Typography variant="body1" paragraph>
        Information about the job position goes here. Detailed description of the role, responsibilities, and requirements.
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
          <Button
            variant="contained"
            component="label"
          >
            Add File
            <input
              type="file"
              hidden
              accept=".pdf, .doc, .docx"
              onChange={handleFileUpload}
            />
          </Button>
          {uploadedFile && (
            <Typography variant="body1">
              Selected file: {uploadedFile.name}
            </Typography>
          )}
          {loading && <CircularProgress />}
          {uploadStatus && (
            <Alert severity={uploadStatus === 'File uploaded successfully' ? 'success' : 'error'}>
              {uploadStatus}
            </Alert>
          )}
          <Button
            type="submit"
            variant="contained"
            color="primary"
          >
            Submit
          </Button>
        </Box>
      </form>
    </Container>
  );
};

export default JobApplicationPage;

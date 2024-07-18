import React, { useState, useEffect, useCallback } from 'react';
import { Container, Box, Button, Typography, Alert, CircularProgress, Grid, IconButton } from '@mui/material';
import Header from '../components/Header';
import FilterButtons from '../components/FilterButtons';
import JobCard from '../components/JobCard';
import axios from 'axios';
import jobsData from '../db/jobs.json'; // נתיב הקובץ לפי המיקום שלו בפרויקט
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import AttachFileIcon from '@mui/icons-material/AttachFile';

const JOBS_PER_PAGE = 8;

const MainPage = () => {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [selectedFilters, setSelectedFilters] = useState({
    Location: '',
    Field: '',
    Company: '',
    Role: '',
    Type: ''
  });
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedJobs, setSelectedJobs] = useState([]);

  useEffect(() => {
    if (jobsData && jobsData.length > 0) {
      setJobs(jobsData);
      setFilteredJobs(jobsData); // הצגת כל המשרות כברירת מחדל בעת טעינת הקומפוננטה
    }
  }, []);

  const filterJobs = useCallback(() => {
    if (Object.values(selectedFilters).every((value) => value === '')) {
      setFilteredJobs(jobs);
    } else {
      const newFilteredJobs = jobs.filter((job) =>
        Object.keys(selectedFilters).every((key) =>
          selectedFilters[key] === '' || job[key.toLowerCase()] === selectedFilters[key]
        )
      );
      setFilteredJobs(newFilteredJobs);
    }
    setCurrentPage(0);
  }, [selectedFilters, jobs]);

  useEffect(() => {
    filterJobs();
  }, [selectedFilters, filterJobs]);

  const handleFilterChange = (category, value) => {
    setSelectedFilters((prevFilters) => ({
      ...prevFilters,
      [category]: value
    }));
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
    setUploadStatus(null);
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

  const handleNextPage = () => {
    if (currentPage < Math.ceil(filteredJobs.length / JOBS_PER_PAGE) - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleJobSelect = (job) => {
    setSelectedJobs((prevSelected) =>
      prevSelected.includes(job)
        ? prevSelected.filter((j) => j !== job)
        : [...prevSelected, job]
    );
  };

  const currentJobs = filteredJobs.slice(currentPage * JOBS_PER_PAGE, (currentPage + 1) * JOBS_PER_PAGE);

  const filters = {
    Location: [...new Set(jobs.map((job) => job.location))],
    Company: [...new Set(jobs.map((job) => job.company))],
    Role: [...new Set(jobs.map((job) => job.title))],
    // Assuming "Field" and "Type" are also part of job data.
    Field: [...new Set(jobs.map((job) => job.field))],
    Type: [...new Set(jobs.map((job) => job.type))]
  };

  return (
    <div>
      <Header />
      <Container>
        <Box mt={4}>
          <FilterButtons filters={filters} selectedFilters={selectedFilters} onFilterChange={handleFilterChange} />
        </Box>
        <Grid container spacing={2} mt={2}>
          {currentJobs.length > 0 ? (
            currentJobs.map((job, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <JobCard job={job} onSelect={() => handleJobSelect(job)} selected={selectedJobs.includes(job)} />
              </Grid>
            ))
          ) : (
            <Typography variant="h6" align="center">
              No jobs available
            </Typography>
          )}
        </Grid>
        <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
          <IconButton onClick={handlePreviousPage} disabled={currentPage === 0}>
            <ArrowBackIcon />
          </IconButton>
          <Typography>
            Page {currentPage + 1} of {Math.ceil(filteredJobs.length / JOBS_PER_PAGE)}
          </Typography>
          <IconButton onClick={handleNextPage} disabled={currentPage >= Math.ceil(filteredJobs.length / JOBS_PER_PAGE) - 1}>
            <ArrowForwardIcon />
          </IconButton>
        </Box>
        <form onSubmit={handleSubmit}>
          <Box display="flex" flexDirection="column" alignItems="center" gap={2} mt={4}>
            <Button
              variant="contained"
              component="label"
              startIcon={<AttachFileIcon />} // הוספת האייקון
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
    </div>
  );
};

export default MainPage;

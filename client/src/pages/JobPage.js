import React, { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Container, Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Link } from '@mui/material';
import axios from 'axios';
import Header from '../components/Header';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const JobPage = () => {
  const { linkdin_url } = useParams();
  const [job, setJob] = useState(null);
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/get_position_by_linkdin_url/', new URLSearchParams({
          linkdin_url: linkdin_url
        }));
        console.log('Job data:', response.data.result); // בדיקה של הנתונים המתקבלים
        setJob(response.data.result);
      } catch (error) {
        console.error('Error fetching job:', error);
      }
    };

    fetchJob();
  }, [linkdin_url]);

  useEffect(() => {
    if (job) {
      const fetchCandidates = async () => {
        try {
          const response = await axios.post('http://localhost:8000/api/get_candidates_by_position/', new URLSearchParams({
            linkdin_url: job.linkdin_url,
            user_name: job.name
          }));
          console.log('Candidates data:', response.data.result); // בדיקה של הנתונים המתקבלים
          setCandidates(response.data.result);
        } catch (error) {
          console.error('Error fetching candidates:', error);
        }
      };

      fetchCandidates();
    }
  }, [job]);

  if (!job) {
    return <Typography variant="h6">Job not found</Typography>;
  }

  return (
    <>
      <Header />
      <Container maxWidth="lg">
        <Box mt={4} display="flex" flexDirection="column" alignItems="center">
          <AccountCircleIcon style={{ fontSize: 60, color: '#3f51b5' }} />
          <Typography variant="h4" gutterBottom>{job.name}</Typography>
          <Typography variant="subtitle1" gutterBottom>{job.company}</Typography>
          <Typography variant="body2" gutterBottom>{job.location}</Typography>
          <Typography variant="body2" paragraph>{job.description}</Typography>
          {job.stats && (
            <Box mt={2}>
              <Typography variant="h6" gutterBottom>Applicant Information</Typography>
              <Typography variant="body2">Total Applicants: {job.stats.totalApplicants}</Typography>
              <Typography variant="body2">AI Passed: {job.stats.aiPassed} / {job.stats.totalApplicants}</Typography>
              <Typography variant="body2">HR Passed: {job.stats.hrPassed} / {job.stats.totalApplicants}</Typography>
              <Typography variant="body2">Team Lead Passed: {job.stats.teamLeadPassed} / {job.stats.totalApplicants}</Typography>
              <Typography variant="body2">Completed: {job.stats.completed} / {job.stats.totalApplicants}</Typography>
            </Box>
          )}
        </Box>
        <Box mt={4} width="100%">
          <Typography variant="h5" gutterBottom>Candidate Information</Typography>
          <TableContainer component={Paper} sx={{ width: '100%' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Stage</TableCell>
                  <TableCell>Responsible</TableCell>
                  <TableCell>Phone</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>LinkedIn</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {candidates.map((candidate) => (
                  <TableRow key={candidate.id} component={RouterLink} to={`/user/`} style={{ textDecoration: 'none', cursor: 'pointer' }}>
                    <TableCell>{candidate.id}</TableCell>
                    <TableCell>{candidate.name}</TableCell>
                    <TableCell>{candidate.stage}</TableCell>
                    <TableCell>{candidate.responsible}</TableCell>
                    <TableCell>{candidate.phone}</TableCell>
                    <TableCell>
                      <Link href={`mailto:${candidate.email}`} target="_blank" rel="noopener noreferrer">
                        {candidate.email}
                      </Link>
                    </TableCell>
                    <TableCell>
                      <Link href={candidate.linkedin} target="_blank" rel="noopener noreferrer">
                        Profile
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Container>
    </>
  );
};

export default JobPage;

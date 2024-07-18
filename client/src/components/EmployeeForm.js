import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { TextField, Button, Container, Typography } from '@mui/material';
import { createEmployee, getEmployeeById, updateEmployee } from '../api/employeeApi';

const EmployeeForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue, formState: { errors } } = useForm();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      getEmployeeById(id).then(employee => {
        setValue('name', employee.name);
        setValue('email', employee.email);
        setValue('position', employee.position);
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, [id, setValue]);

  const onSubmit = async (data) => {
    if (id) {
      await updateEmployee(id, data);
    } else {
      await createEmployee(data);
    }
    navigate('/');
  };

  if (loading) return <div>Loading...</div>;

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        {id ? 'Edit Employee' : 'Add Employee'}
      </Typography>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          fullWidth
          label="Name"
          variant="outlined"
          margin="normal"
          {...register('name', { required: true })}
          error={!!errors.name}
          helperText={errors.name ? 'Name is required' : ''}
        />
        <TextField
          fullWidth
          label="Email"
          variant="outlined"
          margin="normal"
          {...register('email', { required: true })}
          error={!!errors.email}
          helperText={errors.email ? 'Email is required' : ''}
        />
        <TextField
          fullWidth
          label="Position"
          variant="outlined"
          margin="normal"
          {...register('position', { required: true })}
          error={!!errors.position}
          helperText={errors.position ? 'Position is required' : ''}
        />
        <Button type="submit" variant="contained" color="primary" fullWidth margin="normal">
          Submit
        </Button>
      </form>
    </Container>
  );
};

export default EmployeeForm;

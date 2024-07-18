import React, { useState, useEffect } from 'react';
import { getEmployees } from '../api/employeeApi';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const employees = await getEmployees();
      setEmployees(employees);
    }
    fetchData();
  }, []);

  return (
    <div>
      <ul>
        {employees.map(employee => (
          <li key={employee.id}>{employee.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default EmployeeList;

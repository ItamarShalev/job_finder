import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './pages/MainPage';
import LoginPage from './pages/login';
import ManagersMainPage from './pages/ManagersMainPage';
import UserPage from './pages/UserPage';
import JobPage from './pages/JobPage';
const App = () => {
  return (
    <Router>
      
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/managers" element={<ManagersMainPage />} />
        <Route path="/user" element={<UserPage />} />
        <Route path="/job" element={<JobPage />} /> 
      </Routes>
    </Router>
  );
};

export default App;

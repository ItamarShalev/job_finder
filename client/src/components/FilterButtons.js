import React from 'react';
import { Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const FilterButtons = ({ filters, selectedFilters, onFilterChange }) => {
  const categories = Object.keys(filters);

  return (
    <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap">
      {categories.map((category) => (
        <FormControl key={category} variant="outlined" sx={{ minWidth: 120 }}>
          <InputLabel>{category}</InputLabel>
          <Select
            value={selectedFilters[category] || ''}
            onChange={(e) => onFilterChange(category, e.target.value)}
            label={category}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {filters[category].map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      ))}
    </Box>
  );
};

export default FilterButtons;

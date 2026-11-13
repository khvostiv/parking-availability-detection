const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const app = express();
const port = 3001; 

app.use(express.static(path.join(__dirname, 'frontend')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname,'frontend/index.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

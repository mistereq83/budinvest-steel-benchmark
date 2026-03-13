const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Named routes BEFORE static middleware
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'compare', 'index.html'));
});

app.get('/chooser', (req, res) => {
  res.sendFile(path.join(__dirname, 'chooser-variants', 'compare.html'));
});

// Static files (variant HTML, assets)
app.use(express.static(path.join(__dirname)));

app.listen(PORT, () => {
  console.log(`Budinvest Steel running on port ${PORT}`);
});

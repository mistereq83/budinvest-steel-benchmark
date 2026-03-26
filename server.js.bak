const express = require('express');
const path = require('path');
const compression = require('compression');
const app = express();
const PORT = process.env.PORT || 3000;

// Gzip compression
app.use(compression());

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    next();
});

// Static files with cache
app.use(express.static(path.join(__dirname, 'public'), {
    maxAge: '7d',
    etag: true
}));

// Clean URLs
app.get('/:page', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'public', `${req.params.page}.html`), err => { if (err) next(); });
});
app.get('/uslugi/:page', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'public', 'uslugi', `${req.params.page}.html`), err => { if (err) next(); });
});
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => console.log(`Budinvest Steel running on port ${PORT}`));

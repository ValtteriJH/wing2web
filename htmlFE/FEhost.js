// server.js

// Import required modules
const express = require('express');
const path = require('path');

// Create an Express application
const app = express();

// Define a route to serve the HTML file
app.get('/', (req, res) => {
    // Send the HTML file as the response
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/faq', (req, res) => {
    // Send the HTML file as the response
    res.sendFile(path.join(__dirname, 'faq.html'));
});

app.get('/changes', (req, res) => {
    // Send the HTML file as the response
    res.sendFile(path.join(__dirname, 'changes.html'));
});



// Define a route to serve the HTML file
app.get('/script.js', (req, res) => {
    // Send the HTML file as the response
    res.sendFile(path.join(__dirname, 'script.js'));
});

// app.get('/favicon.ico', (req, res) => {
//     // Send the HTML file as the response
//     res.sendFile(path.join(__dirname, '/favicon.ico'));
// });


app.get('/favicon.ico', (req, res) => {
    // Send the HTML file as the response
    res.sendFile(path.join(__dirname, '/favicon_io/android-chrome-192x192.png'));
});



// Start the server
const PORT = process.env.PORT || 8889; //8889; // 2222 is a DEBUG port!
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

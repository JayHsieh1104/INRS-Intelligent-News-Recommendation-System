const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./query.js')
const config = require('./config.json');
const PORT = process.env.PORT || 8080;

app.use(function (req, res, next) {
    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');
    
    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});

app.get('/', (request, response) => {
    response.json({ info: 'Express.js server is running!' })
})

app.get('/news/:category', db.getNewsByCategory)

app.listen(PORT, () => {
    console.log(`App running on port ${PORT}.`)
})
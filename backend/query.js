const config = require('./config.json');
const Pool = require('pg').Pool
const pool = new Pool({
    host: config.db_host,
    // host: "news-recommendation-system-db.cxtw9xtzpfjz.us-east-1.rds.amazonaws.com",
    port: config.db_port,
    database: config.database,
    user: config.db_username,
    // user: "awsuser",
    password: config.db_password
})

const getNewsByCategory = (request, response) => {
    const category = request.params.category

    pool.query('SELECT * FROM public.articles WHERE category = $1', [category], (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}

module.exports = {
    getNewsByCategory,
}
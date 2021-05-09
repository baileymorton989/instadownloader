const express = require('express')

const app = express()

const python = require('python-shell')

const port = 3096

app.get('/', (req,res) => {
    res.send("Hello!");
})



app.listen(port, () => {
    console.log(`Listening at: http://localhost:${port}`)
})

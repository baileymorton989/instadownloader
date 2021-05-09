const express = require('express')

const app = express()

let {PythonShell} = require('python-shell')

const port = 3096


/*
 * Example run Python script:
 *
 *  PythonShell.run('my_script.py', null, function (err) {
 *   if (err) throw err;
 *     console.log('finished');
 *     });
 *
 */

app.get('/', (req,res) => {
    res.send("Hello!");
})

app.listen(port, () => {
    console.log(`Listening at: http://localhost:${port}`)
})

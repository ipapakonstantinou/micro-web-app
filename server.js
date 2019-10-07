const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const app = express();

app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }));

mongoose
  .connect(
    'mongodb://mongo:27017/docker-nodejs-mongo',
    { useNewUrlParser: true }
  )
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));


const Item = require('./models/item');

app.get('/', (req, res) => {
  Item.find()
    .then(items => res.render('server', { items }))
    .catch(err => res.status(404).json({ msg: 'No items found' }));
});

app.post('/item/add', (req, res) => {
  const newItem = new Item({
    name: req.body.name
  });
  newItem.save().then(item => res.redirect('/'));
});

const port = 3000;

app.listen(port, () => console.log('Server running...'));

// var express = require('express');
// var app = express();
// var sqlite3 = require('sqlite3');
// var db = new sqlite3.Database('./db/items.db');
// var bodyParser = require('body-parser');
//
// app.use(express.static(__dirname + '/public'));
// app.use(bodyParser.urlencoded({extended: false}));
//
// app.get('/', function(request, response){
//   response.send('Hello, World');
// });
//
// app.get('/items', function(request, response){
//   console.log('GET request received at /items');
//   db.all('SELECT * FROM items', function(err, rows){
//     if(err){
//       console.log("Error: " + err);
//     }
//     else {
//       response.send(rows);
//     }
//   })
// });
//
// app.post('/items', function(request, response){
//   console.log('POST request recieved at /items');
//   db.run('INSERT INTO items VALUES(?, ?)',
//   [request.body.name, request.body.item], function(err){
//     if(err){
//       console.log("Error: " + err)
//     }
//     else {
//       response.status(200).redirect('/index.html');
//     }
//   });
// });
//
// app.listen(3000, function(){
//   console.log("Server is runnin on port 3000");
// });

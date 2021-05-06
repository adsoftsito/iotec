function route(app, regex, prefix) {
 app.get(regex, function (req, res) {
 var type = req.params[0];
 var path = req.params[1];
 var file = prefix + type + '/' + path
 res.sendfile(file);
 });
}

const bodyParser= require('body-parser')
var express = require('express');


var PORT = 80;

var app = express();
app.set('view engine', 'ejs')

app.get('/', function(req, res) {
 res.sendfile('index.html');
});


app.get('/login', function(req, res) {
 res.sendfile('login_2.html');
});


app.get('/device/:id/:name', function(req,res){
	res.render('device.ejs', {id: req.params.id, name: req.params.name});
});

route(app, /^\/(css|js|images|fonts|assets|img)\/(.*)/, './');

app.listen(PORT);
console.log('Running on port ' + PORT);


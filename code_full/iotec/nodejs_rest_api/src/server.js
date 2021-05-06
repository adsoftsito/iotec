// server.js

// base setup

function responseFormater(success, json, error = undefined){
  json.success = success;

  if(error != undefined)
    json.error = error;

  return json;
}

var mongoose = require('mongoose')
var database_name = 'mongodb://localhost:27017/devices'
mongoose.connect(database_name)
    
var conn = mongoose.connection;
var multer = require('multer');
var GridFsStorage = require('multer-gridfs-storage');
var Grid = require('gridfs-stream');
Grid.mongo = mongoose.mongo;
var gfs = Grid(conn.db);

// call the packages


var express = require('express')
var app = express();
var bodyParser = require('body-parser');

// config app to use bodyParser()

app.use(bodyParser.urlencoded({ extended: true}));
app.use(bodyParser.json());

var storage = GridFsStorage({
      gfs : gfs,
      filename: function (req, file, cb) {
          var datetimestamp = Date.now();
          cb(null, file.fieldname + '-' + datetimestamp + '.' + file.originalname.split('.')[file.originalname.split('.').length -1]);
      },
      /** With gridfs we can store aditional meta-data along with the file */
      metadata: function(req, file, cb) {
          cb(null, { originalname: file.originalname });
      },
      root: 'fs' //root name for collection to store files into
  });

var port = process.env.PORT || 8081; 

// routes for our api

var router = express.Router();

// middleware to use for all requests
router.use(function(req, res, next) {
  res.setHeader("Access-Control-Allow-Methods", "POST, PUT, OPTIONS, DELETE, GET");
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  res.header('Content-Type', 'application/json; charset=utf-8');
  next();
});

var User = require('./app/models/user');
var Device = require('./app/models/device');
var Sensor = require('./app/models/sensor');

// more routes for our API will happen here
router.route('/devices')
  
  .get(function(req, res){
    Device.find().populate('owner', '-_id -password').exec(
      function(error, value){
        res.json(value);
      });
  })

router.route('/image/:id')
  .get(function(req, res){
    var id = req.params.id;
    if (id == undefined || !id.match(/^[0-9a-fA-F]{24}$/)) {
      res.json(responseFormater(false, {}, "id is invalid " + id));
    }

    gfs.files.find({_id: mongoose.Types.ObjectId(id)}).toArray(function(err, files){
      if(!files || files.length === 0){
          return res.status(404).json({
              responseCode: 1,
              responseMessage: "error " + id
          });
      }


      /** create read stream */
      var readstream = gfs.createReadStream({
          _id: id,
          root: "fs"
      });
      /** set the proper content type */
      res.set('Content-Type', files[0].contentType)
      /** return response */
      return readstream.pipe(res);
    });
  })

router.route('/device/:id')
  .get(function(req, res){
    var id = req.params.id;
    if (id == undefined || !id.match(/^[0-9a-fA-F]{24}$/)) {
      res.json(responseFormater(false, {}, "id is invalid"));
    }
    else{
      Device.findOne({_id : mongoose.Types.ObjectId(id)}).exec(function(error, device){
        if(device == null)
          res.json(responseFormater(false, {}, 'invalid device id'));
        else{
            Sensor.distinct("name",{owner: device._id}).exec(function(error, result){
              if(!error)
                res.json(responseFormater(true, result));
              else
                res.json(responseFormater(false, {}, error));
            });
        }
      });
    }
  });

router.route('/device/:id/:name/imagery')
  .get(function(req, res){
    var id = req.params.id;
    var name = req.params.name;

    if (id == undefined || !id.match(/^[0-9a-fA-F]{24}$/)) {
      res.json(responseFormater(false, {}, "id is invalid or name is required"));
    }
    else{
      Device.findOne({_id : mongoose.Types.ObjectId(id)}).exec(function(error, device){
        if(device == null)
          res.json(responseFormater(false, {}, 'invalid device id'));
        else
            Sensor.count({owner: device._id, name: name}).exec(function(error, count){
              if(!error){
                if(count == 0){
                  res.json(responseFormater(false, {}, "Param not found on device"));
                }
                else{
                  Sensor.find({ name: name, owner: device._id }, function(err, sensors){
                    if(err)
                      res.json(responseFormater(false, {}, error));
                    else{
                      var images = [];
                      sensors.forEach(function(current){
                        images = images.concat(current.images);
                      })
                      res.json(responseFormater(true,images));
                    }
                  })               
                }
              }
            });
      });
    }
  });

router.route('/device/:id/:name/statistic')
  .get(function(req, res){
    var id = req.params.id;
    var name = req.params.name;

    if (id == undefined || !id.match(/^[0-9a-fA-F]{24}$/)) {
      res.json(responseFormater(false, {}, "id is invalid or name is required"));
    }
    else{
      Device.findOne({_id : mongoose.Types.ObjectId(id)}).exec(function(error, device){
        if(device == null)
          res.json(responseFormater(false, {}, 'invalid device id'));
        else{
            Sensor.count({owner: device._id, name: name}).exec(function(error, count){
              if(!error){
                if(count == 0){
                  res.json(responseFormater(false, {}, "Param not found on device"));
                }
                else{
                  Sensor.aggregate(
                    [
                      { 
                        $match: { name: name, owner: device._id } 
                      },
                      { $sort: { date: -1 } },
                      { 
                        $group: { 
                          min : {$min : "$numericValue"},
                          max : {$max : "$numericValue"},
                          avg : {$avg : "$numericValue"},
                          last : {$last : "$numericValue"},
                          _id : name 
                        } 
                      }
                    ], function(error, values){
                      if(error)
                        res.json(responseFormater(false, {}, error));
                      else
                        res.json(responseFormater(true, values[0]));
                    }
                  )

                }
              }
              else
                res.json(responseFormater(false, {}, error));
            });
        }
      });
    }
  });

router.route('/device/:id/:name/last')
  .get(function(req, res){
    var id = req.params.id;
    var name = req.params.name;

    var quantity = req.query.amount;
    if(quantity == undefined)
      quantity = 20;

    if (id == undefined || !id.match(/^[0-9a-fA-F]{24}$/) || isNaN(quantity) ) {
      res.json(responseFormater(false, {}, "id is invalid or name is required. quantity must be numeric if present"));
    }
    else{
      Device.findOne({_id : mongoose.Types.ObjectId(id)}).exec(function(error, device){
        if(device == null)
          res.json(responseFormater(false, {}, 'invalid device id'));
        else{
            Sensor.find({owner: device._id, name: name}).select('-_id').limit(quantity).exec(function(error, result){
              if(error)
                res.json(responseFormater(false, {}, error));
              else
                res.json(responseFormater(true, result));
            });
        }
      });
    }
  });


// register our routes
app.use('/api', router);

// start the server
app.listen(port);

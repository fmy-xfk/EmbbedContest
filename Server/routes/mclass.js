var express = require('express');
var musr = require('./users');
var fs = require('fs');
var router = express.Router();

router.get('/', function(req, res, next) {
  if(req.query.code != undefined){
    res.redirect('/mclass/live/'+req.query.code);
  }else{
    res.render('mclass/index',{"user":musr.getUser(req)});
  }
});

router.get('/*', function(req, res, next) {
  var url = req.url
  if(url.endsWith('/')) url.length--;
  url = url.substring(url.lastIndexOf('/')+1)
  res.render('mclass/live',{"user":musr.getUser(req),"livename":url});
});


module.exports = router;

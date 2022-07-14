var express = require('express');
var musr = require('./users');
var fs = require('fs');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.redirect("/mclass");
});

router.get('/ASL', function(req, res, next) {
  res.render('ASL');
});

module.exports = router;

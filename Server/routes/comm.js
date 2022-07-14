var express = require('express');
const session = require('express-session');
var router = express.Router();
var musr = require('./users');

var msg = [];

router.post('/query', function(req, res, next) {
  if(req.body.time!=undefined){
    var time=Number(req.body.time),i,len=msg.length;
    console.log(time);
    for(i=len-1;i>=0;i--){
      if(msg[i].time<=time) break;
    }
    console.log(i);
    var ret = {"success":true,"data":msg.slice(i+1)};
    console.log(ret);
    res.send(ret);
  }else{
    res.send({"success":false});
  }
});

router.post('/send',function(req,res,next){
  var data=req.body.data,time=req.body.time;
  if(!musr.isLogined(req)){
    res.send({"success":false,"msg":"login first"})
  }else{
    var msg0={"name":musr.getUser(req),"time":time,"data":data};
    msg.push(msg0);
    console.log(msg0);
    res.send({"success":true});
  }
});

module.exports = router;

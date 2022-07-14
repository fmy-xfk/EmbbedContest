var express = require('express');
var url = require('url');
var fs = require('fs');
const { match } = require('assert');
const { save } = require('debug/src/browser');

var usrdir=__dirname+"/userlist.json";
var users = JSON.parse(fs.readFileSync(usrdir)).users;
var online_users = {};

function save_users(){
  fs.writeFileSync(usrdir,JSON.stringify({"users":users}));
}

exports.login = function(name,pwd){
  var usr=users.find(e=>e.name===name);
  if(usr!=undefined && usr.pwd===pwd){
    online_users[name]=new Date().getTime();
    return online_users[name];
  }
  return -1;
}

exports.logout = function(name) {
  if(online_users[name]!=undefined){
    delete online_users[name];
    return true;
  }else{
    return false;
  }
}

exports.chpwd = function(name,oldpwd,newpwd) {
  var usr=users.find(e=>e.name===name);
  if(usr!=undefined && usr.pwd===oldpwd){
    usr.pwd=newpwd;
    save_users();
    return true;
  }
  return false;
}

function checkValidity(name,timestamp){
  return online_users[name]===timestamp;
}

exports.isAdmin = function(req) {
  if(req.session === undefined) return false;
  if(req.session.user === 'admin'){
    return checkValidity(req.session.user,req.session.timestamp);
  }else{
    return false;
  }
}

exports.isLogined = function(req) {
  if(req.session === undefined) return false;
  if (req.session.user===undefined || req.session.user===""){
    return false;
  }else{
    return checkValidity(req.session.user,req.session.timestamp);
  }
};

exports.getUser = function(req){
  if(req.session === undefined) return undefined;
  if (req.session.user!=undefined && req.session.user!="" && checkValidity(req.session.user,req.session.timestamp)){
    return req.session.user;
  }else{
    return undefined;
  }
}
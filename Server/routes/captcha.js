var express = require('express');
var svgCaptcha = require("svg-captcha");

function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}

var captcha_list=[];
var mutex=false;

function log_captcha_list() {
    console.log("CAPTCHA_LIST:");
    captcha_list.forEach(function(val){
        console.log(JSON.stringify({"text":val.text,"id":val.id,"expire":val.expire}));
    });
}

var last_clear_time=Date.now();

function clear_expired_captcha(){
    if(Date.now()-last_clear_time<600000) return; //Clear every 10min
    while(mutex);
    mutex=true;
    var new_list=[];
    captcha_list.forEach(function(val){
        if(val.expire>Date.now()){
            new_list.push(val);
        }
    });
    captcha_list=new_list;
    mutex=false;
}
/*
bsearch
par:
    id: id of a captcha structure to be searched
ret:
    success: a boolean, found or not
    pos: if found, pos will indicate its position, otherwise it indicate where it should be inserted in
*/
function bsearch(id){
    while(mutex);
    var l=0,r=captcha_list.length,m=Math.floor((l+r)/2),ret;
    while(l<r){
        if(captcha_list[m].id===id) {/*console.log("ok!");*/return {"success":true,"pos":m};}
        else if(captcha_list[m].id>id) r=m;
        else l=m+1;
        m=Math.floor((l+r)/2);
    }
    ret={"success":false,"pos":m};
    return ret;
}

/*
create
par:
    expire_ms:  expiration period, milisecond as unit
ret:
    text:   captcha string
    data:   svg image
    id:     a random string whose length is 32
    expire: time when the captcha will expire, describe as miliseconds from 19700101 to now
*/
exports.create = function (expire_ms=600000){
    var id=randomString(32),sret=bsearch(id);
    while(sret.success){
        id=randomString(32),sret=bsearch(id);
    }
    var ret=svgCaptcha.create({
        // 翻转颜色
        inverse: false,
        // 字体大小
        fontSize: 36,
        // 噪声线条数
        noise: 3,
        // 宽度
        width: 80,
        // 高度
        height: 30,
      });
    ret["id"]=id;
    ret["expire"]=expire_ms+Date.now();
    while(mutex);
    mutex=true;
    captcha_list.splice(sret.pos,0,ret);
    mutex=false;
    return ret;
}

/*
check
par:
    id, text
ret:
    a boolean
*/
exports.check = function(id,text){
    clear_expired_captcha();
    var sret=bsearch(id);
    if(sret.success){
        var one_cap=captcha_list[sret.pos];
        captcha_list.splice(sret.pos,1);
        if(one_cap.text.toLowerCase()===text.toLowerCase()){
            if(one_cap.expire<Date.now()){
                return {"success":false,"err":"expired-captcha"};
            }else{
                return {"success":true,"err":""};
            }
        }else{
            return {"success":false,"err":"wrong-text"};
        }
    }
    return {"success":false,"err":"invalid-captcha-id"};
}
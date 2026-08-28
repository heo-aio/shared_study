const express = require('express');
const router = express.Router(); // app의 router 기능만 수행

router.get('/hello', function(req, res){
    res.send("Router Module, GET !!");
});

router.post('/hello', function(req, res){
    res.json("Router Module, POST !!");
});

module.exports = router;
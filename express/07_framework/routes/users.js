var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('<h1>Express FrameWork 복잡하노</h1>');
});

module.exports = router;

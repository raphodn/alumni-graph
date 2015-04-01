var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  //res.send({})
  //req.query (/?age=14)
  //req.params (get('users/:id') & url users/33)
  res.render('index', { title: 'Express' });
});

module.exports = router;

// use strict code
"use strict";

// global node modules
var scrapers = require("./scrapers.js");
var helmet = require("helmet");
var express = require("express");
var app = express();
app.use(helmet());

// main logic
var time = new Date();
var port = 8080;


app.get("/fcc", function(req, res) {
  scrapers.mapScrape(req.query.user, res, mapFinish); // scrape map first to build a json structure
});

function mapFinish(err, user, data, map, res) {
  if (err) {
    res.status(500).jsonp({
      "_errors": err
    });
  } else {
    if (user) { // If username is given, then scrape profile
      if(data && map){
        scrapers.profileScrape(user, data, map, res, profileFinish);
      }
    } else {
      res.status(200).jsonp(data);
    }
  }
}

function profileFinish (err, user, data, map, res) {
  if (err) {
    res.status(500).jsonp({
      "_errors": err
    });
  } else {
    res.status(200).jsonp(data);
  }
}

app.listen(port, function() {
  console.info("[FCC-Profile-API]", "Server initialized at port " + port);
});

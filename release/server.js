// use strict code
"use strict";

// global node modules
var scrapers = require("./scrapers.js");
var helmet = require("helmet");
var express = require("express");
var http = require("http");
var https = require("https");
var fs = require("fs");
var app = express();
app.use(helmet());

// https certs
var certs = {
  key: fs.readFileSync("/srv/certs/shared.key", "utf8"),
  cert: fs.readFileSync("/srv/certs/shared.crt", "utf8")
};

// main logic
var time = new Date();

app.get("/fcc", function(req, res) {
  scrapers.mapScrape(req.query.user, res, mapFinish); // scrape map first to build a json structure
});

function mapFinish(err, user, data, map, res) {
  if (err) {
    res.status(500).jsonp({
      "Errors": err
    });
  } else {
    if (user) { // If username is given, then scrape profile
      if (data && map) {
        scrapers.profileScrape(user, data, map, res, profileFinish);
      }
    } else {
      res.status(200).jsonp(data);
    }
  }
}

function profileFinish(err, user, data, map, res) {
  if (err) {
    res.status(500).jsonp({
      "Errors": err
    });
  } else {
    res.status(200).jsonp(data);
  }
}

http.createServer(app).listen(80, function () {
   console.info("[FCC-Profile-API]", "HTTP server initialized");
});
https.createServer(certs, app).listen(443, function () {
   console.info("[FCC-Profile-API]", "HTTPS server initialized");
});

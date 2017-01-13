// global node modules
var fs       = require("fs");
var request  = require("request");
var cheerio  = require("cheerio");
var jsonfile = require("jsonfile");
var helmet   = require('helmet');
var express  = require('express');
var app      = express();
app.use(helmet());

// map functions
function mapScrape(baseUrl, user) {
  var mapObj = {};
  var keyObj = {};
  url = baseUrl + "map";
  var toDate = function(str) {
    var arr = str.split(" ");
    var date = new Date(0);
    if (arr[1].includes("hour")) {
      date.setHours(arr[0]);
    } else if (arr[1].includes("minute")) {
      date.setMinutes(arr[0]);
    } else {
      console.error("[Map Date Error]", str);
      terminate();
    }
    return date;
  };
  request(url, function(error, response, html) {
    if (error) {
      console.error("[Map Req Error]", url, error);
      terminate();
    } else {
      console.info("[Map Scrape]", "Start", url);
      var $ = cheerio.load(html);
      $("#accordion").each(function() { // loop > all tables
        // start certification loop
        $(this).find("div.certBlock").each(function() { // loop > all cert blocks
          var certName = $(this).prev().find("a").text().trim(); // get name in preceding tag
          mapObj[certName] = {}; // init object
          // start chapter loop
          $(this).find("div.chapterBlock").each(function() { // get all chapblock objects
            var chapName = $(this).prev().find("a").text().trim(); // get name in preceding tag
            var chapTime = $(this).prev().find(".challengeBlockTime").text().trim().slice(1, -1); // get time in preceding tag
            var chapDesc = $(this).find(".challengeBlockDescription").eq(0).text().trim();
            mapObj[certName][chapName] = {}; // init object
            mapObj[certName][chapName]["_date"] = toDate(chapTime);
            if (chapDesc) { // if description exists, add it to map
              mapObj[certName][chapName]["_desc"] = chapDesc;
            }
            // start challenge loop
            $(this).find("p.challenge-title").each(function() { // get all chapblock objects
              var chalName = "";
              if ($(this).find("span").length > 1) { // if span containers > 1
                chalName = $(this).find("span").eq(0).text().trim(); // get first span text
              } else {
                chalName = $($(this).contents()[0]).text().trim(); // get first content element text
              }
              chalName = chalName.replace(".", "");
              var chalSoon = $(this).find("em").text().trim();
              var chalLink = $(this).find("a").attr("href"); // get link
              mapObj[certName][chapName][chalName] = {}; // init object
              if (chalSoon) {
                mapObj[certName][chapName][chalName]["_status"] = chalSoon;
              } else if (chalLink) {
                chalLink = baseUrl + chalLink;
                linkCount++;
                mapObj[certName][chapName][chalName]["_link"] = chalLink;
                keyObj[chalName] = [certName, chapName];
              }
            });
          });
        });
      });
      console.info("[Map Scrape]", "Complete", url);
      if (user){
        profileScrape(baseUrl, user, mapObj, keyObj);
      }
    }
  });
}

// profile function
function profileScrape(baseUrl, user, mapObj, keyObj) {
  var url = baseUrl + user;
  request(url, function(error, response, html) {
    if (error) {
      console.error("[Profile Req Error]", url, error);
      terminate();
    } else {
      console.info("[Profile Scrape]", "Start", url);
      var $ = cheerio.load(html);
      mapObj["Deprecated"] = {};
      $("table.table").each(function() { // loop > all tables
        $(this).find("tr").each(function() {
          if (!$(this).find("th").length) {
            var chalName = $(this).find("td.col-xs-12.visible-xs a").text().trim();
            var chalDateC = $(this).find("td.col-xs-2.hidden-xs").eq(0).text().trim();
            var chalDateU = $(this).find("td.col-xs-2.hidden-xs").eq(1).text().trim();
            var chalCode = $(this).find("td.col-xs-12.visible-xs a").attr("href"); // get link
            if (chalCode.includes("?solution=")) {
              chalCode = baseUrl + chalCode;
            } else if (chalCode.includes("/challenges/")) {
              chalCode = "";
            }
            if (keyObj.hasOwnProperty(chalName)) {
              certName = keyObj[chalName][0];
              chapName = keyObj[chalName][1];
              mapObj[certName][chapName][chalName]["_dateC"] = chalDateC;
              if (chalDateU) {
                mapObj[certName][chapName][chalName]["_dateU"] = chalDateU;
              }
              if (chalCode) {
                mapObj[certName][chapName][chalName]["_code"] = chalCode;
              }
            } else {
              console.error("[Profile Error]", "Deprecated", chalName, chalDateC);
              mapObj["Deprecated"][chalName] = {};
              mapObj["Deprecated"][chalName]["_dateC"] = chalDateC;
              if (chalDateU) {
                mapObj["Deprecated"][chalName]["_dateU"] = chalDateU;
              }
              mapObj["Deprecated"][chalName]["_code"] = chalCode;
            }
          }
        });
      });
      console.info("[Profile Scrape]", "Complete", url);
      console.log(mapObj);
    }
  });
}

function terminate() {
  console.error("[Fatal Error]", "Terminated");
  process.exit(1);
}

// main logic
mapScrape("https://www.freecodecamp.com/", "htko89");

// app.get('/', function (req, res) {
//   res.send('Hello World!')
//   // res.jsonp(obj)
// })
//
// app.listen(3000, function () {
//   console.log('Example app listening on port 3000!')
// })

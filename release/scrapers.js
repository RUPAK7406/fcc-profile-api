// use strict code
"use strict";

// global node modules
var request = require("request");
var cheerio = require("cheerio");

// global variables
var baseUrl = "https://www.freecodecamp.com/";

// map functions
var mapScrape = function(user, res, callback) {
  var url = baseUrl + "map";
  console.info("[Map Scrape]", "Start", url);
  var data = {
    "_map": []
  };
  var map = {};
  var toDate = function(str) {
    var arr = str.split(" ");
    var date = new Date(0);
    if (arr[1].includes("hour")) {
      date.setHours(arr[0]);
    } else if (arr[1].includes("minute")) {
      date.setMinutes(arr[0]);
    } else {
      date = null;
    }
    return date;
  };
  request(url, function(error, response, html) {
    if (error) {
      var err = {
        "_message": "Cannot request freeCodeCamp map",
        "_url": url,
        "_error": error
      };
      console.error("[Error]", err);
      callback(err, user, null, null, res);
    } else {
      console.info("[Map Process]", "Request", url);
      var $ = cheerio.load(html);
      $("#accordion").each(function() { // loop > all tables
        // start certification loop
        $(this).find("div.certBlock").each(function(certIdx) { // loop > all cert blocks
          var certName = $(this).prev().find("a").text().trim(); // get name in preceding tag
          data["_map"][certIdx] = { // init object
            "_name": certName,
            "_data": []
          };
          // start chapter loop
          $(this).find("div.chapterBlock").each(function(chapIdx) { // get all chapblock objects
            var chapName = $(this).prev().find("a").text().trim(); // get name in preceding tag
            var chapTime = $(this).prev().find(".challengeBlockTime").text().trim().slice(1, -1); // get time in preceding tag
            var chapDesc = $(this).find(".challengeBlockDescription").eq(0).text().trim();
            data["_map"][certIdx]["_data"][chapIdx] = { // init object
              "_name": chapName,
              "_data": []
            }
            data["_map"][certIdx]["_data"][chapIdx]["_time"] = toDate(chapTime);
            if (chapDesc) { // if description exists, add it to map
              data["_map"][certIdx]["_data"][chapIdx]["_desc"] = chapDesc;
            }
            // start challenge loop
            $(this).find("p.challenge-title").each(function(chalIdx) { // get all chapblock objects
              var chalName = "";
              if ($(this).find("span").length > 1) { // if span containers > 1
                chalName = $(this).find("span").eq(0).text().trim(); // get first span text
              } else {
                chalName = $($(this).contents()[0]).text().trim(); // get first content element text
              }
              chalName = chalName.replace(".", "");
              chalName = chalName.replace("-", "");
              chalName = chalName.replace("()", "");
              var chalSoon = $(this).find("em").text().trim();
              var chalLink = $(this).find("a").attr("href"); // get link
              data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx] = { // init object
                "_name": chalName
              }
              if (chalSoon) {
                data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx]["_status"] = chalSoon;
              } else if (chalLink) {
                if (chalLink.charAt(0) === "/") {
                  chalLink = chalLink.slice(1);
                }
                chalLink = baseUrl + chalLink;
                data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx]["_link"] = chalLink;
                map[chalName] = [certIdx, chapIdx, chalIdx];
              }
            });
          });
        });
      });
      console.info("[Map Process]", "Complete", url);
      callback(null, user, data, map, res);
    }
  });
};

// profile function
var profileScrape = function(user, data, map, res, callback) {
  var url = baseUrl + user;
  console.info("[Profile Scrape]", "Request", url);
  request(url, function(error, response, html) {
    if (error) {
      var err = {
        "_message": "Cannot request freeCodeCamp profile",
        "_url": url,
        "_error": error
      };
      console.error("[Error]", err);
      callback(err, user, null, null, res);
    } else {
      console.info("[Profile Process]", "Start", url);
      var $ = cheerio.load(html);
      var deprIdx = 0;
      $("table.table").each(function() { // loop > all tables
        $(this).find("tr").each(function() {
          if (!$(this).find("th").length) {
            var chalName = $(this).find("td.col-xs-12.visible-xs a").text().trim();
            var chalDateC = $(this).find("td.col-xs-2.hidden-xs").eq(0).text().trim();
            var chalDateU = $(this).find("td.col-xs-2.hidden-xs").eq(1).text().trim();
            var chalCode = $(this).find("td.col-xs-12.visible-xs a").attr("href"); // get link
            if (chalCode.charAt(0) === "/") {
              chalCode = chalCode.slice(1);
            }
            if (chalCode.includes("?solution=")) {
              chalCode = baseUrl + chalCode;
            } else if (chalCode.includes("/challenges/")) {
              chalCode = "";
            }
            if (map.hasOwnProperty(chalName)) {
              var certIdx = map[chalName][0];
              var chapIdx = map[chalName][1];
              var chalIdx = map[chalName][2];
              data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx]["_dateC"] = chalDateC;
              if (chalDateU) {
                data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx]["_dateU"] = chalDateU;
              }
              if (chalCode) {
                data["_map"][certIdx]["_data"][chapIdx]["_data"][chalIdx]["_code"] = chalCode;
              }
            } else {
              if (!data.hasOwnProperty('_deprecated')){
                data["_deprecated"] = []; // init object
              }
              data["_deprecated"][deprIdx] = { // init object
                "_name": chalName
              };
              data["_deprecated"][deprIdx] = {};
              data["_deprecated"][deprIdx]["_dateC"] = chalDateC;
              if (chalDateU) {
                data["_deprecated"][deprIdx]["_dateU"] = chalDateU;
              }
              data["_deprecated"][deprIdx]["_code"] = chalCode;
              deprIdx++;
            }
          }
        });
      });
      console.info("[Profile Process]", "Complete", url);
      callback(null, user, data, map, res);
    }
  });
};

// exports
module.exports.mapScrape = mapScrape;
module.exports.profileScrape = profileScrape;

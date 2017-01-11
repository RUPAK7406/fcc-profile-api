// global node modules
var fs = require("fs");
var request = require("request");
var cheerio = require("cheerio");
var jsonfile = require("jsonfile");

// map functions
function mapScrape(url) {
  url = url + "/map";
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
                descScrape(certName, chapName, chalName, chalLink);
                keyObj[chalName] = [certName, chapName];
              }
            });
          });
        });
      });
      console.info("[Map Scrape]", "Complete", url);
    }
  });
}
// desc function
function descScrape(certName, chapName, chalName, chalLink) {
  var chalDesc = "";
  var toDesc = function(str) {
    return "* " + str + "\n";
  };
  request(chalLink, function(error, response, html) {
    if (error) {
      console.error("[Desc Req Error]", chalLink, error);
      terminate();
    } else {
      if (descCount === 1) {
        console.info("[Desc Scrape]", "Start", linkCount);
      }
      var $ = cheerio.load(html);
      console.log("[Desc Scrape]", chalLink);
      var chalType = -1;
      if ($(".challenge-instructions").length) {
        chalType = 0;
        $(".challenge-instructions p").each(function() {
          chalDesc += toDesc($(this).text().trim());
        });
      } else if ($(".step-text").length) {
        chalType = 3;
        $(".step-text").each(function() {
          chalDesc += toDesc($(this).text().trim());
        });
      } else if ($(".challenge-step-description").length) {
        chalType = 7;
        $(".challenge-step-description").each(function() {
          chalDesc += toDesc($(this).text().trim());
        });
      } else if ($("article").length) {
        chalType = 99;
        $("article p").each(function() {
          chalDesc += toDesc($(this).text().trim());
        });
      } else {
        console.error("[Desc Type Error]", chalLink);
        terminate();
      }
      if (chalDesc) {
        mapObj[certName][chapName][chalName]["_desc"] = chalDesc;
        mapObj[certName][chapName][chalName]["_type"] = chalType;
      }
      descCount++;
      if (linkCount === descCount) {
        console.info("[Desc Scrape]", "Complete", descCount);
        // console.log(mapObj);
        // write json
        var path = dataDir + "/map.json";
        jsonfile.writeFileSync(path, mapObj, {
          spaces: 2
        }, function(error) {
          console.error("[JSON Error]", error);
          terminate();
        });
        console.info("[JSON Write]", "Complete", path);
        // write json
        path = dataDir + "/map.key.json";
        jsonfile.writeFileSync(path, keyObj, {
          spaces: 2
        }, function(error) {
          console.error("[JSON Error]", error);
          terminate();
        });
        console.info("[JSON Write]", "Complete", path);
        if (fullRun) {
          profileScrape(baseUrl);
        }
      }
    }
  });
}
// profile function
function profileScrape(url) {
  request(url + "/" + user, function(error, response, html) {
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
      // console.log(mapObj);
      // write json
      var path = dataDir + "/profile.json";
      jsonfile.writeFileSync(path, mapObj, {
        spaces: 2
      }, function(error) {
        console.error("[JSON Error]", error);
        terminate();
      });
      console.info("[JSON Write]", "Complete", path);
    }
  });
}

function checkArg(str, title) {
  str = args[3];
  if (!str) {
    console.error("[Args Error]", "Must supply " + title);
    terminate();
  } else {
    return str;
  }
}

function terminate() {
  console.error("[Fatal Error]", "Terminated");
  process.exit(1);
}

// global variables
var dataDir = "/Users/sysuser/Google Drive/folio/public/code/fcc/fcc-spider/release/data";
var baseUrl = "https://www.freecodecamp.com";
var linkCount = 0;
var descCount = 0;
var mapObj = {};
var keyObj = {};
var args = process.argv;
var user;
var fullRun;

// main logic
if (args[2] === "map") {
  fullRun = false;
  mapScrape(baseUrl);
} else if (args[2] === "profile") {
  user = checkArg(args[3], "username");
  fullRun = false;
  profileScrape(baseUrl);
} else if (args[2] === "full") {
  user = checkArg(args[3], "username");
  fullRun = true;
  mapScrape(baseUrl);
} else {
  checkArg(args[2], "program");
}

var fs = require("fs");
var request = require("request");
var cheerio = require("cheerio");
function parseDate(str){
  var arr = str.split(" ");
  var date = new Date(0);
  if (arr[1].includes("hour")){
    date.setHours(arr[0])
  } else if (arr[1].includes("minute")){
    date.setMinutes(arr[0])
  } else {
    console.log("Date Error",str)
  }
  return date;
}
function scrape (url){
  request(url, function(error, response, html){
      if(error){
        console.log(error);
      } else {
        var $ = cheerio.load(html);
        var map = {};
        $("#accordion").each(function() { // loop > all tables
          $(this).find("div.certBlock").each(function() { // loop > all cert blocks
            var certName = $(this).prev().find("a").text().trim(); // get name in preceding tag
            map[certName] = {}; // init object
            $(this).find("div.chapterBlock").each(function() { // get all chapblock objects
              var chapName = $(this).prev().find("a").text().trim(); // get name in preceding tag
              var chapTime = $(this).prev().find(".challengeBlockTime").text().slice(1, -1); // get time in preceding tag
              var chapDesc = $(this).find(".challengeBlockDescription").eq(0).text();
              map[certName][chapName] = {};
              map[certName][chapName]["_date"] = parseDate(chapTime);
              if(chapDesc){
                map[certName][chapName]["_desc"] = chapDesc;
              }
              $(this).find("p.challenge-title").each(function() {               // get all chapblock objects
                var chalName = "";
                if ( $(this).find("span").length > 1 ){
                  chalName = $(this).find("span").eq(0).text().trim();
                } else {
                  chalName = $($(this).contents()[0]).text().trim();
                }
                var chalLink = $(this).find("a").attr("href")
                map[certName][chapName][chalName] = {};
                if(chalLink){
                  map[certName][chapName][chalName]["_link"] = chalLink;
                }
              });
            });
          });
        });
        console.log(map);
      }
  })
}
scrape("https://www.freecodecamp.com/map");

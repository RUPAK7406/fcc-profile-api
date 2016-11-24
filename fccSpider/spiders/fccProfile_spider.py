import scrapy
from collections import OrderedDict
import json
import os


class fccProfile(scrapy.Spider):
    name = "profile"
    def __init__(self, username=None, *args, **kwargs):
        super(fccProfile, self).__init__(*args, **kwargs)
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]


    def parse(self, response):
        self.log("Scraped: " + response.url)
        # Clear String Function
        def clrstr(string):
            string = str(string).lstrip()
            if string == "None":
                string = ""
            return string
        # Setup Paths
        resultPath = os.getcwd() + "/output/map.json"
        lookupPath = os.getcwd() + "/output/map.lookup.json"
        failedPath = os.getcwd() + "/output/map.failed.json"
        # Setup Dictionaries
        with open(resultPath) as output:
            result = json.load(output, object_pairs_hook=OrderedDict)
        with open(lookupPath) as output:
            lookup = json.load(output, object_pairs_hook=OrderedDict)
        failed = OrderedDict()
        # Start Scraping
        self.log("Loop Start")
        for table in response.css(".table-striped"):
            # Ignore table separation because it is not organized the same way as the map.
            for challenge in table.css("tr"):
                name = clrstr( challenge.css("td.col-xs-12.visible-xs a::text").extract_first() )
                if name:
                    date = challenge.css("td.col-xs-2.hidden-xs::text").extract()
                    link = clrstr( challenge.css("td.col-xs-12.visible-xs a::attr(href)").extract_first() )
                    if len(date) == 1: # if date only contains `completed date`
                        date.append("") # append empty date
                    if "?solution=" in link:
                        code = link.split("?",1)[1][9:]
                    else:
                        code = ""
                    if name in lookup.keys():
                        parent = lookup[name]
                        result[parent[0]][parent[1]][name]["_dateC"] = clrstr(date[0])
                        result[parent[0]][parent[1]][name]["_dateU"] = clrstr(date[1])
                        result[parent[0]][parent[1]][name]["_code"] = code
                    else:
                        failed[name] = OrderedDict()
                        failed[name]["_link"] = link
                        failed[name]["_dateC"] = clrstr(date[0])
                        failed[name]["_dateU"] = clrstr(date[1])
                        failed[name]["_code"] = code
                        self.log(name+" ("+date[0]+") no longer exists in FCC's curriculum map")
        self.log("Loop End")
        # Output to JSON
        self.log("Output: "+resultPath)
        with open(resultPath, "w") as output:
            json.dump(result, output, indent=2)
        with open(failedPath, "w") as output:
            json.dump(failed, output, indent=2)


# re(r"(^.*)?\?")

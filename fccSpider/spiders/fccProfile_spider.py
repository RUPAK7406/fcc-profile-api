import scrapy
from collections import OrderedDict
import json
import os


class fccProfile(scrapy.Spider):
    name = "fccProfile"
    def __init__(self, username=None, *args, **kwargs):
        super(fccProfile, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]


    def parse(self, response):
        # Clear string function
        def clrstr(string):
            string = str(string).lstrip()
            if string == "None":
                string = ""
            return string
        # Setup Paths
        resultPath = os.getcwd() + "/output/fccMap.json"
        lookupPath = os.getcwd() + "/output/fccMap.lookup.json"
        # Setup dictionaries
        with open(resultPath) as output:
            result = json.load(output, object_pairs_hook=OrderedDict)
        with open(lookupPath) as output:
            lookup = json.load(output, object_pairs_hook=OrderedDict)
        # Start scraping
        self.log("Loop Start")
        for table in response.css(".table-striped"):
            # Ignore table separation because it is not organized the same way as the map.
            for challenge in table.css("tr"):
                name = clrstr( challenge.css("td.col-xs-12.visible-xs a::text").extract_first() )
                if name:
                    date = challenge.css("td.col-xs-2.hidden-xs::text").extract()
                    link = clrstr( challenge.css("td.col-xs-12.visible-xs a::attr(href)").extract_first() )
                    self.log(link)
                    if len(date) == 1: # if date only contains `completed date`
                        date.append("") # append empty date
                    date = clrstr(date)
                    if "solution=" in link:
                        link = link.split("?",1)[0]
                        code = link.split("?",1)[1]
                    else:
                        code = ""
                    if name in lookup.keys():
                        parent = lookup[name]
                        result[parent[0]][parent[1]][name]["_link"] = link
                        result[parent[0]][parent[1]][name]["_dateC"] = date[0]
                        result[parent[0]][parent[1]][name]["_dateU"] = date[1]
                        result[parent[0]][parent[1]][name]["_code"] = code
                    else:
                        self.log(name+" ("+date[0]+") no longer exists in FCC's curriculum map")
        self.log("Loop End")
        self.log("Output: "+resultPath)
        with open(resultPath, "w") as output:
            json.dump(result, output, indent=2)


# re(r"(^.*)?\?")

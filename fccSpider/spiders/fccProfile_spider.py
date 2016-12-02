import scrapy
from collections import OrderedDict
import json
import os


class fccProfile(scrapy.Spider):

    # Init
    name = "profile"
    # Setup Paths
    resultPath = os.getcwd() + "/output/map.json"
    lookupPath = os.getcwd() + "/output/map.lookup.json"
    failedPath = os.getcwd() + "/output/map.failed.json"
    # Setup Dictionaries
    result = OrderedDict()
    lookup = OrderedDict()
    failed = OrderedDict()

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccProfile, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.resultPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        with open(self.lookupPath) as output:
            self.lookup = json.load(output, object_pairs_hook=OrderedDict)
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        self.log("Output: " + self.resultPath)
        with open(self.resultPath, "w") as output:
            json.dump(self.result, output, indent=2)
        with open(self.failedPath, "w") as output:
            json.dump(self.failed, output, indent=2)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).lstrip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Scraping
        self.log("Scraping: " + response.url)
        for table in response.css(".table-striped"):
            # Ignore table separation because it is not organized the same way as the map.
            for challenge in table.css("tr"):
                name = self.clrstr( challenge.css("td.col-xs-12.visible-xs a::text").extract_first() )
                if name:
                    date = challenge.css("td.col-xs-2.hidden-xs::text").extract()
                    link = self.clrstr( challenge.css("td.col-xs-12.visible-xs a::attr(href)").extract_first() )
                    if len(date) == 1: # if date only contains `completed date`
                        date.append("") # append empty date
                    if "?solution=" in link:
                        code = link.split("?",1)[1][9:]
                    else:
                        code = link
                    if name in self.lookup.keys(): # Add to database if challenge name is still in lookup (still exists on FCC)
                        parent = self.lookup[name]
                        self.result[parent[0]][parent[1]][name]["_status"] = "Complete"
                        self.result[parent[0]][parent[1]][name]["_dateC"] = self.clrstr(date[0])
                        self.result[parent[0]][parent[1]][name]["_dateU"] = self.clrstr(date[1])
                        self.result[parent[0]][parent[1]][name]["_code"] = code
                    else: # Add to failed dictionary
                        self.failed[name] = OrderedDict()
                        self.failed[name]["_link"] = link
                        self.failed[name]["_dateC"] = self.clrstr(date[0])
                        self.failed[name]["_dateU"] = self.clrstr(date[1])
                        self.failed[name]["_code"] = code
                        self.log("Deprecated: (" + date[0] + ") " + name)
        self.log("Scraped: " + response.url)

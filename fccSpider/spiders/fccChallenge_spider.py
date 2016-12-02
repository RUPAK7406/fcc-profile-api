import scrapy
from collections import OrderedDict
import json
import os


class fccChallenge(scrapy.Spider):

    # Init
    name = "challenge"
    # Setup Paths
    resultPath = os.getcwd() + "/output/map.json"
    lookupPath = os.getcwd() + "/output/map.lookup.json"
    failedPath = os.getcwd() + "/output/map.failed.json"
    # Setup Dictionaries
    result = OrderedDict()
    lookup = OrderedDict()
    failed = OrderedDict()
    lookupurl = OrderedDict()

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccChallenge, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.lookupPath) as output:
            self.lookup = json.load(output, object_pairs_hook=OrderedDict)
        with open(self.resultPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        # Setup URLs
        self.start_urls = []
        for name in self.lookup.keys():
            parent = self.lookup[name]
            link = self.result[parent[0]][parent[1]][name]["_link"]
            lookupurl[link] = name
            if link:
                link = "https://www.freecodecamp.com" + link
                self.start_urls.append(link)

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        self.log("Output: " + self.resultPath)
        # self.log("Output: " + self.lookupPath)
        with open(self.resultPath, "w") as output:
            json.dump(self.result, output, indent=2)
        # with open(self.lookupPath, "w") as output:
        #     json.dump(self.lookup, output, indent=2)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).lstrip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Scraping
        # self.log("Scraping: " + response.url)
        link = response.url[28:]
        name = lookupurl[link]
        parent = self.lookup[name]
        if response.css(".challenge-instructions").extract_first(): # Standard (0). Parent. Child: p.  Misc: .challenge-instructions-title
            self.result[parent[0]][parent[1]][name]["_desc"] = '/n'.join( response.css(".challenge-instructions p::text").extract() )
            self.log("Type 0")
        elif response.css(".step-text").extract_first(): # Project (3). Child. misc: .challenge-instructions-title
            self.result[parent[0]][parent[1]][name]["_desc"] ='/n'.join( response.css(".step-text::text").extract() )
            self.log("Type 3")
        elif response.css(".challenge-step-description").extract_first(): # Full Page (7). Child. Misc: .challenge-step .challenge-step-counter
            self.result[parent[0]][parent[1]][name]["_desc"] = '/n'.join( response.css(".challenge-step-description::text").extract() )
            self.log("Type 7")
        elif response.css("article").extract_first(): # Video (99). Parent. Child: p. Misc:
            self.result[parent[0]][parent[1]][name]["_desc"] = '/n'.join( response.css("article p::text").extract() )
            self.log("Type 99")
        else:
            self.log("Invalid Type: " + response.url)
        # self.log("Scraped: " + response.url)

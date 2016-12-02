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
            status = self.result[parent[0]][parent[1]][name]["_status"]
            self.lookupurl[link] = name
            if link and status != "Coming Soon" :
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
        name = self.lookupurl[link]
        parent = self.lookup[name]
        text = ""
        if response.css(".challenge-instructions").extract_first(): # Standard (0). Parent. Child: p.  Misc: .challenge-instructions-title
            for tag in response.css(".challenge-instructions p"):
                text = text + "".join( tag.css("::text").extract() ) + "\n"
        elif response.css(".step-text").extract_first(): # Project (3). Child. misc: .challenge-instructions-title
            for tag in response.css(".step-text"):
                text = text + "".join( tag.css("::text").extract() ) + "\n"
        elif response.css(".challenge-step-description").extract_first(): # Full Page (7). Child. Misc: .challenge-step .challenge-step-counter
            for tag in response.css(".challenge-step-description"):
                text = text + "".join( tag.css("::text").extract() ) + "\n"
        elif response.css("article").extract_first(): # Video (99). Parent. Child: p. Misc:
            for tag in response.css("article p"):
                text = text + "".join( tag.css("::text").extract() ) + "\n"
        else:
            text = "Invalid type."
        self.result[parent[0]][parent[1]][name]["_desc"] = self.clrstr( text )
        # self.log("Scraped: " + response.url)

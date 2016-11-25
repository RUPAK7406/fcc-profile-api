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
            if link:
                link = "https://www.freecodecamp.com" + link
                self.start_urls.append(link)
                self.log("Added: " + link)

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        # self.log("Output: " + self.resultPath)
        # self.log("Output: " + self.lookupPath)
        # with open(self.resultPath, "w") as output:
        #     json.dump(self.result, output, indent=2)
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
        self.log("Scraping: " + response.url)
        # Content
        self.log("Scraped: " + response.url)

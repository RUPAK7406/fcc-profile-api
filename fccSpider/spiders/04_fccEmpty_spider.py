import scrapy
from collections import OrderedDict
import json
import os

class fccEmpty(scrapy.Spider):

    # Init
    name = "empty"
    # Setup Folder Paths
    curDir = os.getcwd()
    commonDir = curDir + "/common"
    exportDir = curDir + "/export"
    # Setup File Paths
    emptyPath = commonDir + "/empty.json"
    resultPath = commonDir + "/result.json"
    deprecatedPath = commonDir + "/deprecated.json"
    # Setup Dictionaries
    result = OrderedDict()
    deprecated = OrderedDict()

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccEmpty, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.emptyPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        with open(self.resultPath, "w") as output:
            self.log("Output: " + self.resultPath)
            json.dump(self.result, output, indent=2)
        with open(self.deprecatedPath, "w") as output:
            self.log("Output: " + self.deprecatedPath)
            json.dump(self.deprecated, output, indent=2)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).strip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Scraping
        pass

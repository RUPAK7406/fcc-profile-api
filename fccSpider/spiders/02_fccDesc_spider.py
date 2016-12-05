import scrapy
from collections import OrderedDict
import json
import os

class fccDesc(scrapy.Spider):

    # Init
    name = "desc"
    # Setup Folder Paths
    curDir = os.getcwd()
    commonDir = curDir + "/common"
    exportDir = curDir + "/export"
    # Setup File Paths
    resultPath = commonDir + "/result.json"
    failedPath = commonDir + "/failed.json"
    nameDictPath = commonDir + "/nameDict.json"
    linkDictPath = commonDir + "/linkDict.json"
    # Setup Dictionaries
    result = OrderedDict()
    failed = OrderedDict()
    nameDict = OrderedDict()
    linkDict = OrderedDict()

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccDesc, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.resultPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        with open(self.linkDictPath) as output:
            self.linkDict = json.load(output, object_pairs_hook=OrderedDict)
        # Setup URLs
        self.start_urls = []
        for chalLink in self.linkDict.keys():
            chalPath = self.linkDict[chalLink]
            chalStatus = self.result[chalPath[0]][chalPath[1]][chalPath[2]]["_status"]
            if chalLink and chalStatus != "Coming Soon" :
                chalLink = "https://www.freecodecamp.com" + chalLink
                self.start_urls.append(chalLink)

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        with open(self.resultPath, "w") as output:
            self.log("Output: " + self.resultPath)
            json.dump(self.result, output, indent=2)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).strip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Scraping
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
        chalLink = self.clrstr( response.url )[28:]
        chalPath = self.linkDict[chalLink]
        self.result[chalPath[0]][chalPath[1]][chalPath[2]]["_desc"] = self.clrstr( text )

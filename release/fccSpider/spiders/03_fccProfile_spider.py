import scrapy
from collections import OrderedDict
import json
import os

class fccProfile(scrapy.Spider):

    # Init
    name = "profile"
    # Setup Folder Paths
    curDir = os.getcwd()
    commonDir = curDir + "/common"
    exportDir = curDir + "/export"
    # Setup File Paths
    emptyPath = commonDir + "/empty.json"
    resultPath = commonDir + "/result.json"
    deprecatedPath = exportDir + "/deprecated.json"
    nameDictPath = commonDir + "/nameDict.json"
    # Setup Dictionaries
    result = OrderedDict()
    deprecated = OrderedDict()
    nameDict = OrderedDict()

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccProfile, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.emptyPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        with open(self.nameDictPath) as output:
            self.nameDict = json.load(output, object_pairs_hook=OrderedDict)
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
        for table in response.css(".table-striped"):
            # Ignore table separation because it is not organized the same way as the map.
            for chal in table.css("tr"):
                chalName = self.clrstr( chal.css("td.col-xs-12.visible-xs a::text").extract_first() )
                if chalName:
                    chalDate = chal.css("td.col-xs-2.hidden-xs::text").extract()
                    chalLink = self.clrstr( chal.css("td.col-xs-12.visible-xs a::attr(href)").extract_first() )
                    if len(chalDate) == 1: # if date only contains `completed date`
                        chalDate.append("") # append empty date
                    if "?solution=" in chalLink:
                        chalcodeType = "code"
                        chalCode = chalLink.split("?",1)[1][9:]
                    else:
                        chalCodeType = "url"
                        chalCode = chalLink
                    if chalName in self.nameDict.keys(): # Add to database if challenge name is still in nameDict (still exists on FCC)
                        chalPath = self.nameDict[chalName]
                        self.result[chalPath[0]][chalPath[1]][chalName]["_status"] = "Complete"
                        self.result[chalPath[0]][chalPath[1]][chalName]["_dateC"] = self.clrstr(chalDate[0])
                        self.result[chalPath[0]][chalPath[1]][chalName]["_dateU"] = self.clrstr(chalDate[1])
                        self.result[chalPath[0]][chalPath[1]][chalName]["_codeType"] = chalCodeType
                        self.result[chalPath[0]][chalPath[1]][chalName]["_code"] = chalCode
                    else: # Add to deprecated dictionary
                        self.deprecated[chalName] = OrderedDict()
                        self.deprecated[chalName]["_link"] = chalLink
                        self.deprecated[chalName]["_dateC"] = self.clrstr(chalDate[0])
                        self.deprecated[chalName]["_dateU"] = self.clrstr(chalDate[1])
                        self.deprecated[chalName]["_codeType"] = chalCodeType
                        self.deprecated[chalName]["_code"] = chalCode
                        self.log("Deprecated: (" + chalDate[0] + ") " + chalName)

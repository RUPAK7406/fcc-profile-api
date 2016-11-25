import scrapy
from collections import OrderedDict
import json
import os


class fccMap(scrapy.Spider):

    # Init
    name = "map"
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
        super(fccMap, self).__init__(*args, **kwargs)
        # Load Files
            # None
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/map"]
            # debug url http://local.htko.ca/sources/map.html
            # production url https://www.freecodecamp.com/map

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        self.log("Output: " + self.resultPath)
        self.log("Output: " + self.lookupPath)
        with open(self.resultPath, "w") as output:
            json.dump(self.result, output, indent=2)
        with open(self.lookupPath, "w") as output:
            json.dump(self.lookup, output, indent=2)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).lstrip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Scraping
        self.log("Scraping: " + response.url)
        for table in response.css("#accordion"):
            # Only one table, skip a level in dictionary.
            for certIdx, cert in enumerate(table.css("div.certBlock")): #list certs in table and loop
                certName = self.clrstr( table.css("h2 > a::text").extract()[certIdx] ) #find the title
                self.result[certName] = OrderedDict() #set up empty dictionary under title
                for chapIdx, chap in enumerate(cert.css("div.chapterBlock")): #list chapters in cert and loop
                    chapName = self.clrstr( cert.css("h3 > a::text").extract()[chapIdx] ) #find the title
                    chapTime = self.clrstr( cert.css("h3 > .challengeBlockTime::text").extract()[chapIdx] ) #find the title
                    chapDesc = self.clrstr( chap.css(".challengeBlockDescription::text").extract_first() )
                    if not chapDesc:
                        chapDesc = ""
                    self.result[certName][chapName] = OrderedDict() #set up empty dictionary under title
                    self.result[certName][chapName]["_time"] = chapTime[1:-1]
                    self.result[certName][chapName]["_desc"] = chapDesc
                    for chalIdx, chal in enumerate(chap.css("p.challenge-title")): #list challenges in chapters and loop
                        chalName = self.clrstr(   chal.css("::text").extract_first() ).replace(".", "") # find the name
                        chalLink = self.clrstr(   chal.css("a::attr(href)").extract_first() ) #find the link
                        chalStatus = self.clrstr( chal.css("a span.sr-only::text").extract_first() ) #find the status
                        chalExist = self.clrstr(  chal.css("em::text").extract_first() ) #find if it exists
                        if chalExist:
                            chalStatus = chalExist
                        if chal.css(".disabled.ion-locked"):
                            chalStatus = "Locked"
                        self.result[certName][chapName][chalName] = OrderedDict()
                        self.result[certName][chapName][chalName]["_status"] = chalStatus
                        self.result[certName][chapName][chalName]["_link"] = chalLink
                        self.result[certName][chapName][chalName]["_dateC"] = ""
                        self.result[certName][chapName][chalName]["_dateU"] = ""
                        self.result[certName][chapName][chalName]["_desc"] = ""
                        self.result[certName][chapName][chalName]["_req"] = ""
                        self.result[certName][chapName][chalName]["_code"] = ""
                        self.lookup[chalName] = [certName,chapName]
        self.log("Scraped: " + response.url)

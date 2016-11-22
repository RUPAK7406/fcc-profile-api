import scrapy
from collections import OrderedDict
import json
import os


class fccMap(scrapy.Spider):
    name = "fccMap"
    def __init__(self, username=None, *args, **kwargs):
        super(fccMap, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.freecodecamp.com/map"]
        # debug url http://local.htko.ca/map.html
        # production url https://www.freecodecamp.com/map


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
        result = OrderedDict()
        lookup = OrderedDict()
        # Start scraping
        self.log("Loop Start")
        for table in response.css("#accordion"):
            # only one table, so no need to find titles. Skip a subsection for dictionary.
            for certIdx, cert in enumerate(table.css("div.certBlock")): #list certs in table and loop
                certName = clrstr( table.css("h2 > a::text").extract()[certIdx] ) #find the title
                result[certName] = OrderedDict() #set up empty dictionary under title
                for chapIdx, chap in enumerate(cert.css("div.chapterBlock")): #list chapters in cert and loop
                    chapName = clrstr( cert.css("h3 > a::text").extract()[chapIdx] ) #find the title
                    chapTime = clrstr( cert.css("h3 > .challengeBlockTime::text").extract()[chapIdx] ) #find the title
                    chapDesc = clrstr( chap.css(".challengeBlockDescription::text").extract_first() )
                    if not chapDesc:
                        chapDesc = ""
                    result[certName][chapName] = OrderedDict() #set up empty dictionary under title
                    result[certName][chapName]["_time"] = chapTime[1:-1]
                    result[certName][chapName]["_desc"] = chapDesc
                    for chalIdx, chal in enumerate(chap.css("p.challenge-title")): #list challenges in chapters and loop
                        chalName = clrstr(   chal.css("::text").extract_first() )
                        chalLink = clrstr(   chal.css("a::attr(href)").extract_first() ) #find the link
                        chalStatus = clrstr( chal.css("a span.sr-only::text").extract_first() ) #find the status
                        chalExist = clrstr(  chal.css("em::text").extract_first() ) #find if it exists
                        if chalExist:
                            chalStatus = chalExist
                        if chal.css(".disabled.ion-locked"):
                            chalStatus = "Locked"
                        result[certName][chapName][chalName] = OrderedDict()
                        result[certName][chapName][chalName]["_status"] = chalStatus
                        result[certName][chapName][chalName]["_link"] = chalLink
                        result[certName][chapName][chalName]["_dateC"] = ""
                        result[certName][chapName][chalName]["_dateU"] = ""
                        result[certName][chapName][chalName]["_desc"] = ""
                        result[certName][chapName][chalName]["_req"] = ""
                        result[certName][chapName][chalName]["_code"] = ""
                        lookup[chalName] = [certName,chapName]
        self.log("Loop End")
        self.log("Output: "+resultPath)
        self.log("Output: "+lookupPath)
        with open(resultPath, "w") as output:
            json.dump(result, output, indent=2)
        with open(lookupPath, "w") as output:
            json.dump(lookup, output, indent=2)


# str("%02d"%certIdx) + " " +

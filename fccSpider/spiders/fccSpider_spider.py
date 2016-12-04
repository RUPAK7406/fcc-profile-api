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


class fccExport(scrapy.Spider):

    # Init
    name = "export"
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
        super(fccExport, self).__init__(*args, **kwargs)
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

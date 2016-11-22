import scrapy
from collections import OrderedDict
import json
import os

class fccProfile(scrapy.Spider):
    name = "fccProfile"
    def __init__(self, username=None, *args, **kwargs):
        super(fccProfile, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]


    def parse(self, response):
        # Clear string function
        def clrstr(string):
           string = str(string).lstrip()
           if string == "None":
               string = ""
           return string
        # Start scraping
        with open(os.getcwd() + "/output/fccMap.json") as output:
            result = json.load(output, object_pairs_hook=OrderedDict)
        self.log("Loop Start")
        for table in response.css(".table-striped"):
            # tableName = table.css("th.col-xs-5::text").extract_first()
            # result[tableName] = []
            for challenge in table.css("tr"):
                name = challenge.css("td.col-xs-12.visible-xs a::text").extract_first()
                if name:
                    date = challenge.css("td.col-xs-2.hidden-xs::text").extract()
                    if len(date) == 1: # if date only contains `completed date`
                        date.append("") # append empty date
                    link = challenge.css("td.col-xs-12.visible-xs a::attr(href)").extract_first()
                    if "solution=" in link:
                        code = str(link).split("?",1)[1][9:]
                    else:
                        code = ""
                    entry = {
                        "Name": name,
                        "Date Completed": date[0],
                        "Date Updated": date[1],
                        "Link": link,
                        "Code": code,
                    }
                    result[tableName].append(entry)
        self.log("Loop End")


# re(r"(^.*)?\?")

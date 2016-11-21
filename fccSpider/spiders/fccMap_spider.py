import scrapy
from collections import OrderedDict
import json
import os

class fccMap(scrapy.Spider):
    name = "fccMap"
    def __init__(self, username=None, *args, **kwargs):
        super(fccMap, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.freecodecamp.com/map']


    def parse(self, response):
        result = OrderedDict()
        self.log('Loop Start')
        for table in response.css("#accordion"):
            # only one table, so no need to find titles. Skip a subsection for dictionary.
            for certIdx, cert in enumerate(table.css("div.certBlock")): #list certs in table and loop
                certName = table.css("h2 > a::text").extract()[certIdx] #find the title
                result[certName] = '' #set up empty dictionary under title
                result[certName] = OrderedDict() #set up empty dictionary under title
                for chapIdx, chap in enumerate(cert.css("div.chapterBlock")): #list chapters in cert and loop
                    chapName = cert.css("h3 > a::text").extract()[chapIdx] #find the title
                    result[certName][chapName] = OrderedDict() #set up empty dictionary under title
                    for chalIdx, chal in enumerate(chap.css("p.challenge-title")): #list challenges in chapters and loop
                        chalName = str(chal.css("a span::text").extract_first()).lstrip() #find the title
                        chalName2 = str(chal.css("a::text").extract_first()).lstrip() #find the title
                        chalLink = chal.css("a::attr(href)").extract_first() #find the link
                        chalStatus = str(chal.css("a span.sr-only::text").extract_first()).lstrip() #find the status
                        if chalName == chalStatus:
                            chalName = chalName2
                        result[certName][chapName][chalName] = {
                            'link': chalLink,
                            'status': chalStatus,
                        }
        self.log('Loop End')
        path = os.getcwd() + "/output/fccMap.json"
        self.log('Output: '+path)
        with open(path, 'w') as output:
            json.dump(result, output, indent=2)


# str("%02d"%certIdx) + " " +

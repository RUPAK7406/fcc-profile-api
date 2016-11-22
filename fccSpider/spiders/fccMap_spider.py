import scrapy
from collections import OrderedDict
import json
import os

class fccMap(scrapy.Spider):
    name = "fccMap"
    def __init__(self, username=None, *args, **kwargs):
        super(fccMap, self).__init__(*args, **kwargs)
        self.start_urls = ['http://local.htko.ca/map.html']


    def parse(self, response):
        result = OrderedDict()
        self.log('Loop Start')
        for table in response.css("#accordion"):
            # only one table, so no need to find titles. Skip a subsection for dictionary.
            for certIdx, cert in enumerate(table.css("div.certBlock")): #list certs in table and loop
                certName = table.css("h2 > a::text").extract()[certIdx] #find the title
                result[certName] = OrderedDict() #set up empty dictionary under title
                for chapIdx, chap in enumerate(cert.css("div.chapterBlock")): #list chapters in cert and loop
                    chapName = cert.css("h3 > a::text").extract()[chapIdx] #find the title
                    chapTime = cert.css("h3 > .challengeBlockTime::text").extract()[chapIdx] #find the title
                    result[certName][chapName] = OrderedDict() #set up empty dictionary under title
                    result[certName][chapName]["_time"] = chapTime[1:-1]
                    for chalIdx, chal in enumerate(chap.css("p.challenge-title")): #list challenges in chapters and loop
                        chalName = chal.css("::text").extract_first()
                        chalLink = chal.css("a::attr(href)").extract_first() #find the link
                        chalStatus = chal.css("a span.sr-only::text").extract_first() #find the status
                        chalExist = chal.css("em::text").extract_first() #find if it exists
                        if chalExist:
                            chalStatus = chalExist
                        if chal.css('.disabled.ion-locked'):
                            chalStatus = "Locked"
                        if not chalLink:
                            chalLink = ""
                        chalName = str(chalName).lstrip() #find the title
                        chalStatus = str(chalStatus).lstrip() #find the status
                        chalLink = str(chalLink).lstrip()
                        result[certName][chapName][chalName] = OrderedDict()
                        result[certName][chapName][chalName]["_status"] = chalStatus
                        result[certName][chapName][chalName]["_link"] = chalLink
                        result[certName][chapName][chalName]["_dateC"] = ''
                        result[certName][chapName][chalName]["_dateU"] = ''
                        result[certName][chapName][chalName]["_desc"] = ''
                        result[certName][chapName][chalName]["_req"] = ''
                        result[certName][chapName][chalName]["_code"] = ''
        self.log('Loop End')
        path = os.getcwd() + "/output/fccMap.json"
        self.log('Output: '+path)
        with open(path, 'w') as output:
            json.dump(result, output, indent=2)


# str("%02d"%certIdx) + " " +

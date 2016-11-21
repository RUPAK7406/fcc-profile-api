import scrapy
from collections import OrderedDict

class fccMap(scrapy.Spider):
    name = "fccMap"
    def __init__(self, username=None, *args, **kwargs):
        super(fccMap, self).__init__(*args, **kwargs)
        self.start_urls = ['http://local.htko.ca/map.html']


    def parse(self, response):
        result = {}
        for table in response.css("#accordion"):
            # only one table, so no need to find titles. Skip a subsection for dictionary.
            for certIdx, cert in enumerate(table.css("div.certBlock")): #list certs in table and loop
                certName = str("%02d"%certIdx) + " " + table.css("h2 > a::text").extract()[certIdx] #find the title
                result[certName] = {} #set up empty dictionary under title
                for chapIdx, chap in enumerate(cert.css("div.chapterBlock")): #list chapters in cert and loop
                    chapName = str("%02d"%chapIdx) + " " + cert.css("h3 > a::text").extract()[chapIdx] #find the title
                    result[certName][chapName] = {} #set up empty dictionary under title
                    for chalIdx, chal in enumerate(chap.css("p.challenge-title")): #list challenges in chapters and loop
                        chalName = str("%02d"%chalIdx) + " " + str(chal.css("a span::text").extract_first()) #find the title
                        chalLink = chal.css("a::attr(href)").extract_first() #find the link
                        chalStatus = chal.css("a span.sr-only::text").extract_first() #find the status
                        result[certName][chapName][chalName] = {
                            'link': chalLink,
                            'status': chalStatus,
                        }
        return result

# str("%02d"%certIdx) + " " +

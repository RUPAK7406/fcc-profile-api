import scrapy
import urlparse

class fccSpider(scrapy.Spider):
    name = "fccSpider"
    def __init__(self, username=None, *args, **kwargs):
        super(fccSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.freecodecamp.com/%s' % username]


    def parse(self, response):
        self.log('Loop Start')
        result = {}
        for table in response.css(".table-striped"):
            tableName = table.css("th.col-xs-5::text").extract_first()
            result[tableName] = []
            for challenge in table.css("tr"):
                name = challenge.css("td.col-xs-12.visible-xs a::text").extract_first()
                if name:
                    date = challenge.css("td.col-xs-2.hidden-xs::text").extract()
                    dateLen = len(date)
                    if dateLen == 1:
                        date.append("None")
                    data = challenge.css("td.col-xs-12.visible-xs a::attr(href)").extract_first()
                    if "/challenges/" in data:
                        dataSplit = str(data).split("?",1)
                        link = "https://www.freecodecamp.com" + dataSplit[0]
                        if "solution=" in data:
                            code = dataSplit[1][9:]
                        else:
                            code = None
                    else:
                        link = data
                        code = None
                    entry = {
                        'Name': name,
                        'Date Completed': date[0],
                        'Date Updated': date[1],
                        'Link': link,
                        'Code': code,
                    }
                    result[tableName].append(entry)
        self.log('Loop End')
        return result

# re(r'(^.*)?\?')

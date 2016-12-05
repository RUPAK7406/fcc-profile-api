import scrapy
from collections import OrderedDict
import json
import os
from string import Template

class fccExport(scrapy.Spider):

    # Init
    name = "export"
    # Setup Folder Paths
    curDir = os.getcwd()
    commonDir = curDir + "/common"
    exportDir = curDir + "/export"
    # Setup File Paths
    resultPath = commonDir + "/result.json"
    failedPath = commonDir + "/failed.json"
    nameDictPath = commonDir + "/nameDict.json"
    linkDictPath = commonDir + "/linkDict.json"
    templatePath = commonDir + "/template.md"
    # Setup Dictionaries
    result = OrderedDict()
    failed = OrderedDict()
    nameDict = OrderedDict()
    linkDict = OrderedDict()
    templateFile = None

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccExport, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.resultPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        self.templateFile = Template( open(self.templatePath).read() )
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)

    def clrstr(self, string):
        # Clear String Function
        string = str(string).strip()
        if string == "None":
            string = ""
        return string

    def parse(self, response):
        # Start Export
        certIndex = 0
        for certName, cert in self.result.items():
            # Setup Path
            certDir = "/" + str(certIndex).zfill(2) + " - " + certName
            certPath = self.exportDir + certDir
            certIndex = certIndex + 1
            chapIndex = 0
            # Make Path
            try:
                os.stat(certPath)
            except:
                os.mkdir(certPath)
            for chapName, chap in cert.items():
                # Variables
                chapTime = self.result[certName][chapName]["_time"]
                chapDesc = self.result[certName][chapName]["_desc"]
                # Setup Path
                chapDir = "/" + str(chapIndex).zfill(2) + " - " + chapName + " (" + chapTime + ")"
                chapPath = certPath + chapDir
                chapIndex = chapIndex + 1
                chalIndex = 0
                # Make Path
                try:
                    os.stat(chapPath)
                except:
                    os.mkdir(chapPath)
                for chalName, chal in chap.items():
                    if not chalName[0] == "_":
                        # Variables
                        chalData = {
                            "chapDesc": chapDesc,
                            "chalIndex": chalIndex,
                            "chalName": chalName,
                            "chalStatus": self.result[certName][chapName][chalName]["_status"],
                            "chalDateC": self.result[certName][chapName][chalName]["_dateC"],
                            "chalDateU": self.result[certName][chapName][chalName]["_dateU"],
                            "chalDesc": self.result[certName][chapName][chalName]["_desc"],
                            "chalCode": self.result[certName][chapName][chalName]["_code"],
                        }
                        # Substitute Data
                        chalTemplate = str( self.templateFile.safe_substitute(chalData) )
                        # Setup Path
                        chalFile = "/" + str(chalIndex).zfill(2) + " - " + chalName + ".md"
                        chalPath = chapPath + chalFile
                        chalIndex = chalIndex + 1
                        # Make Path
                        with open(chalPath, "w") as output:
                            output.write( chalTemplate )

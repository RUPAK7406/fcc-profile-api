import scrapy
from collections import OrderedDict
import json
import os
from string import Template
from urllib import parse

class fccExport(scrapy.Spider):

    # Init
    name = "export"
    # Setup Folder Paths
    curDir = os.getcwd()
    commonDir = curDir + "/common"
    templateDir = curDir + "/template"
    exportDir = curDir + "/export"
    # Setup File Paths
    resultPath = commonDir + "/result.json"
    nameDictPath = commonDir + "/nameDict.json"
    linkDictPath = commonDir + "/linkDict.json"
    # Setup Export
    exportPath = exportDir + "/result.json"
    readmePath = templateDir + "/readme.md"
    chapterPath = templateDir + "/chapter.md"
    challengePath = templateDir + "/challenge.md"
    # Setup Dictionaries
    result = OrderedDict()
    nameDict = OrderedDict()
    linkDict = OrderedDict()
    templateFile = None

    def __init__(self, username=None, *args, **kwargs):
        # Init
        super(fccExport, self).__init__(*args, **kwargs)
        # Load Files
        with open(self.resultPath) as output:
            self.result = json.load(output, object_pairs_hook=OrderedDict)
        self.readmeFile = Template( open(self.readmePath).read() )
        self.chapterFile = Template( open(self.chapterPath).read() )
        self.challengeFile = Template( open(self.challengePath).read() )
        # Setup URLs
        self.start_urls = ["https://www.freecodecamp.com/%s" % username]

    def closed(self, reason):
        # Init
        self.log("Stop Reason: " + reason)
        # Save Files
        with open(self.exportPath, "w") as output:
            self.log("Output: " + self.exportPath)
            json.dump(self.result, output, indent=2)

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
                chapData = {
                    "chapIndex": chapIndex,
                    "chapName": chapName,
                    "chapTime": chapTime,
                    "chapDesc": chapDesc,
                }
                # Substitute Data
                chapTemplate = str( self.chapterFile.safe_substitute(chapData) )
                # Setup Path
                chapDir = "/" + str(chapIndex).zfill(2) + " - " + chapName + " (" + chapTime + ")"
                chapPath = certPath + chapDir
                chapFile = "/readme.md"
                chapFilePath = chapPath + chapFile
                chapIndex = chapIndex + 1
                chalIndex = 0
                # Make Path
                try:
                    os.stat(chapPath)
                except:
                    os.mkdir(chapPath)
                with open(chapFilePath, "w") as output:
                    self.log("Output: " + chapFilePath)
                    output.write( chapTemplate )
                for chalName, chal in chap.items():
                    if not chalName[0] == "_":
                        # Variables
                        chalCode = self.result[certName][chapName][chalName]["_code"]
                        if self.result[certName][chapName][chalName]["_codeType"] == "code":
                            chalCode = parse.unquote( chalCode )
                        chalData = {
                            "chalIndex": chalIndex,
                            "chalName": chalName,
                            "chalStatus": self.result[certName][chapName][chalName]["_status"],
                            "chalDateC": self.result[certName][chapName][chalName]["_dateC"],
                            "chalDateU": self.result[certName][chapName][chalName]["_dateU"],
                            "chalDesc": self.result[certName][chapName][chalName]["_desc"],
                            "chalCode": chalCode,
                        }
                        # Substitute Data
                        chalTemplate = str( self.challengeFile.safe_substitute(chalData) )
                        # Setup Path
                        chalFile = "/" + str(chalIndex).zfill(2) + " - " + chalName + ".md"
                        chalFilePath = chapPath + chalFile
                        chalIndex = chalIndex + 1
                        # Make Path
                        with open(chalFilePath, "w") as output:
                            self.log("Output: " + chalFilePath)
                            output.write( chalTemplate )
                        with open(chapFilePath, "a") as output:
                            self.log("Append: " + chapFilePath)
                            output.write( chalTemplate )

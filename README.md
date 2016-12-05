# FCC Spider
Built on [Scrapy](https://scrapy.org/) & [Python](https://www.python.org/), this tool converts your Free Code Camp challenge profile into JSON data

## Install
* These bash scripts are mostly designed to run in a Linux environment, specifically Python 3 container in Docker 1.10+ running on Ubuntu 16.04.1. Scrapy is yet to support Python 3 in Windows as of today.
* Install Python 3, Scrapy's dependencies and Scrapy itself.
```
apt-get update
apt-get install python-pip
apt-get install build-essential libssl-dev libffi-dev python-dev
pip install cryptography
pip install Scrapy
```
* Extract [latest version](https://github.com/htko89/FCC-Spider/releases) into a directory, say `~/fccSpider`, and enter it.
* Set executable permissions:
```
cd ~/fccSpider
chmod 755 -R ~/fccSpider
```
* `~/fccSpider` should contain:
```
/fccSpider
/common
/export
fccSpider.sh
scrapy.cfg
readme.md
```

## Usage / Changelog

### 0.3
* Usage:
```
+ Application Comments:
+ Usage   : ./fccSpider.sh [username] [action]
+ Example : ./fccSpider.sh htko89 full
+ Actions : See below.
++ full : Downloads the FCC curriculum map, challenge descriptions, personal completion profile, export results
++ scrape : Downloads the FCC curriculum map, challenge descriptions, personal completion profile
++ empty  : Downloads the FCC curriculum map, challenge descriptions.
++ export : Exports existing results to export folder. Scrape must have run at least once before or errors will occur
```
* Working data output to `/common`. Export data output to `/export`.
* Challenge solution code in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

### 0.2
* Usage:
```
cd ~/fccSpider
./fccSpider.sh [username]
Example: ./fccSpider.sh myfccusername
```
* Data output to `map.json` and `map.failed.json` in `~/fccSpider/output/`. Make sure files in this folder are backed up, as they are wiped per execution.
* Challenge solution code in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

### 0.1
* Usage:
```
cd ~/fccSpider
./fccSpider.sh [username] [spiderName]
Example: ./fccSpider.sh myfccusername fccProfile
```
* Available spiders:
```
fccProfile, fccMap (WIP)
```
* Data output to `[spiderName].json` in `~/fccSpider/output/`.
* Challenge solutions code in URL encoding.

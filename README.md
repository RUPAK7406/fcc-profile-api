# FCC Spider
Built on [Scrapy](https://scrapy.org/) & [Python](https://www.python.org/), this tool converts your Free Code Camp challenge profile into JSON data

## Install
* These bash scripts are mostly designed to run in a Linux environment, specifically Python 3 container in Docker 1.10+ running on Ubuntu 16.04.1. Scrapy is yet to support Python 3 in Windows as of today.
* Install Python 3
```
apt-get update
apt-get install python-pip
```
* Install Scrapy
```
pip install Scrapy
```
* Extract [latest version](https://github.com/htko89/FCC-Spider/releases) into a directory, say `~/fccSpider`, and enter it.
```
cd ~/fccSpider
```
* Set executable permissions:
```
chmod 755 -R ~/fccSpider
```
* `~/fccSpider` should contain `fccSpider`, `output` folders and `fccSpider.sh`, `scrapy.cfg` files.

## Usage / Changelog

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

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
pip install scrapy
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

### 0.4
* Usage:
```
+ Application Comments:
+  Usage    : ./fccSpider.sh [username] [action]
+  Example  : ./fccSpider.sh htko89 full
+  Actions  : See below.
++  full    - Download FCC curriculum map & challenge descriptions, personal profile, export results
++  map     - Download FCC curriculum map & challenge descriptions.
++  profile - Download & export personal profile. Map must be downloaded or error will error.
++  empty   - Download & export empty profile. Map must be downloaded or error will error.
++  clear   - Deletes all maps and exports.
```
* Working data output to `/common`. Export data output to `/export`.
* Challenge solution code in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

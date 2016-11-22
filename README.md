# FCC Spider
Built on [Scrapy](https://scrapy.org/) & [Python](https://www.python.org/), this tool converts your Free Code Camp challenge profile, or general map structure into JSON data.

## Install
* There are bash scripts in this project, hence it requires linux. You can use it without linux by learning how it works in `fccSpider.sh`.
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
chmod ~/fccSpider 755 -R .
```
* `~/fccSpider` should contain `fccSpider`, `output` folders and `fccSpider.sh`, `scrapy.cfg` files.

## Usage / Changelog

* In `~/fccSpider`:
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

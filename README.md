# FCC Spider
Built on [Scrapy](https://scrapy.org/) & [Python](https://www.python.org/), this tool converts your Free Code Camp challenge profile into JSON data.

## Install
* There are bash scripts in this project, hence it requires linux. You can use it without linux by learning how it works in `fccSpider.sh`.
* Install Python 2
```
apt-get update
apt-get install python-pip
```
* Install Scrapy
```
pip install Scrapy
```
* Download this repository into a directory, say `~/fccSpider`, and enter it.
```
cd ~/fccSpider
```
* `~/fccSpider` should contain `fccSpider.sh`, a `fccSpider` folder and a `output` folder.

## Application Usage:
* In `~/fccSpider`:
```
./fccSpider.sh [username] [spiderName]"
Example: ./fccSpider.sh myfccusername fccProfile"
```
* Currently available spiders:
```
fccProfile, fccMap (WIP)
```
* Your data will be appended to `[spiderName].json` in `~/fccSpider/output/`. Your challenge solutions are in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

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
* Download this repository into a directory, say `~/fccSpider`, and enter it.
```
cd ~/fccSpider
```
* `~/fccSpider` should contain `fccSpider.sh`, `scrapy.cfg`, `fccSpider` folder, and an `output` folder.

## Application Usage:
* In `~/fccSpider`:
```
./fccSpider.sh [username]
Example: ./fccSpider.sh myfccusername
```
* Your data will be output to `map.json` and `map.failed.json` in `~/fccSpider/output/`. Make sure files in this folder are backed up, as they are wiped per execution. 
* Your challenge solutions are in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

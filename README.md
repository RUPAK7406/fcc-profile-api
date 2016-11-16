# FCC Spider
Built on [Scrapy](https://scrapy.org/) & [Python](https://www.python.org/), this tool converts your Free Code Camp challenge profile into JSON data.

## Usage
* Install Python
* Install Scrapy
```
pip install Scrapy
```
* Download this repository into a directory, say `~/fccSpider`, and enter it.
```
cd ~/fccSpider
```
* Run this tool, replacing `USER` with your Free Code Camp username.
```
scrapy crawl fccSpider -o items.json -t json -a username=USER
```
* Your data will be appended to `items.json` in `~/fccSpider`, with your challenge solution in URL encoding. Decoder: [Here](http://meyerweb.com/eric/tools/dencoder/).

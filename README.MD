# Amazon Image Scraper
## Installation Guide
This scraper is implemented on Scrapy framework. Please follow the steps below to config your environment before running the spider. You can skip certain steps if you already have it installed.

### Package Version
- Python 3.7.2
- Scrapy 1.5.1
- Docker 18.06
- scrapy-splash 0.7.2

### Install virtualenv and python 3.7
If you have not installed python virtual environment, install and create a virtual enviroment with python 3.7.
```
pip install virtualenv 
virtualenv -p python3 [env name]
source /path/to/env
```

### Install Scrapy
Scrapy is an application framework for crawling web sites and extracting structured data. Our scraper is implemented on scrapy. Following instructions help you install scrapy to your python environment.
```
pip install Scrapy
```

### Install Docker and spin up Splash backend
#### Docker
Splash can execute custom rendering scripts written in the Lua programming language. This allows us to use Splash as a browser automation tool. To set up Splash and let it run in the backend, we need to install Docker container first.

On Ubuntu system, type the following command:
```
sudo apt install docker.io
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash
```
Now you should have set up a Splash docker container running in the backend. Type `localhost:8050` in your browser to see if you have successfully started Splash service.

#### Scrapy-splash
Scrapy-splash is a useful library that integrates Splash into Scrapy. Install Scrapy-splash is simple:
```
pip install scrapy-splash
```

### Install scrapy-fake-useragent
To avoid being detected as a bot, we should switch `user-agent` while scraping. **scrapy-fake-useragent** is a random User-Agent middleware based on fake-useragent. It picks up User-Agent strings based on usage statistics from a real world database.
```
pip install scrapy-fake-useragent
```
See [this page](https://github.com/alecxe/scrapy-fake-useragent) for further details on this library.

### (Optional) Install scrapy-proxies
As Amazon is good at detecting bots, having multiple proxies do the scraping job can alleviate this issue. To config multi-proxy, install `scrapy-proxies` first:
```
pip install scrapy_proxies
```
Then prepare your proxy list following the instructions from [here](https://github.com/aivarsk/scrapy-proxies). To enable mutil-proxy, set `ENABLE_PROXY` entry in `user_config.py` file to `True`.

## Usage
After configuring the enviroment, you are ready to scrape image data from Amazon! The following steps teach you how to run the spider.

**Please make sure you are in the root directory.**

### Configure user setting
Edit `user_settings.py` file under the root directory. Your can configure the following settings according to you needs:
- `KEY_WORDS`: A list of item key words to scrape.
- `MAX_DEPTH`: Max number of list pages to scrape for each key word.
- `DETAIL_IMG`: Whether you want to scrape detailed, high-quality images of the items. If set to `False`, the program will only scrape thumbnail of the items in list page (Instead of further scraping the detail page).
- `ENABLE_PROXY`: Whether you want to enable multi-proxy. Make sure you have add you proxy information to `proxy_list.txt` file.
   
_**Note:** Current release of scraper will usually fail in scraping images when `DETAIL_IMG` is set to `True`. Because the scraper is frequently detected by Amazon as bot and blocked. Future release will fix this problem._

### Run
Run scraper with `python runSpider.py` command.

### Output
When the scraper finishes its work, A file named `Output` will generate under root directory. A json file `Output/result.json` contains the structured information of all scraped items. All scraped images are download to `Output/full`.

## Release
**release v0.1 (11/30/2018 current release)**

This release contains the following feature items:
- Scrape list pages and detail pages of certain catagory.
- Fake user agent for anti bot-detection.







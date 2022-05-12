import os
from dotenv import load_dotenv
load_dotenv()
# Scrapy settings for moviePro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
# 引用自己的custom pipeline MovieproPipeline是pipelines class的名字

ITEM_PIPELINES = {
    'moviePro.pipelines.MovieProPipeline': 300
}

BOT_NAME = 'moviePro'

SPIDER_MODULES = ['moviePro.spiders']
NEWSPIDER_MODULE = 'moviePro.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
DOWNLOAD_DELAY = 2  # delay in downloading images
# IMAGES_STORE = r"C:\Users\User\PycharmProjects\movie3\moviePro\moviePro\spiders\image"

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# 我真不知道加上面那兩行有沒有用
# 下面那個路徑後的/img是我加的 檔名最後會變成img+num 因為不加他不跑
IMAGES_STORE = os.getenv('IMAGES_STORE')
# 丟S3
# 我有去S3 bucket policy改  "Action": [
#                 "s3:GetObject",
#                 "s3:PutObject"
#             ],

# IMAGES_STORE_S3_ACL = 'public-read'
# 根本不用加這行 不知道是在三小...

# IMAGES_STORE = 's3://AKIAXB56RUKLQBIS2V7O:azOFXBpPyhHsKj6Ike9O0PpU9djY8Td/pwSpDyyY@bucket-for-dinners-project'
# s3://aws_key:aws_secret@mybucket/path/to/export.csv
# s3://mybucket/path/to/export.csv

# folder name or path where to save images



# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'moviePro (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.8,de-de;q=0.5,de;q=0.3',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'moviePro.middlewares.MovieproSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'moviePro.middlewares.MovieproDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'moviePro.pipelines.MovieproPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
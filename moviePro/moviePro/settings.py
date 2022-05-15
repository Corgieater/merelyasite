import os
from dotenv import load_dotenv
load_dotenv()

ITEM_PIPELINES = {
    'moviePro.pipelines.MovieProPipeline': 300
}

BOT_NAME = 'moviePro'

SPIDER_MODULES = ['moviePro.spiders']
NEWSPIDER_MODULE = 'moviePro.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
DOWNLOAD_DELAY = 2

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

IMAGES_STORE = os.getenv('BUCKET')

ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.8,de-de;q=0.5,de;q=0.3',
}

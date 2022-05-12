# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieproItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    imdb_rating = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    genres = scrapy.Field()
    story_line = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()

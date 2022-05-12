# import scrapy
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
# from moviePro.dataImport import *

from itemadapter import ItemAdapter
import hashlib
from os.path import splitext
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from moviePro.dataImport import *

import mysql.connector
import os


# 看起來用default也會下載 那應該就是有沒有install Pillow的關係了
# 要記得裝botocore

database = Database()

# 照阿六的寫法全部改寫
# 引用原始的pipeline複寫


class MovieProPipeline(ImagesPipeline):
    # 不知道為啥這個打開會讓下面code都沒辦法出來，所以我就先關掉，把這個丟到處理img的那邊去
    # def process_item(self, item, spider):
    #     title = item['title']
    #     year = item['year']
    #     directors = item['directors']
    #     directors = ",".join(directors)
    #     stars = item['stars']
    #     stars = ",".join(stars)
    #     genres = item['genres']
    #     genres = ",".join(genres)
    #     story_line = item['story_line']
    #
    #     movie_data = (None, title, year, directors,
    #                   stars, genres, story_line, None)
    #     database.add_to_database(movie_data)
    #
    #     return item

    def get_media_requests(self, item, info):
        title = item['title']
        year = item['year']
        directors = item['directors']
        directors = ",".join(directors)
        stars = item['stars']
        stars = ",".join(stars)
        genres = item['genres']
        genres = ",".join(genres)
        story_line = item['story_line']

        movie_data = (None, title, year, directors,
                      stars, genres, story_line, None)
        database.add_to_database(movie_data)
        image_url = item['image_urls']
        # yield的時候如果image_url不加0會一直叫說我給他list
        # meta用來抓item我建的name然後轉成str不然內部功能也會一直叫叫叫
        print('img_url\n', image_url)
        yield scrapy.Request(image_url[0], meta={'name': str(item['image_name'])})
        return item

    def item_completed(self, results, item, info):
        # 這段完全照抄
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no img")
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        # 要meta然後在filename+.jpg就可以改名了
        name = request.meta['name']
        filename = name+'.jpg'
        print('++++\n', name, filename)
        return filename


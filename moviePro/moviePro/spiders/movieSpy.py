import scrapy
from moviePro.items import MovieproItem
# this fucker works????
from bs4 import BeautifulSoup

id = 1


class MoviePro(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ['https://www.imdb.com/chart/top']

    def parse(self, response):
        item = MovieproItem()
        # good for all
        for href in response.css("td.titleColumn a::attr(href)").getall():
            yield response.follow(url=href, callback=self.parse_movie)

        # test for 2
        # for i in range(2):
        #     yield response.follow(url=response.css("td.titleColumn a::attr(href)").getall()[i],
        #                           callback=self.parse_movie)


        # soup = BeautifulSoup(response.text, 'html.parser')
        #
        #
        # movie = soup.select('tbody.lister-list tr td.titleColumn')[0]
        # href = response.urljoin(movie.select_one('a').get('href'))

        # this one
        # href = response.css("td.titleColumn a::attr(href)").get()
        # yield response.follow(url=href, callback=self.parse_movie)


    def parse_movie(self, response):
        global id
        item = MovieproItem()
        soup = BeautifulSoup(response.text, 'html.parser')

        item['title'] = soup.find('h1').text.strip()
        item['year'] = soup.find('span', 'sc-8c396aa2-2 itZqyK').text
        item['directors'] = []
        item['stars'] = []
        item['genres'] = []
        item['image_name'] = id
        item['story_line'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/'
                                   'section/div[3]/div[2]/div[1]/div[1]/p/span[3]/text()').extract()[0]


        for a in response.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/'
                                'div[1]/section[4]/ul/li[1]/div/ul/li/a'):
            item['directors'].append(a.xpath('text()').extract()[0])

        for a in response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/'
                               'div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a'):
            item['stars'].append(a.xpath('text()').extract()[0])

        for a in response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/'
                                'div[3]/div[2]/div[1]/div[1]/div/a'):
            item['genres'].append(a.xpath('ul/li/text()').get())
        print(item['genres'])


        poster_url = response.xpath('//*[@id="__next"]/main/div/section[1]/'
                                    'section/div[3]/section/section/div[3]/div[1]/div/div[1]/div/a/@href').get()
        clean_url = 'https://www.imdb.com'+poster_url
        print('-------------\n', clean_url)
        yield response.follow(url=clean_url, callback=self.parse_poster, meta={'item': item})
        id += 1
        print(item)
        return item

    def parse_poster(self, response):
        item = response.meta['item']
        poster_url = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[4]/img/@src').get()
        # print('aaaaaaaaaaaaaaaaa\n', poster_url)
        item['image_urls'] = [poster_url]
        # print('wewewweewewwe\n', item['image_urls'])

        yield item
        # yield {
        #     'image_urls' : url_list
        # }

import scrapy
from tiki.items import BookItem, PhoneItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.contrib.spiders import Rule


mc = lambda x: 'https://tiki.vn' + x


class TikiSpider(scrapy.Spider):
    name = 'tiki'
    start_urls = ['https://tiki.vn']

    def parse(self, response):
        paginate_urls = response.xpath('//ul/li/a/@href').extract()

        print(paginate_urls,'____________day la paginate_urls_________________________')
        if paginate_urls:
            for url in paginate_urls:
                if '/' in url:
                    print(url)
                    yield scrapy.Request(url=url.strip(), callback=self.parse_category)

    def parse_category(self, response):
        categories = response.xpath('//*[@class="list-group-item is-child"]/a/@href').extract()
        print(categories,'_____________________categories____________________________')
        if categories:
            for url in categories:
                if '/' in url:
                    print(url)
                    yield scrapy.Request(url=mc(url).strip(), callback=self.parse_item)

    # def parse_item(self, response):
        # product_urls = response.xpath('//*[@class="next"]/@href').extract()

    def parse_item(self, response):
        paginate_urls1 = response.xpath('//*[@class="next"]/@href').extract()
        if paginate_urls1:
            for url in paginate_urls1:
                if '/' in url:
                    print(mc(url), '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    yield scrapy.Request(url=mc(url).strip())




            book_urls = response.xpath('//*[@class="product-item    "]/a/@href').extract()
            for url in book_urls:
                if '/' in url:
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        l = ItemLoader(BookItem(), response)
        l.add_xpath('name', '//*[@itemprop="name"]/text()', MapCompose(str.strip), TakeFirst())

        return l.load_item()



#         # for url in product_urls:
#             yield scrapy.Request(url=mc(next_href.strip()), callback=self.parse_detail)
#
    # def parse_detail(self, response):
    #     # import pdb; pdb.set_trace()
    #     product_item= response.xpath('//*[@class="product-item    "]/a/@href').extract()
    #     # for url in product_item:
    #         # yield scrapy.Request(url)

# class TikiSpider(scrapy.Spider):
#     name = 'tiki'
#     start_urls = ['https://tiki.vn/sach-van-hoc/c839?order=newest']
#
#     def parse(self, response):
#         paginate_urls = response.xpath('//*[@class="next"]/@href').extract()
#         print(paginate_urls,"################################################################################")
#         # import pdb;pdb.set_trace()
#         for url in paginate_urls:
#             yield scrapy.Request(url=mc(url))
#
#         book_urls = response.xpath('//*[@class="product-item    "]/a/@href').extract()
#         for url in book_urls:
#             yield scrapy.Request(url, callback=self.parse_item)
#
#     def parse_item(self, response):
#         l = ItemLoader(BookItem(), response )
#         l.add_xpath('name', '//*[@itemprop="name"]/text()', MapCompose(str.strip), TakeFirst())
#
#         return l.load_item()














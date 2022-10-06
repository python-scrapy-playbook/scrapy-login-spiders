
from http import cookies
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest


class BasicLoginSpider(Spider):
    name = 'basic_login_spider'

    def start_requests(self):
        login_url = 'http://quotes.toscrape.com/login'
        yield scrapy.Request(login_url, callback=self.login)

    
    def login(self, response):
        token = response.css("form input[name=csrf_token]::attr(value)").extract_first()
        yield FormRequest.from_response(response,
                                         formdata={'csrf_token': token,
                                                   'password': 'foobar',
                                                   'username': 'foobar'},
                                         callback=self.start_scraping)


    def start_scraping(self, response):
        for quote in response.css('div.quote'):
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall(),
                }


               




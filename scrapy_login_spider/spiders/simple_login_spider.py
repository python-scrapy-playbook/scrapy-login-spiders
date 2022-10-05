
from scrapy import Spider
from scrapy.http import FormRequest


class SimpleLoginSpider(Spider):
    name = 'simple_login'

    def start_requests(self):
        login_url = 'http://example.com/login'
        yield FormRequest(login_url,
                            formdata={'email': 'example@gmail.com', 'password': 'foobar'},
                            callback=self.start_scraping)

    def start_scraping(self, response):
        ## Insert code to start scraping pages once logged in
        pass
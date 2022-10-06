import scrapy
from scrapy_splash import SplashRequest 
import base64

lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(1))

    splash:set_viewport_full()

    local email_input = splash:select('input[name=email]')   
    email_input:send_text("YOUR_EMAIL_HERE")
    assert(splash:wait(1))

    local email_submit = splash:select('input[id=continue]')
    email_submit:click()
    assert(splash:wait(3))

    local password_input = splash:select('input[name=password]')   
    password_input:send_text("YOUR_PASSWORD_HERE")
    assert(splash:wait(1))

    local password_submit = splash:select('input[id=signInSubmit]')
    password_submit:click()
    assert(splash:wait(3))

    return {
        html=splash:html(),
        url = splash:url(),
        png = splash:png(),
        cookies = splash:get_cookies(),
        }
    end
"""


class HeadlessBrowserLoginSpider(scrapy.Spider):
    name = "amazon_login"

    def start_requests(self):
        signin_url = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&'
        yield SplashRequest(
            url=signin_url, 
            callback=self.start_scrapping,
            endpoint='execute', 
            args={
                'width': 1000,
                'lua_source': lua_script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
                },
            )
    
    def start_scrapping(self,response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'after_login.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        url_list = ['https://www.amazon.com/']
        for url in url_list:
            yield scrapy.Request(url=url, cookies=cookies_dict, callback=self.parse)

    def parse(self, response):
        # save the full page html
        with open('response.html', 'wb') as f:
            f.write(response.body)

        # scraping all the links on the page
        page_urls = response.css('a')
        for page_url in page_urls:
            if(page_url.css('a::text').get() is not None):
                try:
                    yield {
                        'url_text' : page_url.css('a::text').get(),
                        'url' : page_url.css('a').attrib['href']
                    }
                except:
                    print("An error occurred when scraping a link")


    
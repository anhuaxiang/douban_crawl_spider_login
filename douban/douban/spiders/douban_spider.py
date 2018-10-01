# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from douban.items import DoubanItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import urllib
import urllib.request
from PIL import Image


class DoubanSpiderSpider(CrawlSpider):
    name = 'douban_spider'
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com/top250']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

    rules = (
        Rule(LinkExtractor(allow='start=[\d]{2}&filter='), follow=True),
        Rule(LinkExtractor(allow='subject/\d+'), callback='parse_item')
    )

    def start_requests(self):
        """
        重写start_request,请求登录页面
        :return:
        """
        return [scrapy.FormRequest("https://accounts.douban.com/login", headers=self.headers, meta={"cookiejar": 1},
                                   callback=self.parse_before_login)]

    def parse_before_login(self, response):
        print('登录填写表单')
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        if captcha_image_url is None:
            print('此次登录不需要验证码')
            form_data = {
                "source": "index_nav",
                "form_email": "18301605620",
                "form_password": "10011900aaa",
            }
        else:
            print('此次登录需要验证码')
            save_image_path = 'cap.jpeg'
            urllib.request.urlretrieve(captcha_image_url, save_image_path)
            try:
                im = Image.open(save_image_path)
                im.show()
            except:
                pass

            captcha_solution = input('输入图片中的验证码')
            form_data = {
                "source": "None",
                "redir": "https://www.douban.com",
                "form_email": "18301605620",
                "form_password": "10011900aaa",
                "captcha-solution": captcha_solution,
                "captcha-id": captcha_id,
                "login": "登录",
            }
        print("登陆中......")
        return scrapy.FormRequest.from_response(response,
                                                meta={"cookiejar": response.meta["cookiejar"]},
                                                headers=self.headers, formdata=form_data,
                                                callback=self.parse_after_login)

    def parse_after_login(self, response):
        """
        验证登录是否成功,通过make_requests_from_url对接crawlspider
        :param response:
        :return:
        """
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
            for url in self.start_urls:
                yield self.make_requests_from_url(url)

    def parse_item(self, response):
        item = DoubanItem()
        content = Selector(response)
        item['rank'] = content.xpath('//div[@class="top250"]/span[@class="top250-no"]/text()').extract_first()
        item['title'] = content.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        item['star'] = content.xpath('//strong[@class="ll rating_num"]/text()').extract_first()
        yield item























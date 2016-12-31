# -*- coding: UTF-8 -*-

import scrapy
import getpass
from bscraper.items import ForumTable

class ForumSpider(scrapy.Spider):
    name = "b-forums"
    login_url = "https://intranet.utcv.edu.mx/login"
    allowed_domains = ["intranet.utcv.edu.mx"]
    forum_names = [
        'M5',
        'FSC IV Sep 14',
        'TIC Desarrollo de Aplicaciones II.',
        'TIC Ingeniería de SW I',
        'TIC Administración de BD ESC',
    ]
    forum_urls = [
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=37358",
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=34621",
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=22840",
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=33657",
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=32225",
        "https://intranet.utcv.edu.mx/mod/forum/view.php?id=32195",
    ]

    def start_requests(self):
        usr, pwd = self.loggin()
        return [scrapy.FormRequest(
                self.login_url,
                formdata = {'username': usr, 'password': pwd},
                callback = self.parse_link
            )]

    def loggin(self):
        username = str(input("username: "))
        password = getpass.getpass("password: ")
        return username, password

    def parse_link(self, response):
        for link in self.forum_urls:
            yield scrapy.Request(link, callback=self.parse_item)

    def parse_item(self, response):
        table = ForumTable()
        forum_name = ""
        for name in self.forum_names:
            if name in response.body:
                forum_name = name
        table['name'] = forum_name.decode('unicode-escape')
        table['content'] = response.xpath('//table[@class="forumheaderlist"]').extract()
        return table
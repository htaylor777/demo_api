# -*- coding: utf-8 -*-
# pages increment by 12 as an offest on this site per subject
# API
import scrapy
from scrapy.exceptions import CloseSpider
import json


class EbooksSpider(scrapy.Spider):
    name = 'ebooks'
    allowed_domains = ['openlibrary.org']
    increment_by = 12
    offset = 0
    start_urls = [
        'https://openlibrary.org/subjects/picture_books.json?limit=12']

  # keep spider from running forever - when page status == 500 -> close it!
    def parse(self, response):
        if response.status == 500:
            raise CloseSpider(reason='Reached last page')

        resp = json.loads(response.body)
        ebooks = resp.get('works')
        for ebook in ebooks:
            yield {
                'Author': ebook.get('authors')[0].get('name'),
                'CanBorrow': ebook.get('availability'),
                'Subject': ebook.get('subject'),
                'Title': ebook.get('title'),

            }

        self.offset += self.increment_by
        yield scrapy.Request(
            url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
            callback=self.parse
        )
# added newline after

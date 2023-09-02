import scrapy
from ..items import FinancialtimeItem


class FinancialTime(scrapy.Spider):
    name = 'financial'
    start_urls = [
        'https://www.ft.com/green-bonds'
    ]

    def parse(self, response, **kwargs):

        items = FinancialtimeItem()

        divs = response.xpath('//div[@data-trackable="stream"]//li[.//div[@class="o-teaser__heading"]]')

        for each_div in divs:
            # Date
            try:
                date_posted = each_div.xpath('.//div[@class="stream-card__date"]//time/text()').extract_first()
            except AttributeError:
                date_posted = None

            image_url = None  # Set a default value

            # Image URL
            try:
                extracted_url = each_div.xpath('.//a[@data-trackable="image-link"]/@href').extract_first()
                if extracted_url:
                    image_url = 'https://www.ft.com' + extracted_url
            except AttributeError:
                pass  # Handle the error as needed

            # Is Special
            try:
                is_special = each_div.xpath('.//div[@class="o-teaser__meta"]//span/text()').extract_first()
                is_special = is_special == "Special Report"
            except AttributeError:
                is_special = False

            # Publisher
            try:
                published_by = each_div.xpath('.//div[@class="o-teaser__meta"]//a/text()').extract_first()
            except AttributeError:
                published_by = None

            # Title
            try:
                title = each_div.xpath('.//div[@class="o-teaser__heading"]').xpath('string()').extract_first()
            except AttributeError:
                title = None

            # Description
            try:
                description = each_div.xpath('.//a[@data-trackable="standfirst-link"]').xpath('string()').extract_first()
            except AttributeError:
                description = None

            items['date_posted'] = date_posted
            items['image_url'] = image_url
            items['is_special'] = is_special
            items['published_by'] = published_by
            items['title'] = title
            items['description'] = description

            yield items

        next_page_href = response.xpath('//a[@data-trackable="next-page"]/@href').get()

        if next_page_href is not None:
            next_page = 'https://www.ft.com/green-bonds' + next_page_href
            yield response.follow(next_page, callback=self.parse)

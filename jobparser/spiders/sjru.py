import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@class, 'dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)
        links = response.xpath("//span[contains(@class, ' _3DjcL _3sM6i')]//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[contains(@class, '_1piNv')]//text()").getall()
        salary = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)

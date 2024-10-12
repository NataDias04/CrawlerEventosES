import scrapy


class EventosVitoriaSpider(scrapy.Spider):
    name = "eventos_vitoria"
    allowed_domains = ["zig.tickets"]
    start_urls = ["https://zig.tickets"]

    def parse(self, response):
        pass

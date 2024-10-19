import scrapy
import json
import time

class EventosVitoriaSpider(scrapy.Spider):
    name = "eventos_vitoria"
    allowed_domains = ["zig.tickets", "agazeta.com.br", "lebillet.com.br"]
    start_urls = [
        "https://zig.tickets/?st=Esp%C3%ADrito%20Santo", 
        "https://www.agazeta.com.br/hz/agenda-cultural",
        "https://lebillet.com.br",
    ]

    def parse(self, response):
        pass

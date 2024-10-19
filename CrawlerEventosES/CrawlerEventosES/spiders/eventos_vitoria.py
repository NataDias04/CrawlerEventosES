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
        
        if "zig.tickets" in response.url:
            for evento in response.css('div.event-card'):  
                yield {
                    'titulo': evento.css('h3.event-title::text').get(),
                    'data': evento.css('span.event-date::text').get(),
                    'local': evento.css('span.event-location::text').get(),
                    'link': evento.css('a::attr(href)').get()
                }

        
        elif "agazeta.com.br" in response.url:
            for evento in response.css('div.event-card'): 
                yield {
                    'titulo': evento.css('h3.event-title::text').get(),
                    'data': evento.css('span.event-date::text').get(),
                    'local': evento.css('span.event-location::text').get(),
                    'link': evento.css('a::attr(href)').get()
                }
    

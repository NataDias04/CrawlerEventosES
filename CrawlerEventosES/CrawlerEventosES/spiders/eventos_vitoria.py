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
                    'titulo': evento.css('h2::text').get().strip(),
                    'data': evento.css('span.banner-date::text').get().strip(),
                    'local': response.css('span.banner-place::text').get().strip(),
                    'horario': response.css('span.banner-place::text').re_first(r'\d{2}:\d{2}').strip(),
                    'classificacao': response.css('span.banner-place i.fa-user + ::text').get().strip()
                }

        
        elif "agazeta.com.br" in response.url:
            for evento in response.css('div.event-card'): 
                yield {
                    'titulo': evento.css('h3.event-title::text').get(),
                    'data': evento.css('span.event-date::text').get(),
                    'local': evento.css('span.event-location::text').get(),
                    'link': evento.css('a::attr(href)').get()
                }
    
        elif "lebillet.com.br" in response.url:
            for evento in response.css('div.card-event'):  
                yield {
                    'titulo': evento.css('h2.card-title::text').get(),
                    'data': evento.css('span.card-date::text').get(),
                    'local': evento.css('span.card-location::text').get(),
                    'link': evento.css('a::attr(href)').get()
                }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def salvar_dados(dados):
    with open('eventos.json', 'a') as f:
        json.dump(dados, f)
        f.write('\n')


def executar_spider():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(EventosVitoriaSpider)
    process.start()

    

def agendar_execucoes(intervalo):
    while True:
        executar_spider()
        time.sleep(intervalo)


if __name__ == "__main__":
    agendar_execucoes(3600)

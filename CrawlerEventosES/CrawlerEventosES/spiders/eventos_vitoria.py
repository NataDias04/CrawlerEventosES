import scrapy
import json

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner


class EventosVitoriaSpider(scrapy.Spider):
    name = "eventos_vitoria"
    #allowed_domains = ["lebillet.com.br"] #"agazeta.com.br", "zig.tickets"

    start_urls = ["https://lebillet.com.br/"]

    

    def parse(self, response):

        dados = []
    
        if "lebillet.com.br" in response.url:
            for evento in response.css('div.show-card.big'):
                local_evento = evento.css('p.data-text.location::text').get(default='N/A')
        
                if verifica_locais(local_evento):
                    dados.append({
                        'titulo': evento.css('h3.title::text').get(default='N/A'),
                        'data': evento.css('p.data-text.datetime::text').get(default='N/A'),
                        'horario': evento.css('p.data-text.datetime::text').getall()[1] if len(evento.css('p.data-text.datetime::text').getall()) > 1 else 'N/A',
                        'local': local_evento,
                        'link': evento.css('a::attr(href)').get(default='N/A')
                    })

            next_page = response.css('a.next::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

            salvar_dados(dados)

locais = ["Vitória, ES", "Vila Velha, ES","A Definir ES, ES","Serra, ES", "Colatina, ES"]


def verifica_locais(local_evento):
    return local_evento in locais

def salvar_dados(dados, nome_arquivo='../eventos.json'):

    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:

        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def executar_spider():
    print("Iniciando execução da spider...")
    runner = CrawlerRunner()
    d = runner.crawl(EventosVitoriaSpider)
    d.addBoth(lambda _: print("Spider finalizada."))

def agendar_execucoes(intervalo):
    print(f"Agendando execução a cada 10 segundos...")
    tarefa = LoopingCall(executar_spider)
    tarefa.start(intervalo, now=True)
    reactor.run()


if __name__ == "__main__":
    agendar_execucoes(10)

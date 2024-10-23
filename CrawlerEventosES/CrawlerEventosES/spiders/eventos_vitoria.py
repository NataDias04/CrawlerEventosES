import scrapy
import json
import requests
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner

filaEventosProcessados = []
filaEventosPendentes = []

class EventosVitoriaSpider(scrapy.Spider):
    name = "eventos_vitoria"
    start_urls = [
        "https://lebillet.com.br/", 
        "https://www.agazeta.com.br/hz/agenda-cultural"
    ]

    def parse(self, response):
        eventos = []
        if "agazeta.com.br" in response.url:
            for evento in response.css('article.box.box--imagem'):
                titulo = evento.css('h2.titulo::text').get(default='N/A')
                eventos.append({'titulo': titulo})

        elif "lebillet.com.br" in response.url:
            for evento in response.css('div.show-card.big'):
                local_evento = evento.css('p.data-text.location::text').get(default='N/A')
                if verifica_locais(local_evento):
                    eventos.append({
                        'titulo': evento.css('h3.title::text').get(default='N/A'),
                        'data': evento.css('p.data-text.datetime::text').get(default='N/A'),
                        'horario': evento.css('p.data-text.datetime::text').getall()[1] 
                                   if len(evento.css('p.data-text.datetime::text').getall()) > 1 else 'N/A',
                        'local': local_evento,
                        'link': evento.css('a::attr(href)').get(default='N/A')
                    })

            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)

        filaEventosPendentes.extend(eventos)
        salva_eventos()

locais = ["Vitória, ES", "Vila Velha, ES", "A Definir ES, ES", "Serra, ES", "Colatina, ES"]

def verifica_locais(local_evento):
    return local_evento in locais

def salva_eventos(arquivo='../eventos.json'):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados_existentes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dados_existentes = []

    novos_eventos = [e for e in filaEventosPendentes if e not in dados_existentes]
    
    if novos_eventos:
        filaEventosProcessados.extend(novos_eventos)
        dados_existentes.extend(novos_eventos)

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_existentes, f, ensure_ascii=False, indent=4)

        print(f"{len(novos_eventos)} novos eventos salvos.")
    else:
        print("Nenhum evento novo para salvar.")

def executar_spider():
    print("Iniciando execução da spider...")
    runner = CrawlerRunner()
    d = runner.crawl(EventosVitoriaSpider)
    d.addBoth(lambda _: print("Spider finalizada."))

def agendar_execucoes(intervalo):
    print(f"Agendando execução a cada {intervalo} segundos...")
    tarefa = LoopingCall(executar_spider)
    tarefa.start(intervalo, now=True)
    reactor.run()

if __name__ == "__main__":
    agendar_execucoes(10)
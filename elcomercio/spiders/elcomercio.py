import scrapy
from w3lib.html import remove_tags, remove_tags_with_content
from ..items import NoticiaItem


class ElComercioSpider(scrapy.Spider):
    name = 'elcomercio'
    start_urls = [
        'http://elcomercio.pe/politica',
    ]

    def parse(self, response):
        links = response.xpath(
            '//div[contains(@class, "column-flows")]/div[contains(@class, "modules")]//a[contains(@class, "page-link")]/@href'
        ).extract()

        for link in links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_page
            )

    def parse_page(self, response):
        titulo = response.xpath('//h1/text()').extract_first(default='')
        descripcion = response.css('h2.news-summary ::text').extract_first()
        contenido = response.xpath('//div[contains(@class, "news-text-content")]').extract_first()
        contenido = remove_tags_with_content(contenido, which_ones=('script', ))
        contenido = remove_tags(contenido)

        foto = response.xpath('//div[contains(@class, "image_pri")]//img/@src').extract_first()

        item = NoticiaItem()
        item['titulo'] = titulo
        item['descripcion'] = descripcion
        item['url'] = response.url
        item['contenido'] = contenido
        item['foto'] = foto

        yield item

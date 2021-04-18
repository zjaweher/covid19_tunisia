# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.http import Request, FormRequest

class CasesByGovernorateSpider(scrapy.Spider):
    name = 'cases_by_governorate'
    allowed_domains = ['en.wikipedia.org/wiki/COVID-19_pandemic_in_Tunisia']
    start_urls = (
        'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Tunisia',
    )

    def parse(self, response):  
        history_page = response.xpath('//*[@class="collapsible"and @id="ca-history"]/a/@href').extract_first()+'&offset=&limit=250'
        absolute_history_page = response.urljoin(history_page)            
        yield Request(absolute_history_page, callback = self.parse_past_updates, dont_filter=True)

    def parse_past_updates(self, response):
    	past_updates_urls = response.xpath('//*[@data-mw-revid]/a/@href').extract()
    	for url in past_updates_urls:
    		url = response.urljoin(url)
    		yield Request(url, callback = self.parse_update, dont_filter=True)

    def parse_update(self, response):
    	if len(response.xpath('//*[contains(caption,"Cases")]')) != 0:
    		date = response.xpath('//*[@id="mw-revision-date"]/text()').extract_first()
    		for x in range(0,24):
    			governorate = response.xpath('//table[contains(caption,"Cases")]/tbody/tr/td/a/text()').extract()[x]
    			n_infected = response.xpath('//table[contains(caption,"Cases")]/tbody/tr/td/text()').extract()[4*x+1]
    			n_recovered = response.xpath('//table[contains(caption,"Cases")]/tbody/tr/td/text()').extract()[4*x+3]
    			n_dead = response.xpath('//table[contains(caption,"Cases")]/tbody/tr/td/text()').extract()[4*x+2]
    			yield {'date': date,
    			   'governorate': governorate.strip(),
    			   'n_infected': n_infected.strip(),
    			   'n_recovered': n_recovered.strip(),
    			   'n_dead': n_dead.strip()}

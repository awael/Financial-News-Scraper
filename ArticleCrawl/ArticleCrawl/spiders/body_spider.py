import scrapy


class BodySpider(scrapy.Spider):
    name = "body"

    #start_urls = ['https://almalnews.com/category/stocks/page/2']

    def start_requests(self):
        with open('links.csv') as f:
            for line in f:
                if not line.strip():
                    continue
                yield scrapy.Request(line)

    def parse(self, response):

        separator = " "
        #for full_page in response.css('div.entry-content'):
        full_page = response.css('div.entry-content')
        yield {
            'link': response.request.url,
            'body_text': separator.join(full_page.xpath('//div[@class = "entry-content"]/descendant::text()[not(ancestor::a)]').getall())
        }
        #next_page = response.css('div.custom-pagination a::attr(href)').getall()[-2]
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse)

# scrapy crawl articles -o articles.csv
#article_text = full_page.xpath('//div[@class = "entry-content"]/descendant::text()[not(ancestor::a)]').getall()
#full_page = response.css('div.entry-content')
#scrapy crawl body -s JOBDIR=crawls/body-2 -o texts.csv
#scrapy crawl body -s JOBDIR=crawls/body-5 -o texts_url.csv
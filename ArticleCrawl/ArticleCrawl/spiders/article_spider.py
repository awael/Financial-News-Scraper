import scrapy


class ArticleSpider(scrapy.Spider):
    name = "articles"

    start_urls = ['https://almalnews.com/category/stocks/page/2']

    def parse(self, response):
        self.settings.CONCURRENT_REQUESTS_PER_DOMAIN = 20
        article_section = response.xpath('//*[@id="category-latest"]/div/div')[1]
        for article in article_section.css('div.home-small-news-item'):
            yield {
                'title': article.css('.row.half-gutters .hln-content.col-8 .hln-title a::text').get(),
                'date': article.css('.row.half-gutters .hln-content.col-8 .hln-meta.post-meta span::text')[1].get(),
                'link': article.css('.row.half-gutters .hln-content.col-8 .hln-title a::attr(href)').get()
            }
            # print(dict(title=title, date=date, link=link))
        next_page = response.css('div.custom-pagination a::attr(href)').getall()[-2]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

# scrapy crawl articles -o articles.csv

import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"

    start_urls = [
        "https://books.toscrape.com/"
    ]

    def parse(self, response):

        books = response.css("article.product_pod")

        for book in books:
            yield {
                "Title": book.css("h3 a::attr(title)").get(),
                "Price": book.css(".price_color::text").get(),
                "Availability": book.css(".availability::text").getall()[-1].strip()
            }
from crawler.aaa_crawler import crawl_aaa_pages
from crawler.esa_crawler import crawl_esa_pages, crawl_known_esa_cars

if __name__ == '__main__':
    crawl_esa_pages()
    crawl_known_esa_cars()
    crawl_aaa_pages()

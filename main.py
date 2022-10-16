from crawler.EsaCrawler import crawl_esa_pages, crawl_known_esa_cars

def main():
    crawl_esa_pages()
    crawl_known_esa_cars()

if __name__ == '__main__':
    main()
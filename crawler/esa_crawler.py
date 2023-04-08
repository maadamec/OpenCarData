""" ESA Crawler contains functions for crawling pages with multiple cars or single car pages """

import datetime
import re
import multiprocessing as mp
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from psycopg2.errors import UniqueViolation
from common.custom_exceptions import CarSoldOutException
from dbClient.esa_db_client import EsaDbClient
from dbClient.esa_db_factory import esa_car_to_dtos
from dbClient.dto.car_dto import CarDto
from dbClient.dto.job_dto import JobDto
from extractor.esa.esa_extractor import extract_from_list_page, extract_car_from_page


def crawl_esa_pages():
    """ Function that will start crawl pages with multiple cars and save them into the database """
    print("Starting to crawl esa pages")
    pattern: str = "https://www.autoesa.cz/vsechna-auta?zobrazeni=2&stranka={page}"
    page_i: int = 1

    client = EsaDbClient(user="madamec", password="madamec")

    page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
    page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')

    pagination_last = page_bs.find("div", class_="pagination").find('a', class_="ajax", string=re.compile(r"\.\.\."))
    last_page_i = int(re.sub(r"\D+", "", pagination_last.text))

    job_dto = JobDto(None, "Crawl Auto Esa Pages", datetime.datetime.now(), None, "")
    job_dto.job_id = client.insert_job(job_dto)

    with mp.Pool(mp.cpu_count()) as pool:
        for cars in tqdm(pool.imap_unordered(__extract_cars_from_page, range(1, last_page_i + 1))):
            for car in cars:
                car_dto, _ = esa_car_to_dtos(car)
                car_dto.job_id = job_dto.job_id
                try:
                    car_dto.car_id = client.insert_car(car_dto)
                except UniqueViolation:
                    pass
                except (Exception,) as e:
                    print(f"ERROR: Issue during insertion to database. {car_dto}. Exception: ", e)

    job_dto.datetime_end = datetime.datetime.now()
    client.update_job(job_dto)
    client.conn.close()


def crawl_known_esa_cars():
    """ Function that crawls unsold cars in the database and save current variable values into the database """
    print("Starting to crawl esa cars")
    client = EsaDbClient(user="madamec", password="madamec")
    job_dto = JobDto(None, "Crawl Auto Esa Single Cars Pages", datetime.datetime.now(), None, "")
    job_dto.job_id = client.insert_job(job_dto)

    with mp.Pool(mp.cpu_count()) as pool:
        num_of_cars_to_crawl = client.get_count_of_cars_to_crawl()
        num_of_sold = 0
        num_of_error = 0
        for res in tqdm(pool.imap_unordered(__extract_single_car, client.get_cars_to_crawl()),
                        total=num_of_cars_to_crawl):
            car_dto, car, status = res

            if status == "SOLD":
                num_of_sold += 1
                car_dto.datetime_sold = datetime.datetime.now()
                client.update_car_datetime_sold(car_dto.car_id, car_dto.datetime_sold)
            elif status == "ERROR" or car is None:
                num_of_error += 1
                print(f"Skipping result for car {car_dto.car_id} due to status {status} or car is None")
            else:
                _, car_variable_dto = esa_car_to_dtos(car)
                car_variable_dto.car_id = car_dto.car_id
                car_variable_dto.job_id = job_dto.job_id

                try:
                    car_variable_dto.car_variable_id = client.insert_car_variable(car_variable_dto)
                except (Exception,) as e:
                    num_of_error += 1
                    print(f"ERROR: Issue during insertion to database. {car_variable_dto}. Exception: ", e)

    job_dto.datetime_end = datetime.datetime.now()
    client.update_job(job_dto)
    client.conn.close()
    print(f"Number of cars crawled: {num_of_cars_to_crawl}")
    print(f"Number of sold cars: {num_of_sold}")
    print(f"Number of errors: {num_of_error}")


def __extract_single_car(car_dto: CarDto):
    """ Function to extract CarDto from single car page """
    try:
        page_html: str = requests.get(f"https://www.autoesa.cz{car_dto.url}", timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        return car_dto, extract_car_from_page(page_bs), None
    except CarSoldOutException:
        return car_dto, None, "SOLD"
    except (Exception,) as e:
        print(f"ERROR: Issue during single car page extraction. Car {car_dto}. Exception: ", e)
        return car_dto, None, "ERROR"


def __extract_cars_from_page(page_i):
    """ Function to extract list of CarDto from multi car page """
    pattern: str = "https://www.autoesa.cz/vsechna-auta?zobrazeni=2&stranka={page}"
    try:
        page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        return extract_from_list_page(page_bs)
    except (Exception,) as e:
        print(f"ERROR: Issue during extraction. Page: {pattern.replace('{page}', str(page_i))}. Exception: ",
              e.with_traceback(None))
        return []

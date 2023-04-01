import datetime
import re
from tqdm import tqdm
import requests as requests
from bs4 import BeautifulSoup
from psycopg2.errors import UniqueViolation

from common.CustomException import CarSoldOutException
from dbClient.EsaDbClient import EsaDbClient
from dbClient.EsaDbFactory import esa_car_to_dtos
from dbClient.dto.JobDto import JobDto
from model.EsaCar import EsaCar
from extractor.esa.EsaExtractor import extract_from_list_page, extract_car_from_page


def crawl_esa_pages():
    pattern: str = "https://www.autoesa.cz/vsechna-auta?zobrazeni=2&stranka={page}"
    page_i: int = 1
    cars: list[EsaCar] = []

    client = EsaDbClient(user="madamec", password="madamec")

    page_html: str = requests.get(pattern.replace("{page}", str(page_i))).text
    page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')

    pagination_last = page_bs.find("div", class_="pagination").find('a', class_="ajax", string=re.compile("\.\.\."))
    last_page_i = int(re.sub("\D+", "", pagination_last.text))

    job_dto = JobDto(None, "Crawl Auto Esa Pages", datetime.datetime.now(), None, "")
    job_dto.job_id = client.insert_job(job_dto)

    for page_i in tqdm(range(1, last_page_i + 1)):
        try:
            page_html: str = requests.get(pattern.replace("{page}", str(page_i))).text
            page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
            newly_extracted_cars: list[EsaCar] = extract_from_list_page(page_bs)
            cars.extend(newly_extracted_cars)
        except Exception as e:
            print(f"ERROR: Issue during extraction. Page: {pattern.replace('{page}', str(page_i))}. Exception: ",
                  e.with_traceback(None))
            continue
        for car in newly_extracted_cars:
            car_dto, _ = esa_car_to_dtos(car)
            car_dto.job_id = job_dto.job_id
            try:
                car_dto.car_id = client.insert_car(car_dto)
            except UniqueViolation:
                pass
            except Exception as e:
                print(f"ERROR: Issue during insertion to database. {car_dto}. Exception: ", e)

    job_dto.datetime_end = datetime.datetime.now()
    client.update_job(job_dto)
    client.conn.close()


def crawl_known_esa_cars():
    client = EsaDbClient(user="madamec", password="madamec")

    job_dto = JobDto(None, "Crawl Auto Esa Single Cars Pages", datetime.datetime.now(), None, "")
    job_dto.job_id = client.insert_job(job_dto)

    for car_dto in tqdm(client.get_cars_to_crawl()):
        try:
            page_html: str = requests.get(f"https://www.autoesa.cz{car_dto.url}").text
            page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
            car: EsaCar = extract_car_from_page(page_bs)
        except CarSoldOutException:
            print(f"Car with id: {car_dto.car_id} is sold out")
            car_dto.datetime_sold = datetime.datetime.now()
            client.update_car_datetime_sold(car_dto.car_id, car_dto.datetime_sold)
            continue
        except Exception as e:
            print(f"ERROR: Issue during single car page extraction. Car {car_dto}. Exception: ", e)
            continue

        _, car_variable_dto = esa_car_to_dtos(car)
        car_variable_dto.car_id = car_dto.car_id
        car_variable_dto.job_id = job_dto.job_id

        try:
            car_variable_dto.car_variable_id = client.insert_car_variable(car_variable_dto)
        except Exception as e:
            print(f"ERROR: Issue during insertion to database. {car_variable_dto}. Exception: ", e)

    job_dto.datetime_end = datetime.datetime.now()
    client.update_job(job_dto)
    client.conn.close()

""" AAA Crawler contains functions for crawling pages or AAA Auto dealer with multiple cars or single car pages """

import datetime
import re
import multiprocessing as mp
import uuid
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from common.constants import URL_PATTERN_AAA
from dbClient.model import CarModel, JobModel
from dbClient.aaa_db_mapper import car_entity_to_model
from app import app
from app import db
from extractor.aaa.aaa_extractor import extract_from_list_page
from model.aaa_entities import AaaCar, AaaCarVariable


def crawl_aaa_pages():
    print("Starting to crawl aaa auto pages")
    with app.app_context():
        pattern: str = URL_PATTERN_AAA
        page_i: int = 1
        page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')

        # Get last page
        pagination_last = page_bs.find("nav", class_="pagenav").findAll('a')[-2]
        last_page_i = int(re.sub(r"\D+", "", pagination_last.text))

        job_dto = JobModel(job_id=uuid.uuid4(), job_name="Crawl AAA Auto Pages", datetime_start=datetime.datetime.now(),
                           datetime_end=None, detail="")
        db.session.add(job_dto)
        db.session.commit()

        with mp.Pool(mp.cpu_count()) as pool:
            for cars in tqdm(pool.imap_unordered(__extract_cars_from_page, range(1, last_page_i + 1)),
                             total=last_page_i):
                for car in cars:
                    car.job_id = job_dto.job_id
                    car_dto = car_entity_to_model(car)
                    try:
                        db.session.add(car_dto)
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                    except (Exception,) as e:
                        print(f"ERROR: Issue during insertion to database. {car_dto}. Exception: ", e)
                        db.session.rollback()

        job_dto.datetime_end = datetime.datetime.now()
        print(job_dto)
        db.session.add(job_dto)
        db.session.commit()


def crawl_known_aaa_cars():
    pass


def __extract_single_car(car_dto: CarModel) -> tuple[
    CarModel, (AaaCar, None), (AaaCarVariable, None), (str, None)]:
    pass


def __extract_cars_from_page(page_i) -> list[AaaCar]:
    """ Function to extract list of CarDto from multi car page """
    pattern: str = URL_PATTERN_AAA
    try:
        page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        return extract_from_list_page(page_bs)
    except (Exception,) as e:
        print(f"ERROR: Issue during extraction. Page: {pattern.replace('{page}', str(page_i))}. Exception: ",
              e.with_traceback(None))
        return []

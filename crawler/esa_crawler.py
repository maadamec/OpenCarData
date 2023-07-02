""" ESA Crawler contains functions for crawling pages with multiple cars or single car pages """

import datetime
import re
import multiprocessing as mp
import uuid
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from common.constants import URL_PATTERN_ESA, RESELLER_NAME_AUTO_ESA
from common.custom_exceptions import CarSoldOutException
from dbClient.model import CarModel, JobModel
from dbClient.esa_db_mapper import car_entity_to_model, car_variable_entity_to_model
from extractor.esa.esa_extractor import extract_from_list_page, extract_car_from_page
from app import app
from app import db
from model.entities import EsaCar, EsaCarVariable


def crawl_esa_pages():
    """ Function that will start crawl pages with multiple cars and save them into the database """
    with app.app_context():
        print("Starting to crawl esa pages")
        pattern: str = URL_PATTERN_ESA
        page_i: int = 1

        page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')

        pagination_last = page_bs.find("div", class_="pagination").find('a', class_="ajax",
                                                                        string=re.compile(r"\.\.\."))
        last_page_i = int(re.sub(r"\D+", "", pagination_last.text))

        job_dto = JobModel(
            job_id=uuid.uuid4(),
            job_name="Crawl Auto Esa Pages",
            datetime_start=datetime.datetime.now(),
            datetime_end=None,
            detail=""
        )
        db.session.add(job_dto)
        db.session.commit()

        with mp.Pool(mp.cpu_count()) as pool:
            for cars in tqdm(pool.imap_unordered(__extract_cars_from_page, range(1, last_page_i + 1)),
                             total=last_page_i):
                for car, _ in cars:
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
        db.session.add(job_dto)
        db.session.commit()


def crawl_known_esa_cars():
    """ Function that crawls unsold cars in the database and save current variable values into the database """
    with app.app_context():
        print("Starting to crawl esa cars")

        job_dto = JobModel(
            job_id=uuid.uuid4(),
            job_name="Crawl Auto Esa Single Cars Pages",
            datetime_start=datetime.datetime.now(),
            datetime_end=None,
            detail=""
        )
        db.session.add(job_dto)
        db.session.commit()

        db.session().expire_on_commit = False

        with mp.Pool(mp.cpu_count()) as pool:
            query = db.session.query(CarModel).filter_by(datetime_sold=None, reseller=RESELLER_NAME_AUTO_ESA)
            num_of_cars_to_crawl = query.count()
            num_of_sold = 0
            num_of_error = 0
            for res in tqdm(pool.imap_unordered(__extract_single_car, query.all()), total=num_of_cars_to_crawl):
                car_dto, _, car_variable, status = res

                if status == "SOLD":
                    num_of_sold += 1
                    try:
                        CarModel.query.filter_by(car_id=car_dto.car_id).update(
                            dict(datetime_sold=datetime.datetime.now()))
                        db.session.commit()
                    except IntegrityError as e:
                        print(f"ERROR: Issue during update to database. {car_dto.reseller_id}, rollback ", e)
                        db.session.rollback()
                    except (Exception,) as e:
                        num_of_error += 1
                        print(f"ERROR: Issue during update to database. {car_dto.reseller_id}. Exception: ", e)
                        db.session.rollback()
                elif status == "ERROR" or car_variable is None:
                    num_of_error += 1
                    print(f"Skipping result for car {car_dto.car_id} due to status {status} or car is None")
                else:
                    car_variable_dto = car_variable_entity_to_model(car_variable)
                    car_variable_dto.car_id = car_dto.car_id
                    car_variable_dto.job_id = job_dto.job_id

                    try:
                        db.session.add(car_variable_dto)
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                    except (Exception,) as e:
                        num_of_error += 1
                        print(f"ERROR: Issue during insertion to database. {car_variable_dto}. Exception: ", e)
                        db.session.rollback()

        JobModel.query.filter_by(job_id=job_dto.job_id).update(
            {"datetime_end": datetime.datetime.now()})
        db.session.commit()

        db.session().expire_on_commit = True

        print(f"Number of cars crawled: {num_of_cars_to_crawl}")
        print(f"Number of sold cars: {num_of_sold}")
        print(f"Number of errors: {num_of_error}")


def __extract_single_car(car_dto: CarModel) -> tuple[
    CarModel, (EsaCar, None), (EsaCarVariable, None), (str, None)]:
    """ Function to extract CarDto from single car page """
    try:
        page_html: str = requests.get(f"https://www.autoesa.cz{car_dto.url}", timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        new_car, new_car_variable = extract_car_from_page(page_bs)
        return car_dto, new_car, new_car_variable, None
    except CarSoldOutException:
        return car_dto, None, None, "SOLD"
    except (Exception,) as e:
        print(f"ERROR: Issue during single car page extraction. Car {car_dto}. Exception: ", e)
        return car_dto, None, None, "ERROR"


def __extract_cars_from_page(page_i) -> list[tuple[EsaCar, EsaCarVariable]]:
    """ Function to extract list of CarDto from multi car page """
    pattern: str = URL_PATTERN_ESA
    try:
        page_html: str = requests.get(pattern.replace("{page}", str(page_i)), timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        return extract_from_list_page(page_bs)
    except (Exception,) as e:
        print(f"ERROR: Issue during extraction. Page: {pattern.replace('{page}', str(page_i))}. Exception: ",
              e.with_traceback(None))
        return []

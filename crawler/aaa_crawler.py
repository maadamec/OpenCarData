""" AAA Crawler contains functions for crawling pages or AAA Auto dealer with multiple cars or single car pages """

import datetime
import re
import multiprocessing as mp
import uuid
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from common.constants import URL_PATTERN_AAA, RESELLER_NAME_AAA_AUTO
from common.custom_exceptions import CarSoldOutException
from dbClient.model import CarModel, JobModel
from dbClient.aaa_db_mapper import car_entity_to_model, car_variable_entity_to_model
from app import app
from app import db
from extractor.aaa.aaa_extractor import extract_from_list_page, extract_car_from_page
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

        job_dto = JobModel(
            job_id=uuid.uuid4(),
            job_name="Crawl AAA Auto Pages",
            datetime_start=datetime.datetime.now(),
            datetime_end=None,
            detail=""
        )
        db.session.add(job_dto)
        db.session.commit()

        with mp.Pool(mp.cpu_count()) as pool:
            for cars in tqdm(pool.imap_unordered(__extract_cars_from_page, range(1, last_page_i + 1)),
                             total=last_page_i, mininterval=2):
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
        db.session.add(job_dto)
        db.session.commit()


def crawl_known_aaa_cars():
    """ Function that crawls unsold cars in the database and save current variable values into the database """
    with app.app_context():
        print("Starting to crawl known AAA cars")

        job_dto = JobModel(
            job_id=uuid.uuid4(),
            job_name="Crawl AAA Auto Single Cars Pages",
            datetime_start=datetime.datetime.now(),
            datetime_end=None,
            detail=""
        )
        db.session.add(job_dto)
        db.session.commit()

        db.session().expire_on_commit = False

        with mp.Pool(mp.cpu_count()) as pool:
            query = db.session.query(CarModel).filter_by(datetime_sold=None, reseller=RESELLER_NAME_AAA_AUTO)
            num_of_cars_to_crawl = query.count()
            num_of_sold = 0
            num_of_error = 0
            for res in tqdm(pool.imap_unordered(__extract_single_car, query.all()),
                            total=num_of_cars_to_crawl, mininterval=2):
                car_dto, aaa_car, car_variable, status = res
                db.session.begin(nested=True)
                if status == "SOLD":
                    num_of_sold += 1
                    try:
                        CarModel.query\
                            .filter_by(car_id=car_dto.car_id)\
                            .update({"datetime_sold": datetime.datetime.now()})
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
                    # Fill missing values
                    if car_dto.equipment_class is None:
                        updated_values = {
                            "equipment_class": aaa_car.equipment_class,
                            "brand": aaa_car.brand,
                            "body_type": aaa_car.body_type,
                            "gear": aaa_car.gear,
                        }
                        CarModel.query.filter_by(car_id=car_dto.car_id).update(updated_values)

                    car_variable_dto = car_variable_entity_to_model(car_variable)
                    car_variable_dto.car_id = car_dto.car_id
                    car_variable_dto.job_id = job_dto.job_id

                    try:
                        db.session.add(car_variable_dto)
                        db.session.commit()
                    except IntegrityError as e:
                        print(f"ERROR: Issue during insertion to database. car dto: {car_dto}, {car_variable_dto}. Exception: ", e)
                        db.session.rollback()
                    except (Exception,) as e:
                        num_of_error += 1
                        print(f"ERROR: Issue during insertion to database. car dto: {car_dto}, {car_variable_dto}. Exception: ", e)
                        db.session.rollback()

        JobModel.query.filter_by(job_id=job_dto.job_id).update(
            {"datetime_end": datetime.datetime.now()})
        db.session.commit()

        db.session().expire_on_commit = True
        db.session.close()

        print(f"Number of cars crawled: {num_of_cars_to_crawl}")
        print(f"Number of sold cars: {num_of_sold}")
        print(f"Number of errors: {num_of_error}")


def __extract_single_car(car_dto: CarModel) -> tuple[
    CarModel, (AaaCar, None), (AaaCarVariable, None), (str, None)]:
    """ Function to extract CarDto from single car page """
    try:
        page_html: str = requests.get(f"https://www.aaaauto.cz{car_dto.url}", timeout=30).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        new_car, new_car_variable = extract_car_from_page(page_bs)
        return car_dto, new_car, new_car_variable, None
    except CarSoldOutException:
        return car_dto, None, None, "SOLD"
    except (Exception,) as e:
        print(f"ERROR: Issue during single car page extraction. Car {car_dto}. Exception: ", e)
        return car_dto, None, None, "ERROR"


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

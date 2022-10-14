import requests as requests
from bs4 import BeautifulSoup
from psycopg2.errors import UniqueViolation
from dbClient.EsaDbClient import EsaDbClient
from dbClient.EsaDbFactory import esa_car_to_dtos
from model.EsaCar import EsaCar
from extractor.esa.EsaExtractor import extract_from_list_page


def crawlEsaPages():

    pattern: str = "https://www.autoesa.cz/vsechna-auta?stranka={page}"
    page_i: int = 1
    cars: list[EsaCar] = []

    client = EsaDbClient(user="madamec", password="madamec")

    has_next_page: bool = True
    while has_next_page:
        page_html: str = requests.get(pattern.replace("{page}", str(page_i))).text
        page_bs: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        newly_extracted_cars: list[EsaCar] = extract_from_list_page(page_bs)
        cars.extend(newly_extracted_cars)
        for car in newly_extracted_cars:
            print(car)
            car_dto, car_variable_dto = esa_car_to_dtos(car)

            try:
                car_id = client.insert_car(car_dto)
                car_dto.car_id = car_id
                car_variable_dto.car_id = car_id

                # car_variable_id = client.insert_car_variable(car_variable_dto)
                # car_variable_dto.car_variable_id = car_variable_id
            except UniqueViolation:
                print(f"UniqueViolation on insert: esa_id {car_dto.esa_id}")


        # client.commit()


        print(f"Page {page_i} crawled")

        has_next_page = page_bs.find('li', class_="pagination__next") is not None
        page_i += 1

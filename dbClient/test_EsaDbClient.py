from unittest import TestCase

from dbClient.EsaDbClient import EsaDbClient
from dbClient.dto.CarDto import CarDto
from dbClient.dto.CarVariableDto import CarVariableDto
from datetime import datetime
import sys

class Test(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        client = EsaDbClient("madamec", "madamec", "localhost", "5432", "test")

        with client.get_cursor() as cur:
            print("Creating tables")
            with open("dbClient/scripts/create.sql", "r", encoding="UTF-8") as create_script:
                cur.execute(create_script.read())
            print("Tables created.")
            print("Inserting data.")
            with open("dbClient/scripts/insert_test_data.sql", "r", encoding="UTF-8") as insert_script:
                cur.execute(insert_script.read())
            print("Data inserted.")
        client.conn.close()

    def setUp(self) -> None:
        self.client = EsaDbClient("madamec", "madamec", "localhost", "5432", "test")

    def test_insert_car(self):
        car = CarDto(None, "url", "image", "esa_id", "skoda", "full_name", "engine", "equipment_class",
                     2022, "gear", 77, "fuel", "kombi", 80000, ["test", "tag"], datetime.now(), None, 1)

        car_id = self.client.insert_car(car)
        self.assertIsNotNone(car_id)

    def test_insert_car_variable(self):
        car_id = 101
        with self.client.get_cursor() as cur:
            cur.execute("SELECT car_id from public.car limit 1")
            car_id = cur.fetchone()[0]

        lowcost = True
        premium = True
        monthly_price = 1000
        special_price = 100000
        condition = 7.5
        price = 110000
        discount = 20000
        job_id = 1

        datetime_captured = datetime.now()
        variable = CarVariableDto(car_variable_id=None, car_id=car_id, lowcost=lowcost, premium=premium, monthly_price=monthly_price,
                                  special_price=special_price, condition=condition, price=price, discount=discount,
                                  datetime_captured=datetime_captured, job_id=job_id)
        variable_id = self.client.insert_car_variable(variable)

        with self.client.get_cursor() as cur:
            cur.execute(f"""SELECT car_variable_id, car_id, lowcost, premium, monthly_price, special_price, condition, price, discount, 
                           datetime_captured, job_id FROM public.car_variable WHERE car_variable_id = {variable_id};""")
            new_variable = cur.fetchone()
            new_variable_dto = CarVariableDto(*new_variable)
            self.assertIsNotNone(new_variable_dto)
            self.assertEqual(variable_id, new_variable_dto.car_variable_id)
        self.assertIsNotNone(variable_id)

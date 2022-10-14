import psycopg2

from dbClient.dto.BodyTypeDto import BodyTypeDto
from dbClient.dto.BrandDto import BrandDto
from dbClient.dto.CarDto import CarDto
from dbClient.dto.CarVariableDto import CarVariableDto

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
POSTGRE_DATETIME_FORMAT = 'yyyy-mm-dd hh24:mi:ss'

class EsaDbClient:

    def __init__(self,
                 user: str = "postgres",
                 password: str = "postgres",
                 host: str = "localhost",
                 port: str = "5432",
                 database: str = "postgres"):
        self.conn = psycopg2.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     database=database)
        self.conn.autocommit = True
        self.brands: dict[str, BrandDto] = {}
        self.body_types: dict[str, BodyTypeDto] = dict()
        print("Connection established")

    # def commit(self):
    #     self.conn.commit()
    #     print("Changes committed")
    #
    # def rollback(self):
    #     self.conn.rollback()
    #     print("Changes rollback")

    def get_cursor(self):
        return self.conn.cursor()

    def insert_car(self, car: CarDto):
        formatted_tags: str = "{" + ",".join([f"\"{tag}\"" for tag in car.tags]) + "}"
        insert_query = f"""
            INSERT INTO public.car( 
                                    image, 
                                    esa_id, 
                                    brand, 
                                    full_name, 
                                    engine, 
                                    equipment_class, 
                                    year, 
                                    gear, 
                                    power, 
                                    fuel, 
                                    body_type, 
                                    mileage, 
                                    tags,
                                    datetime_captured)
        VALUES ({self.__get_value_or_null(car.image, True)}, 
                {self.__get_value_or_null(car.esa_id, True)}, 
                {self.__get_value_or_null(car.brand, True)}, 
                {self.__get_value_or_null(car.full_name, True)}, 
                {self.__get_value_or_null(car.engine, True)}, 
                {self.__get_value_or_null(car.equipment_class, True)}, 
                {self.__get_value_or_null(car.year)}, 
                {self.__get_value_or_null(car.gear, True)}, 
                {self.__get_value_or_null(car.power)}, 
                {self.__get_value_or_null(car.fuel, True)}, 
                {self.__get_value_or_null(car.body_type, True)}, 
                {self.__get_value_or_null(car.mileage)}, 
                {self.__get_value_or_null(formatted_tags, True)},
                (to_timestamp('{car.datetime_captured.strftime(DATETIME_FORMAT)}', '{POSTGRE_DATETIME_FORMAT}'))) 
        RETURNING car_id;
        """

        with self.get_cursor() as cur:
            cur.execute(insert_query)
            print("Insert car executed")
            return cur.fetchone()[0]

    def insert_car_variable(self, car_variable: CarVariableDto):
        insert_query = f"""
            INSERT INTO public.car_variable(
                                    car_id, 
                                    lowcost, 
                                    premium, 
                                    monthly_price, 
                                    special_price, 
                                    condition, 
                                    price, 
                                    discount, 
                                    datetime_captured)
        VALUES ({self.__get_value_or_null(car_variable.car_id)}, 
                {self.__get_value_or_null(car_variable.lowcost)}, 
                {self.__get_value_or_null(car_variable.premium)}, 
                {self.__get_value_or_null(car_variable.monthly_price)},
                {self.__get_value_or_null(car_variable.special_price)}, 
                {self.__get_value_or_null(car_variable.condition)}, 
                {self.__get_value_or_null(car_variable.price)}, 
                {self.__get_value_or_null(car_variable.discount)}, 
                (to_timestamp('{car_variable.datetime_captured.strftime(DATETIME_FORMAT)}', '{POSTGRE_DATETIME_FORMAT}'))) 
        RETURNING car_variable_id;
        """

        with self.get_cursor() as cur:
            cur.execute(insert_query)
            print("Car Variable inserted")
            return cur.fetchone()[0]

    # def __get_brands(self):
    #     if len(self.brands) == 0:
    #         with self.get_cursor() as cur:
    #             cur.execute("SELECT brand_id, brand_name FROM public.brand")
    #             for record in cur:
    #                 self.brands[record[1]] = BrandDto(record[0], record[1])
    #             print(f"Brands retrieved [{len(self.brands)}]")
    #     return self.brands
    #
    # def __get_body_types(self):
    #     if len(self.body_types) == 0:
    #         with self.get_cursor() as cur:
    #             cur.execute("SELECT body_type_id, body_type_name FROM public.body_type")
    #             for record in cur:
    #                 self.body_types[record[1]] = BodyTypeDto(record[0], record[1])
    #             print(f"Brands retrieved [{len(self.body_types)}]")
    #     return self.body_types

    @staticmethod
    def __get_value_or_null(value, add_quotes: bool = False):
        if value is not None:
            return f"'{value}'" if add_quotes else value
        else:
            return "null"

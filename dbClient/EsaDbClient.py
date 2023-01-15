import datetime
from typing import Generator

import psycopg2

from dbClient.dto.CarDto import CarDto
from dbClient.dto.CarVariableDto import CarVariableDto
from dbClient.dto.JobDto import JobDto


class EsaDbClient:

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    POSTGRE_DATETIME_FORMAT = 'yyyy-mm-dd hh24:mi:ss'

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
        print("Connection established")

    def get_cursor(self):
        return self.conn.cursor()

    def insert_car(self, car: CarDto) -> int:
        formatted_tags: str = "{" + ",".join([f"\"{tag}\"" for tag in car.tags]) + "}"
        formatted_datetime_sold: str = f"(to_timestamp('{car.datetime_sold.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}'))" if car.datetime_sold is not None else "null"

        insert_query = f"""
            INSERT INTO public.car(image, url, esa_id, brand, full_name, engine, equipment_class, year, gear, power, 
                                    fuel, body_type, mileage, tags, datetime_captured, datetime_sold, job_id)
        VALUES ({self.__get_value_or_null(car.image, True)}, 
                {self.__get_value_or_null(car.url, True)}, 
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
                (to_timestamp('{car.datetime_captured.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}')),
                {formatted_datetime_sold},
                {self.__get_value_or_null(car.job_id)})
        RETURNING car_id;
        """

        with self.get_cursor() as cur:
            cur.execute(insert_query)
            return cur.fetchone()[0]

    def update_car_datetime_sold(self, car_id: int, datetime_sold: datetime.datetime):
        insert_query = f"""
                    UPDATE public.car
                    SET datetime_sold=(to_timestamp('{datetime_sold.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}'))
                    WHERE car_id={car_id};
                """
        with self.get_cursor() as cur:
            cur.execute(insert_query)

    def insert_car_variable(self, car_variable: CarVariableDto) -> int:
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
                                    datetime_captured,
                                    job_id)
        VALUES ({self.__get_value_or_null(car_variable.car_id)}, 
                {self.__get_value_or_null(car_variable.lowcost)}, 
                {self.__get_value_or_null(car_variable.premium)}, 
                {self.__get_value_or_null(car_variable.monthly_price)},
                {self.__get_value_or_null(car_variable.special_price)}, 
                {self.__get_value_or_null(car_variable.condition)}, 
                {self.__get_value_or_null(car_variable.price)}, 
                {self.__get_value_or_null(car_variable.discount)}, 
                (to_timestamp('{car_variable.datetime_captured.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}')),
                {self.__get_value_or_null(car_variable.job_id)}) 
        RETURNING car_variable_id;
        """

        with self.get_cursor() as cur:
            cur.execute(insert_query)
            return cur.fetchone()[0]

    def get_cars_to_crawl(self) -> Generator[CarDto, CarDto, None]:
        with self.get_cursor() as cur:
            cur.execute("""SELECT car_id, url, image, esa_id, brand, full_name, engine, equipment_class,
                                year, gear, power, fuel, body_type, mileage, tags, datetime_captured, datetime_sold, job_id
                           from public.car
                           WHERE datetime_sold is null""")
            for record in cur:
                yield CarDto(*record)

    def insert_job(self, job_dto: JobDto):
        insert_query = f"""
                INSERT INTO public.job(job_name, datetime_start, detail)
                VALUES ({self.__get_value_or_null(job_dto.job_name, True)}, 
                        (to_timestamp('{job_dto.datetime_start.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}')),
                        {self.__get_value_or_null(job_dto.detail, True)}) 
                RETURNING job_id;
                """

        with self.get_cursor() as cur:
            cur.execute(insert_query)
            print("Job created")
            return cur.fetchone()[0]

    def update_job(self, job_dto: JobDto):
        update_query = f"""
                UPDATE public.job
                SET job_name={self.__get_value_or_null(job_dto.job_name, True)}, 
                    datetime_start=to_timestamp('{job_dto.datetime_start.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}'), 
                    datetime_end=to_timestamp('{job_dto.datetime_end.strftime(self.DATETIME_FORMAT)}', '{self.POSTGRE_DATETIME_FORMAT}'), 
                    detail={self.__get_value_or_null(job_dto.detail, True)}
                WHERE job_id={job_dto.job_id}
                """

        with self.get_cursor() as cur:
            cur.execute(update_query)
            print(f"Job [{job_dto.job_id}] updated")

    @staticmethod
    def __get_value_or_null(value, add_quotes: bool = False):
        if value is not None:
            return f"'{value}'" if add_quotes else value
        else:
            return "null"

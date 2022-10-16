from typing import Tuple

from dbClient.dto.CarDto import CarDto
from dbClient.dto.CarVariableDto import CarVariableDto
from model.EsaCar import EsaCar

def esa_car_to_dtos(esa_car: EsaCar) -> Tuple[CarDto, CarVariableDto]:
    car_dto: CarDto = CarDto(car_id=None, url=esa_car.url, image=esa_car.image, esa_id=esa_car.esa_id, brand=esa_car.brand,
                             full_name=esa_car.full_name, engine=esa_car.engine,equipment_class= esa_car.equipment_class,
                             year=esa_car.year, gear=esa_car.gear, power=esa_car.power, fuel=esa_car.fuel,
                             body_type=esa_car.body_type, mileage=esa_car.mileage, tags=esa_car.tags,
                             datetime_captured= esa_car.datetime_captured, job_id=None)

    car_variable_dto: CarVariableDto = CarVariableDto(car_variable_id=None, car_id=None, lowcost=esa_car.lowcost, premium=esa_car.premium,
                                                      monthly_price=esa_car.monthly_price, special_price=esa_car.special_price,
                                                      condition=esa_car.condition, price=esa_car.price, discount=esa_car.discount,
                                                      datetime_captured=esa_car.datetime_captured, job_id=None)
    return car_dto, car_variable_dto

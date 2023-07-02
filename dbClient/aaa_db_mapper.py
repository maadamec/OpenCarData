""" Function to transform model to entity and other way around """
from common.constants import RESELLER_NAME_AAA_AUTO
from dbClient.model import CarModel
from dbClient.model import CarVariableModel
from dbClient.model import JobModel
from model.aaa_entities import AaaCar, AaaCarVariable
from model.entities import Job


def job_model_to_entity(instance: JobModel) -> Job:
    return Job(
        job_id=instance.job_id,
        job_name=instance.job_name,
        datetime_start=instance.datetime_start,
        datetime_end=instance.datetime_end,
        detail=instance.detail
    )

def job_entity_to_model(instance: Job) -> JobModel:
    return JobModel(
        job_id=instance.job_id,
        job_name=instance.job_name,
        datetime_start=instance.datetime_start,
        datetime_end=instance.datetime_end,
        detail=instance.detail
    )


def car_model_to_entity(instance: CarModel) -> AaaCar:
    return AaaCar(
        car_id=instance.car_id,
        url=instance.url,
        image=instance.image,
        aaa_id=instance.reseller_id,
        brand=instance.brand,
        full_name=instance.full_name,
        engine=instance.engine,
        equipment_class=instance.equipment_class,
        year=instance.year,
        gear=instance.gear,
        power=instance.power,
        fuel=instance.fuel,
        body_type=instance.body_type,
        mileage=instance.mileage,
        datetime_captured=instance.datetime_captured,
        datetime_sold=instance.datetime_sold,
        job_id=instance.job_id,
    )

def car_entity_to_model(instance: AaaCar) -> CarModel:
    return CarModel(
        car_id=instance.car_id,
        url=instance.url,
        image=instance.image,
        reseller=RESELLER_NAME_AAA_AUTO,
        reseller_id=instance.aaa_id,
        brand=instance.brand,
        full_name=instance.full_name,
        engine=instance.engine,
        equipment_class=instance.equipment_class,
        year=instance.year,
        gear=instance.gear,
        power=instance.power,
        fuel=instance.fuel,
        body_type=instance.body_type,
        mileage=instance.mileage,
        datetime_captured=instance.datetime_captured,
        datetime_sold=instance.datetime_sold,
        job_id=instance.job_id,
    )


def car_variable_model_to_entity(instance: CarVariableModel) -> AaaCarVariable:
    return AaaCarVariable(
        car_variable_id=instance.car_variable_id,
        car_id=instance.car_id,
        monthly_price=instance.monthly_price,
        special_price=instance.special_price,
        price=instance.price,
        discount=instance.discount,
        datetime_captured=instance.datetime_captured,
        job_id=instance.job_id,
    )

def car_variable_entity_to_model(instance: AaaCarVariable) -> CarVariableModel:
    return CarVariableModel(
        car_variable_id=instance.car_variable_id,
        car_id=instance.car_id,
        lowcost=False,
        premium=False,
        monthly_price=instance.monthly_price,
        special_price=instance.special_price,
        condition=0,
        price=instance.price,
        discount=instance.discount,
        datetime_captured=instance.datetime_captured,
        job_id=instance.job_id,
    )

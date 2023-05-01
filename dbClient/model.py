"""Class to store information from the EsaCar website"""
from __future__ import annotations
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ARRAY, DateTime, ForeignKey, UUID, Boolean, Float

db = SQLAlchemy()


@dataclass
class JobModel(db.Model):
    """ Class to represent job run """
    __tablename__ = "job"

    job_id = db.Column(UUID(as_uuid=True), primary_key=True)
    job_name = db.Column(String)
    datetime_start = db.Column(DateTime)
    datetime_end = db.Column(DateTime, nullable=True)
    detail = db.Column(String)


@dataclass
class CarModel(db.Model):
    """ Class representing one car from AUTO ESA without variable attributes """
    __tablename__ = "car"

    car_id = db.Column(UUID(as_uuid=True), primary_key=True)
    url = db.Column(String)
    image = db.Column(String)
    esa_id = db.Column(String, unique=True)
    brand = db.Column(String)
    full_name = db.Column(String)
    engine = db.Column(String)
    equipment_class = db.Column(String)
    year = db.Column(Integer)
    gear = db.Column(String)
    power = db.Column(Integer)
    fuel = db.Column(String)
    body_type = db.Column(String)
    mileage = db.Column(Integer)
    tags = db.Column(ARRAY(String))
    datetime_captured = db.Column(DateTime)
    datetime_sold = db.Column(DateTime)
    job_id = db.Column(UUID(as_uuid=True), ForeignKey("job.job_id"))


@dataclass
class CarVariableModel(db.Model):
    """ Class to represent variable attributes of cat from AUTO ESA"""
    __tablename__ = "car_variable"

    car_variable_id = db.Column(UUID(as_uuid=True), primary_key=True)
    car_id = db.Column(UUID(as_uuid=True), ForeignKey("car.car_id"))
    lowcost = db.Column(Boolean)
    premium = db.Column(Boolean)
    monthly_price = db.Column(Integer)
    special_price = db.Column(Integer)
    condition = db.Column(Integer)
    price = db.Column(Integer)
    discount = db.Column(Integer)
    datetime_captured = db.Column(DateTime)
    job_id = db.Column(UUID(as_uuid=True), ForeignKey("job.job_id"))

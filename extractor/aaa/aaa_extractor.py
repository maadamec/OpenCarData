from __future__ import annotations

import datetime
import re
import uuid
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from common.custom_exceptions import CarSoldOutException
from common.decorators import save_attribute_extraction
from common.utils import clear_text
from extractor.esa.esa_extractor import clear_integer
from model.aaa_entities import AaaCar, AaaCarVariable


def extract_from_list_page(page: BeautifulSoup) -> list[AaaCar]:
    result: list[AaaCar] = []
    for car in page.find("div", id="carsGrid").find_all("div", class_="card box"):
        url = __extract_car_url(car)
        image_url = __extract_image_url(car)
        aaa_id = __extract_aaa_id(url)
        brand = __extract_brand(url)
        gear = __extract_gear(car)
        full_name = __extract_full_name(car)
        engine = __extract_engine(car)
        year = __extract_year(car)
        power = __extract_power(car)
        fuel = __extract_fuel(car)
        mileage = __extract_mileage(car)
        car_id = uuid.uuid4()
        result.append(
            AaaCar(
                car_id=car_id,
                url=url,
                image=image_url,
                aaa_id=aaa_id,
                brand=brand,
                full_name=full_name,
                engine=engine,
                equipment_class=None,
                year=year,
                gear=gear,
                power=power,
                fuel=fuel,
                body_type=None,
                mileage=mileage,
                datetime_captured=datetime.now(),
                datetime_sold=None,
                job_id=None
            )
        )
    return result


@save_attribute_extraction(element="car url")
def __extract_car_url(car: Tag):
    return car.find('a', class_="fullSizeLink")['href'].replace("https://www.aaaauto.cz")


@save_attribute_extraction(element="image url")
def __extract_image_url(car: Tag):
    return car.find('figure').find('img')['src']


@save_attribute_extraction(element="aaa id")
def __extract_aaa_id(url: str):
    return re.search("id=(.+)#", url).group(1)


@save_attribute_extraction(element="brand")
def __extract_brand(url: str):
    # TODO: change this to catch all brands
    return re.search("/cz/(.+)-(.+)/", url).group(1)


@save_attribute_extraction(element="full name")
def __extract_full_name(car: Tag):
    return re.sub(',', '', re.sub(r'\s+', ' ', car
                                  .find('div', class_="carFeatures")
                                  .find("h2")
                                  .find("a")
                                  .find(text=True, recursive=False)
                                  .get_text(strip=True, separator=' ')))


@save_attribute_extraction(element="engine")
def __extract_engine(car: Tag):
    return clear_text(
        car.find('div', class_="carFeatures")
        .find('ul', class_="carFeaturesList")
        .find(lambda tag: "kW" in tag.text)
        .get_text(strip=True, separator=' ')
        .split(" / ")[0]
    )


@save_attribute_extraction(element="equipment class")
def __extract_equipment_class(url: str):
    return re.search("^/.+/(.+)/.+/.+/.+", url).group(1)


@save_attribute_extraction(element="year")
def __extract_year(car: Tag):
    return clear_integer(
        car.find('div', class_="carFeatures").find("h2").find("span", class_="regular").get_text(strip=True,
                                                                                                 separator=' '))


@save_attribute_extraction(element="gear")
def __extract_gear(car: Tag):
    tag_text = clear_text(
        car.find('div', class_="carFeatures")
        .find('ul', class_="carFeaturesList")
        .find(lambda tag: " stupňů" in tag.text or "Automat" in tag.text)
        .get_text(strip=True, separator=' ')
    )

    if "Automat" in tag_text:
        return "automat"
    return "manual"


@save_attribute_extraction(element="power")
def __extract_power(car: Tag):
    return clear_integer(clear_text(
        car.find('div', class_="carFeatures")
        .find('ul', class_="carFeaturesList")
        .find(lambda tag: "kW" in tag.text)
        .get_text(strip=True, separator=' ')
        .split(" / ")[1].split(", ")[0]
    ))


@save_attribute_extraction(element="fuel")
def __extract_fuel(car: Tag):
    # TODO: map to known values Benzín -> benzin
    return clear_text(
        car.find('div', class_="carFeatures")
        .find('ul', class_="carFeaturesList")
        .find_all('li')[2]
        .get_text(strip=True, separator=' ')
    )


@save_attribute_extraction(element="body type")
def __extract_body(url: str):
    return re.search("^/.+/.+/(.+)/.+/.+", url).group(1)


@save_attribute_extraction(element="mileage")
def __extract_mileage(car: Tag):
    tag = car.find('div', class_="carFeatures") \
        .find('ul', class_="carFeaturesList") \
        .find(lambda tag: " km" in tag.text)

    if tag is not None:
        return clear_integer(clear_text(tag.get_text(strip=True, separator=' ')))
    return None


@save_attribute_extraction(element="monthly price")
def __extract_monthly_price(car: Tag):
    monthly_price = 0
    if (monthly_price_el := car.find('div', class_="car_item__price_holder").find('div',
                                                                                  "car_item__price_block")) is not None:
        monthly_price_text = re.search(r"Měsíčně od\s*([\s0-9]+)\s*Kč",
                                       clear_text(monthly_price_el.get_text(strip=True, separator=' ')))
        monthly_price = 0 if monthly_price_text is None else clear_integer(
            monthly_price_text.group(1).replace(" ", "").strip())
    return monthly_price


@save_attribute_extraction(element="special price")
def __extract_special_price(car: Tag):
    special_price = 0
    if (special_price_el := car.find('div', class_="car_item__price_holder").find('div',
                                                                                  "car_item__price_block text-red")) is not None:
        special_price_text = re.search(r"Akční cena\s*([\s0-9]+)\s*Kč",
                                       clear_text(special_price_el.get_text(strip=True, separator=' ')))
        special_price = 0 if special_price_text is None else int(
            special_price_text.group(1).replace(" ", "").strip())
    return special_price


@save_attribute_extraction(element="discount")
def __extract_discount(car: Tag):
    discount = 0
    if (discount_el := car.find('div', class_="car_item__save")) is not None:
        discount_text = re.search(r"Zlevněno o\s*([\s0-9]+)\s*Kč",
                                  re.sub(r"\s+", " ", discount_el.get_text(strip=True, separator=' ')))
        discount = 0 if discount_text is None else int(discount_text.group(1).replace(" ", "").strip())
    return discount


def extract_car_from_page(page: BeautifulSoup) -> tuple[AaaCar, AaaCarVariable]:
    __check_single_if_sold(page)

    brand = __extract_single_brand(page)
    full_name = __extract_single_full_name(page)
    monthly_price = __extract_single_monthly_price(page)
    special_price = __extract_single_special_price(page)
    price = __extract_single_price(page)
    discount = __extract_single_discount(page)

    # Detail box
    detail_box = __get_single_detail_box_element(page)
    year = clear_integer(detail_box["Rok uvedení do provozu"])
    gear = clear_text(detail_box["Převodovka"].split("/")[0])
    fuel = clear_text(detail_box["Palivo"])
    mileage = clear_integer(detail_box["Tachometr"])
    car_body = clear_text(detail_box["Karoserie"])

    equipment_class = full_name.replace(brand, "").replace(str(year), "").replace(",", "")
    if detail_box["Motor"]:
        equipment_class = equipment_class.replace(clear_text(detail_box["Motor"]), "")
    if detail_box["Pohon"]:
        equipment_class = equipment_class.replace(clear_text(detail_box["Pohon"].split(",")[0]), "")
    equipment_class = clear_text(equipment_class)

    car_id = uuid.uuid4()
    return (
        AaaCar(
            car_id=car_id,
            url=None,
            image=None,
            aaa_id=None,
            brand=brand,
            full_name=full_name,
            engine=None,
            equipment_class=equipment_class,
            year=year,
            gear=gear,
            power=None,
            fuel=fuel,
            body_type=car_body,
            mileage=mileage,
            datetime_captured=datetime.now(),
            datetime_sold=None,
            job_id=None
        ),
        AaaCarVariable(
            car_variable_id=uuid.uuid4(),
            car_id=car_id,
            monthly_price=monthly_price,
            special_price=special_price,
            price=price,
            discount=discount,
            datetime_captured=datetime.now(),
            job_id=None
        )
    )


def __check_single_if_sold(page: BeautifulSoup):
    if page.find("div", id="carCardHead") is None:
        raise CarSoldOutException()


def __get_single_detail_box_element(page: BeautifulSoup):
    result: dict = {}
    result.setdefault("Motor", None)
    result.setdefault("Pohon", None)
    for tr in page.find("div", class_="techParamsRow").find_all("tr"):
        label = clear_text(tr.find("th").text)
        value = clear_text(tr.find("td").text)
        result[label] = value
    return result


@save_attribute_extraction(element="brand")
def __extract_single_brand(page: BeautifulSoup):
    return clear_text(
        page.find("div", id="carCardHead").find("h1").find(text=True, recursive=False).get_text(strip=True,
                                                                                                separator=" "))


@save_attribute_extraction(element="full name")
def __extract_single_full_name(page: BeautifulSoup):
    return clear_text(page.find('div', id="carCardHead").find("h1").text)


@save_attribute_extraction(element="monthly price")
def __extract_single_monthly_price(page: BeautifulSoup):
    if (monthly_price_el := page.find("div", class_="sidebar").find("li", class_="homeDelivery")) is not None:
        if "Výhodné splátky měsíčně od" in monthly_price_el.text:
            return clear_integer(clear_text(monthly_price_el.get_text(strip=True, separator=' ')))
    return None


@save_attribute_extraction(element="special price")
def __extract_single_special_price(page: BeautifulSoup):
    if (special_price_el := page.find("div", class_="sidebar").find("li", class_="infoBoxNavTitle")) is not None:
        if "Akční cena na úvěr" in special_price_el.text:
            return clear_integer(clear_text(special_price_el.get_text(strip=True, separator=' ')))
    return None


@save_attribute_extraction(element="price")
def __extract_single_price(page: BeautifulSoup):
    return clear_integer(clear_text(page.find("div", class_="sidebar").find("ul", class_="infoBoxNav").find(
        lambda tag: tag.name == "span" and "Cena" in tag.text).parent.text.split("Kč")[-2]))


@save_attribute_extraction(element="discount")
def __extract_single_discount(page: BeautifulSoup):
    if (discount_el := page.find(lambda tag: tag.name == "span" and "Tento vůz je zlevněn o" in tag.text)) is not None:
        return clear_integer(clear_text(discount_el.get_text(strip=True, separator=' ')))
    return None

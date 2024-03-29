from __future__ import annotations

import datetime
import re
import uuid
from datetime import datetime

from bs4 import BeautifulSoup, Tag
from common.decorators import save_attribute_extraction
from common.custom_exceptions import CarSoldOutException, AttributeExtractionError
from common.utils import clear_integer, clear_text
from model.esa_entities import EsaCar, EsaCarVariable


def extract_from_list_page(page: BeautifulSoup) -> list[tuple[EsaCar, EsaCarVariable]]:
    result: list[tuple[EsaCar, EsaCarVariable]] = []
    for car in page.find_all("a", class_="car_item"):
        url = car['href']
        image_url = __extract_image_url(car)
        esa_id = __extract_esa_id(url)
        brand = __extract_brand(url)
        # gear = __extract_gear(url)
        equipment_class = __extract_equipment_class(url)
        body = __extract_body(url)
        full_name = __extract_full_name(car)
        # engine = __extract_engine(car)
        year = __extract_year(car)
        power = __extract_power(car)
        fuel = __extract_fuel(car)
        mileage = __extract_mileage(car)
        lowcost = __extract_lowcost(car)
        premium = __extract_premium(car)
        monthly_price = __extract_monthly_price(car)
        special_price = __extract_special_price(car)
        condition = __extract_condition(car)
        price = 0
        discount = __extract_discount(car)

        car_id = uuid.uuid4()
        result.append(
            (EsaCar(
                car_id=car_id,
                url=url,
                image=image_url,
                esa_id=esa_id,
                brand=brand,
                full_name=full_name,
                engine=None,
                equipment_class=equipment_class,
                year=year,
                gear=None,
                power=power,
                fuel=fuel,
                body_type=body,
                mileage=mileage,
                datetime_captured=datetime.now(),
                datetime_sold=None,
                job_id=None
            ),
             EsaCarVariable(
                 car_variable_id=uuid.uuid4(),
                 car_id=car_id,
                 lowcost=lowcost,
                 premium=premium,
                 monthly_price=monthly_price,
                 special_price=special_price,
                 condition=condition,
                 price=price,
                 discount=discount,
                 datetime_captured=datetime.now(),
                 job_id=None
             )
            )
        )
    return result


@save_attribute_extraction(element="image url")
def __extract_image_url(car: Tag):
    return car.find('img', class_="")['src']


@save_attribute_extraction(element="esa id")
def __extract_esa_id(url: str):
    return re.search("^/.+/.+/.+/.+/(.+)", url).group(1)


@save_attribute_extraction(element="brand")
def __extract_brand(url: str):
    return re.search("^/(.+)/.+/.+/.+/.+", url).group(1)


@save_attribute_extraction(element="full name")
def __extract_full_name(car: Tag):
    return car.find('span', class_="car-title").get_text(strip=True, separator=' ')


# @save_attribute_extraction(element="engine")
# def __extract_engine(car: Tag):
#     return car.find('div', class_="icon_power").get_text(strip=True, separator=' ').split("/")[0]


@save_attribute_extraction(element="equipment class")
def __extract_equipment_class(url: str):
    return re.search("^/.+/(.+)/.+/.+/.+", url).group(1)


@save_attribute_extraction(element="year")
def __extract_year(car: Tag):
    return clear_integer(car.find('div', class_="icon_year").get_text(strip=True, separator=' '))


# @save_attribute_extraction(element="gear")
# def __extract_gear(url: str):
#     return re.search("^/.+/.+/.+/(.+)/.+", url).group(1)


@save_attribute_extraction(element="power")
def __extract_power(car: Tag):
    return clear_integer(clear_text(
        car.find('div', class_="icon_power").get_text(strip=True, separator=' ').replace(" kW", "")))


@save_attribute_extraction(element="fuel")
def __extract_fuel(car: Tag):
    return car.find('div', class_="icon_fuel").get_text(strip=True, separator=' ')


@save_attribute_extraction(element="body type")
def __extract_body(url: str):
    return re.search("^/.+/.+/(.+)/.+/.+", url).group(1)


@save_attribute_extraction(element="mileage")
def __extract_mileage(car: Tag):
    return clear_integer(
        clear_text(car.find('div', class_="icon_range").get_text(strip=True, separator=' ').replace(" km", "")))


@save_attribute_extraction(element="lowcost")
def __extract_lowcost(car: Tag):
    return car.find('img', class_="lowcost-icon") is not None


@save_attribute_extraction(element="premium")
def __extract_premium(car: Tag):
    return "PREMIUM" in car.find('div', class_="car-image-tags").get_text(strip=True, separator=' ')


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


@save_attribute_extraction(element="tags")
def __extract_tags(car: Tag):
    return [tag.text for tag in car.find('div', class_="car_item__tags").findAll("div", class_="car_item__tag")]


@save_attribute_extraction(element="condition")
def __extract_condition(car: Tag):
    return len([] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + len(
        [] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i", "fa-star-half-o")) + 0.5


@save_attribute_extraction(element="discount")
def __extract_discount(car: Tag):
    discount = 0
    if (discount_el := car.find('div', class_="car_item__save")) is not None:
        discount_text = re.search(r"Zlevněno o\s*([\s0-9]+)\s*Kč",
                                  re.sub(r"\s+", " ", discount_el.get_text(strip=True, separator=' ')))
        discount = 0 if discount_text is None else int(discount_text.group(1).replace(" ", "").strip())
    return discount


def extract_car_from_page(page: BeautifulSoup) -> tuple[EsaCar, EsaCarVariable]:
    __check_single_if_sold(page)

    url, esa_id, brand, equipment_class = __extract_single_url_data(page)
    image = __extract_single_image_url(page)
    # Full name
    full_name = __extract_single_full_name(page)
    # Monthly price
    monthly_price = __extract_single_monthly_price(page)
    # Action price
    special_price = __extract_single_special_price(page)
    price = __extract_single_price(page)
    discount = __extract_single_discount(page)
    lowcost = page.find('img', class_="lowcost-icon") is not None
    premium = page.find('img', class_="premium-icon") is not None
    condition = __extract_single_condition(page)

    # Detail box
    detail_box = page.find('div', class_="detail_attr_inner")
    year = clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))
    gear = __extract_single_detail_box_element(detail_box, "Převodovka")
    engine = __extract_single_detail_box_element(detail_box, "Motor")
    power = clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))

    fuel = __extract_single_detail_box_element(detail_box, "Palivo")
    mileage = clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))
    car_body = __extract_single_detail_box_element(detail_box, "Karosérie")

    car_id = uuid.uuid4()
    return (
        EsaCar(
            car_id=car_id,
            url=url,
            image=image,
            esa_id=esa_id,
            brand=brand,
            full_name=full_name,
            engine=engine,
            equipment_class=equipment_class,
            year=year,
            gear=gear,
            power=power,
            fuel=fuel,
            body_type=car_body,
            mileage=mileage,
            datetime_captured=datetime.now(),
            datetime_sold=None,
            job_id=None
        ),
        EsaCarVariable(
            car_variable_id=uuid.uuid4(),
            car_id=car_id,
            lowcost=lowcost,
            premium=premium,
            monthly_price=monthly_price,
            special_price=special_price,
            condition=condition,
            price=price,
            discount=discount,
            datetime_captured=datetime.now(),
            job_id=None
        )
    )


def __check_single_if_sold(page: BeautifulSoup):
    if page.find("div", class_="car-not-found") is not None:
        raise CarSoldOutException()


@save_attribute_extraction(element="url data")
def __extract_single_url_data(page: BeautifulSoup):
    if (url_el := page.find("meta", property="og:url")) is not None:
        url = url_el.attrs["content"].replace("http", "").replace("https", "").replace("://www.autoesa.cz", "")
        esa_id = __extract_esa_id(url)
        brand = __extract_brand(url)
        equipment_class = __extract_equipment_class(url)
        return url, esa_id, brand, equipment_class
    raise AttributeExtractionError("Did not find url element.")


@save_attribute_extraction(element="image")
def __extract_single_image_url(page: BeautifulSoup):
    if (image_el := page.find("div", class_="initCarDetailSlider")) is not None and image_el.find("a") is not None:
        return image_el.find("a")['href']
    return "not available"


@save_attribute_extraction(element="full name")
def __extract_single_full_name(page: BeautifulSoup):
    full_name_el = page.find('div', class_="car_detail2__h1")
    return clear_text(full_name_el.text)


@save_attribute_extraction(element="monthly price")
def __extract_single_monthly_price(page: BeautifulSoup):
    monthly_price_el = page.find("div", class_="car_detail2__topline").find(string="Měsíčně od")
    return clear_integer(
        clear_text(monthly_price_el.parent.find_next_sibling("strong").get_text(strip=True, separator=' ')))


@save_attribute_extraction(element="special price")
def __extract_single_special_price(page: BeautifulSoup):
    action_price_el = page.find("div", class_="car_detail2__topline").find(string="Akční cena na úvěr")
    return clear_integer(clear_text(
        action_price_el.parent.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))


@save_attribute_extraction(element="price")
def __extract_single_price(page: BeautifulSoup):
    price_el = page.find("div", class_="car_detail2__topline").find(string="Cena v hotovosti")
    return clear_integer(clear_text(price_el.parent.parent.find("strong").get_text(strip=True, separator=' ')))


@save_attribute_extraction(element="discount")
def __extract_single_discount(page: BeautifulSoup):
    if (discount_el := page.find("span", class_="car_item__save_text")) is not None:
        return clear_integer(clear_text(discount_el.get_text(strip=True, separator=' ')))
    return None


def __extract_single_detail_box_element(detail_box: BeautifulSoup, label: str) -> (str | None):
    try:
        el = detail_box.find(string=label)
        if (el.parent.name != "strong"):
            return clear_text(
                el.find_parent("strong").find_next_sibling("span").get_text(strip=True, separator=' '))
        return clear_text(el.parent.find_next_sibling("span").get_text(strip=True, separator=' '))
    except Exception as e:
        raise AttributeExtractionError(
            f"Issue during extraction detail box data looking for label: {label}, {e.with_traceback(None)}") from e


@save_attribute_extraction(element="condition")
def __extract_single_condition(page: BeautifulSoup):
    return len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + \
        len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star-half-o")) + 0.5


def __extract_data_from_detail_box(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    year = clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))
    gear = __extract_single_detail_box_element(detail_box, "Převodovka")
    engine = __extract_single_detail_box_element(detail_box, "Motor")
    power = clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))

    fuel = __extract_single_detail_box_element(detail_box, "Palivo")
    mileage = clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))
    car_body = __extract_single_detail_box_element(detail_box, "Karosérie")
    return year, gear, engine, power, fuel, mileage, car_body


@save_attribute_extraction(element="year")
def __extract_single_year(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))


@save_attribute_extraction(element="gear")
def __extract_single_gear(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Převodovka")


@save_attribute_extraction(element="engine")
def __extract_single_engine(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Motor")


@save_attribute_extraction(element="power")
def __extract_single_power(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))


@save_attribute_extraction(element="fuel")
def __extract_single_fuel(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Palivo")


@save_attribute_extraction(element="mileage")
def __extract_single_mileage(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))


@save_attribute_extraction(element="car body")
def __extract_single_car_body(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Karosérie")

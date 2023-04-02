import datetime
import re
from bs4 import BeautifulSoup, Tag

from common.Decorators import save_attribute_extraction
from model.EsaCar import EsaCar
from typing import Optional
from datetime import datetime
from common.CustomException import CarSoldOutException, AttributeExtractionError


def extract_from_list_page(page: BeautifulSoup) -> list[EsaCar]:
    result: list[EsaCar] = []
    for car in page.find_all("a", class_="car_item"):
        url = car['href']
        image_url = __extract_image_url(car)
        esa_id = __extract_esa_id(url)
        brand = __extract_brand(url)
        gear = __extract_gear(url)
        equipment_class = __extract_equipment_class(url)
        body = __extract_body(url)
        full_name = __extract_full_name(car)
        engine = __extract_engine(car)
        year = __extract_year(car)
        power = __extract_power(car)
        fuel = __extract_fuel(car)
        mileage = __extract_mileage(car)
        lowcost = __extract_lowcost(car)
        premium = __extract_premium(car)
        monthly_price = __extract_monthly_price(car)
        special_price = __extract_special_price(car)
        tags = __extract_tags(car)
        condition = __extract_condition(car)
        price = 0
        discount = __extract_discount(car)

        result.append(
            EsaCar(url, image_url, esa_id, brand, full_name, engine, equipment_class, year, gear, power, fuel, body,
                   mileage, lowcost, premium, monthly_price, special_price, tags, condition, price, discount,
                   datetime.now(), None))
    return result


def __extract_image_url(car: Tag):
    try:
        return car.find('img', class_="")['src']
    except Exception as e:
        raise AttributeExtractionError("Issue during extraction of image url")


def __extract_esa_id(url: str):
    try:
        return re.search("^/.+/.+/.+/.+/(.+)", url).group(1)
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of esa id, {e.with_traceback(None)}")


def __extract_brand(url: str):
    try:
        return re.search("^/(.+)/.+/.+/.+/.+", url).group(1)
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of brand, {e.with_traceback(None)}")


def __extract_full_name(car: Tag):
    try:
        return car.find('span', class_="car-title").get_text(strip=True, separator=' ')
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of full name, {e.with_traceback(None)}")


def __extract_engine(car: Tag):
    try:
        return car.find('div', class_="icon_power").get_text(strip=True, separator=' ').split("/")[0]
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of full name, {e.with_traceback(None)}")


def __extract_equipment_class(url: str):
    try:
        return re.search("^/.+/(.+)/.+/.+/.+", url).group(1)
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of equipment class, {e.with_traceback(None)}")


def __extract_year(car: Tag):
    try:
        return __clear_integer(car.find('div', class_="icon_year").get_text(strip=True, separator=' '))
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of year, {e.with_traceback(None)}")


def __extract_gear(url: str):
    try:
        return re.search("^/.+/.+/.+/(.+)/.+", url).group(1)
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of gear, {e.with_traceback(None)}")


def __extract_power(car: Tag):
    try:
        return __clear_integer(__clear_text(
            car.find('div', class_="icon_power").get_text(strip=True, separator=' ').replace(" kW", "")))
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of power, {e.with_traceback(None)}")


def __extract_fuel(car: Tag):
    try:
        return car.find('div', class_="icon_fuel").get_text(strip=True, separator=' ')
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of fuel, {e.with_traceback(None)}")


def __extract_body(url: str):
    try:
        return re.search("^/.+/.+/(.+)/.+/.+", url).group(1)
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of body, {e.with_traceback(None)}")


def __extract_mileage(car: Tag):
    try:
        return __clear_integer(
            __clear_text(car.find('div', class_="icon_range").get_text(strip=True, separator=' ').replace(" km", "")))
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of mileage, {e.with_traceback(None)}")


def __extract_lowcost(car: Tag):
    try:
        return car.find('img', class_="lowcost-icon") is not None
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of lowcost, {e.with_traceback(None)}")


def __extract_premium(car: Tag):
    try:
        return "PREMIUM" in car.find('div', class_="car-image-tags").get_text(strip=True, separator=' ')
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of premium, {e.with_traceback(None)}")


def __extract_monthly_price(car: Tag):
    try:
        monthly_price = 0
        if (monthly_price_el := car.find('div', class_="car_item__price_holder").find('div',
                                                                                       "car_item__price_block")) is not None:
            monthly_price_text = re.search("Měsíčně od\s*([\s0-9]+)\s*Kč",
                                           __clear_text(monthly_price_el.get_text(strip=True, separator=' ')))
            monthly_price = 0 if monthly_price_text is None else __clear_integer(
                monthly_price_text.group(1).replace(" ", "").strip())
        return monthly_price
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of monthly price, {e.with_traceback(None)}")


def __extract_special_price(car: Tag):
    try:
        special_price = 0
        if (special_price_el := car.find('div', class_="car_item__price_holder").find('div',
                                                                                       "car_item__price_block text-red")) is not None:
            special_price_text = re.search("Akční cena\s*([\s0-9]+)\s*Kč",
                                           __clear_text(special_price_el.get_text(strip=True, separator=' ')))
            special_price = 0 if special_price_text is None else int(
                special_price_text.group(1).replace(" ", "").strip())
        return special_price
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of special price, {e.with_traceback(None)}")


def __extract_tags(car: Tag):
    try:
        return [tag.text for tag in car.find('div', class_="car_item__tags").findAll("div", class_="car_item__tag")]
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of tags, {e.with_traceback(None)}")


def __extract_condition(car: Tag):
    try:
        return len([] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + len(
            [] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i", "fa-star-half-o")) + 0.5
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of condition, {e.with_traceback(None)}")


def __extract_discount(car: Tag):
    try:
        discount = 0
        if (discount_el := car.find('div', class_="car_item__save")) is not None:
            discount_text = re.search("Zlevněno o\s*([\s0-9]+)\s*Kč",
                                      re.sub("\s+", " ", discount_el.get_text(strip=True, separator=' ')))
            discount = 0 if discount_text is None else int(discount_text.group(1).replace(" ", "").strip())
        return discount
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction of discount, {e.with_traceback(None)}")


def extract_car_from_page(page: BeautifulSoup) -> EsaCar:
    url = esa_id = brand = equipment_class = image = full_name = monthly_price = special_price = price = discount = None

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
    year = __clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))
    gear = __extract_single_detail_box_element(detail_box, "Převodovka")
    engine = __extract_single_detail_box_element(detail_box, "Motor")
    power = __clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))

    fuel = __extract_single_detail_box_element(detail_box, "Palivo")
    mileage = __clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))
    car_body = __extract_single_detail_box_element(detail_box, "Karosérie")

    return EsaCar(url, image, esa_id, brand, full_name, engine, equipment_class, year, gear, power, fuel, car_body,
                  mileage, lowcost, premium, monthly_price, special_price, [], condition, price, discount,
                  datetime.now(), None)

def __check_single_if_sold(page: BeautifulSoup):
    if page.find("div", class_="car-not-found") is not None:
        raise CarSoldOutException()

@save_attribute_extraction(element="url data")
def __extract_single_url_data(page: BeautifulSoup):
    if (url_el := page.find("meta", property="og:url")) is not None:
        url = url_el.attrs["content"].replace("https://www.autoesa.cz", "")
        esa_id = __extract_esa_id(url)
        brand = __extract_brand(url)
        equipment_class = __extract_equipment_class(url)
        return url, esa_id, brand, equipment_class
    else:
        raise AttributeExtractionError("Did not find url element.")

@save_attribute_extraction(element="image")
def __extract_single_image_url(page: BeautifulSoup):
    if (image_el := page.find("div", class_="initCarDetailSlider")) is not None and image_el.find("a") is not None:
        return image_el.find("a")['href']
    else:
        "not available"

@save_attribute_extraction(element="full name")
def __extract_single_full_name(page: BeautifulSoup):
    if (full_name_el := page.find('div', class_="car_detail2__h1")) is not None:
        return __clear_text(full_name_el.text)
    else:
        raise AttributeExtractionError("Did not find full name element.")

@save_attribute_extraction(element="monthly price")
def __extract_single_monthly_price(page: BeautifulSoup):
    if (monthly_price_el := page.find("div", class_="car_detail2__topline").find(string="Měsíčně od")) is not None:
        return __clear_integer(
            __clear_text(monthly_price_el.parent.find_next_sibling("strong").get_text(strip=True, separator=' ')))
    else:
        raise AttributeExtractionError("Did not find monthly price element.")

@save_attribute_extraction(element="special price")
def __extract_single_special_price(page: BeautifulSoup):
    if (action_price_el := page.find("div", class_="car_detail2__topline").find(string="Akční cena na úvěr")) is not None:
        return __clear_integer(
            __clear_text(
                action_price_el.parent.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))
    else:
        raise AttributeExtractionError("Did not find special price element.")

@save_attribute_extraction(element="price")
def __extract_single_price(page: BeautifulSoup):
    if (price_el := page.find("div", class_="car_detail2__topline").find(string="Cena v hotovosti")) is not None:
        return __clear_integer(__clear_text(price_el.parent.parent.find("strong").get_text(strip=True, separator=' ')))
    else:
        raise AttributeExtractionError("Did not find price element.")

@save_attribute_extraction(element="discount")
def __extract_single_discount(page: BeautifulSoup):
    if (discount_el := page.find("span", class_="car_item__save_text")) is not None:
        return __clear_integer(__clear_text(discount_el.get_text(strip=True, separator=' ')))
    else:
        return None

def __extract_single_detail_box_element(detail_box: BeautifulSoup, label: str) -> Optional[str]:
    try:
        if (el := detail_box.find(string=label)) is not None:
            if(el.parent.name != "strong"):
                 return __clear_text(el.find_parent("strong").find_next_sibling("span").get_text(strip=True, separator=' '))
            else:
                return __clear_text(el.parent.find_next_sibling("span").get_text(strip=True, separator=' '))
        else:
            raise AttributeExtractionError("Did not find detail box element.")
    except Exception as e:
        raise AttributeExtractionError(f"Issue during extraction detail box data looking for label: {label}, {e.with_traceback(None)}")

@save_attribute_extraction(element="condition")
def __extract_single_condition(page: BeautifulSoup):
    return len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + \
            len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star-half-o")) + 0.5

def __extract_data_from_detail_box(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    year = __clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))
    gear = __extract_single_detail_box_element(detail_box, "Převodovka")
    engine = __extract_single_detail_box_element(detail_box, "Motor")
    power = __clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))

    fuel = __extract_single_detail_box_element(detail_box, "Palivo")
    mileage = __clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))
    car_body = __extract_single_detail_box_element(detail_box, "Karosérie")
    return year, gear, engine, power, fuel, mileage, car_body

@save_attribute_extraction(element="year")
def __extract_single_year(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __clear_integer(__extract_single_detail_box_element(detail_box, "Rok"))

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
    return __clear_integer(__extract_single_detail_box_element(detail_box, "Výkon"))

@save_attribute_extraction(element="fuel")
def __extract_single_fuel(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Palivo")

@save_attribute_extraction(element="mileage")
def __extract_single_mileage(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __clear_integer(__extract_single_detail_box_element(detail_box, "Stav tachometru"))

@save_attribute_extraction(element="car body")
def __extract_single_car_body(page: BeautifulSoup):
    detail_box = page.find('div', class_="detail_attr_inner")
    return __extract_single_detail_box_element(detail_box, "Karosérie")


def __clear_text(text: str) -> str:
    return re.sub("\s+", " ", text).strip()


def __clear_integer(text_with_number: str) -> int:
    return int(re.sub("\D", "", text_with_number))

import datetime
import re
from bs4 import BeautifulSoup, Tag
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

    if page.find("div", class_="car-not-found") is not None:
        raise CarSoldOutException()

    if (url_el := page.find("meta", property="og:url")) is not None:
        url = url_el.attrs["content"].replace("https://www.autoesa.cz", "")
        esa_id = __extract_esa_id(url)
        brand = __extract_brand(url)
        equipment_class = __extract_equipment_class(url)

    if (image_el := page.find("div", class_="initCarDetailSlider")) is not None:
        image = image_el.find("a")['href']

    # Full name
    if (full_name_el := page.find('div', class_="car_detail2__h1")) is not None:
        full_name = __clear_text(full_name_el.text)

    # Monthly price
    if (monthly_price_el := page.find("div", class_="car_detail2__topline").find(string="Měsíčně od")) is not None:
        monthly_price = __clear_integer(
            __clear_text(monthly_price_el.parent.find_next_sibling("strong").get_text(strip=True, separator=' ')))

    # Action price
    if (action_price_el := page.find("div", class_="car_detail2__topline").find(
                string="Akční cena na úvěr")) is not None:
        special_price = __clear_integer(
            __clear_text(action_price_el.parent.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))

    # # Price of new car
    # if (new_car_price_el := page.find("div", class_="car_detail2__topline").find(
    #             string="Cena nového vozu")) is not None:
    #     new_car_price = __clear_integer(
    #         __clear_text(new_car_price_el.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))

    # Price in cash and discount
    if (price_el := page.find("div", class_="car_detail2__topline").find(string="Cena v hotovosti")) is not None:
        price = __clear_integer(
            __clear_text(price_el.parent.parent.find("strong").get_text(strip=True, separator=' ')))

    if (discount_el := page.find("span", class_="car_item__save_text")) is not None:
        discount = __clear_integer(__clear_text(discount_el.get_text(strip=True, separator=' ')))

    lowcost = page.find('img', class_="lowcost-icon") is not None
    premium = page.find('img', class_="premium-icon") is not None

    condition = len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + \
                len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i",
                                                                                                 "fa-star-half-o")) + 0.5

    # Detail box
    detail_box = page.find('div', class_="detail_attr_inner")
    year = __clear_integer(__extract_detail_box_element(detail_box, "Rok"))
    gear = __extract_detail_box_element(detail_box, "Převodovka")
    engine = __extract_detail_box_element(detail_box, "Motor")
    # color = __extract_detail_box_element(detail_box, "Barva")
    power = __clear_integer(__extract_detail_box_element(detail_box, "Výkon"))

    # if (consumption_caption := __extract_detail_box_element(detail_box, "Spotřeba paliva")) is not None:
    #     consumption_out = consumption_caption.split(" / ")[0]
    #     consumption_city = consumption_caption.split(" / ")[1]
    #     consumption_mixed = consumption_caption.split(" / ")[2]

    fuel = __extract_detail_box_element(detail_box, "Palivo")
    mileage = __clear_integer(__extract_detail_box_element(detail_box, "Stav tachometru"))
    # num_of_doors = __clear_integer(__extract_detail_box_element(detail_box, "Počet dveří"))
    car_body = __extract_detail_box_element(detail_box, "Karosérie")
    # wheel_drive = __extract_detail_box_element(detail_box, "Pohon")
    # stk = __extract_detail_box_element(detail_box, "STK")

    return EsaCar(url, image, esa_id, brand, full_name, engine, equipment_class, year, gear, power, fuel, car_body,
                  mileage, lowcost, premium, monthly_price, special_price, [], condition, price, discount,
                  datetime.now(), None)


def __extract_detail_box_element(detail_box: BeautifulSoup, label: str) -> Optional[str]:
    if (el := detail_box.find(string=label)) is not None:
        return __clear_text(el.parent.find_next_sibling("span").get_text(strip=True, separator=' '))
    else:
        return None


def __clear_text(text: str) -> str:
    return re.sub("\s+", " ", text).strip()


def __clear_integer(text_with_number: str) -> int:
    return int(re.sub("\D", "", text_with_number))

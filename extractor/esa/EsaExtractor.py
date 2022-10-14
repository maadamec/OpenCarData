import datetime
import re
from bs4 import BeautifulSoup
from model.EsaCar import EsaCar
from typing import Optional
from datetime import datetime


def extract_from_list_page(page: BeautifulSoup) -> list[EsaCar]:
    result: list[EsaCar] = []
    for car in page.find_all("a", class_="car_item"):
        url = car['href']
        image_url = car.find('img', class_="")['src']
        esa_id = re.search("^/.+/.+/.+/.+/(.+)", url).group(1)
        brand = re.search("^/(.+)/.+/.+/.+/.+", url).group(1)
        full_name = car.find('span', class_="car-title").get_text(strip=True, separator=' ')
        engine = car.find('div', class_="icon_power").get_text(strip=True, separator=' ').split("/")[0]
        equipment_class = re.search("^/.+/(.+)/.+/.+/.+", url).group(1)
        year = __clear_integer(car.find('div', class_="icon_year").get_text(strip=True, separator=' '))
        gear = car.find('div', class_="icon_gear").get_text(strip=True, separator=' ')
        power = __clear_integer(__clear_text(car.find('div', class_="icon_power").get_text(strip=True, separator=' ').split("/")[1].replace(" kW", "")))
        fuel = car.find('div', class_="icon_fuel").get_text(strip=True, separator=' ')
        body = car.find('div', class_="icon_type").get_text(strip=True, separator=' ')
        mileage = __clear_integer(__clear_text(car.find('div', class_="icon_range").get_text(strip=True, separator=' ').replace(" km", "")))
        lowcost = car.find('img', class_="lowcost-icon") is not None
        premium = car.find('img', class_="premium-icon") is not None

        monthly_price = 0
        if (monthly_price_el := car.find('div', class_="car_item__price_holder2").find('div',
                                                                                       "car_item__price_block")) is not None:
            monthly_price_text = re.search("Měsíčně od\s*([\s0-9]+)\s*Kč", __clear_text(monthly_price_el.get_text(strip=True, separator=' ')))
            monthly_price = 0 if monthly_price_text is None else __clear_integer(monthly_price_text.group(1).replace(" ", "").strip())

        special_price = 0
        if (special_price_el := car.find('div', class_="car_item__price_holder2").find('div',
                                                                                       "car_item__price_block text-red")) is not None:
            special_price_text = re.search("Akční cena\s*([\s0-9]+)\s*Kč", __clear_text(special_price_el.get_text(strip=True, separator=' ')))
            special_price = 0 if special_price_text is None else int(special_price_text.group(1).replace(" ", "").strip())

        tags = [tag.text for tag in car.find('div', class_="car_item__tags").findAll("div", class_="car_item__tag")]
        condition = len([] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + \
                    len([] if (stars := car.find('div', class_="stars")) is None else stars.findAll("i",
                                                                                                    "fa-star-half-o")) + 0.5

        price = 0
        discount = 0
        if (discount_el := car.find('div', class_="car_item__save")) is not None:
            discount_text = re.search("Zlevněno o\s*([\s0-9]+)\s*Kč", re.sub("\s+", " ", discount_el.get_text(strip=True, separator=' ')))
            discount = 0 if discount_text is None else int(discount_text.group(1).replace(" ", "").strip())
        result.append(EsaCar(url, image_url, esa_id, brand, full_name, engine, equipment_class, year, gear, power, fuel, body,
                             mileage, lowcost, premium, monthly_price, special_price, tags, condition, price, discount, datetime.now()))
    return result


def extract_car_from_page(page: BeautifulSoup) -> EsaCar:

    if (url_el := page.find("meta", property="og:url")) is not None:
        url = url_el.attrs["content"].replace("https://www.autoesa.cz", "")
        esa_id = re.search(".*/.+/.+/.+/.+/(.+)", url).group(1)
        brand = re.search(".*/(.+)/.+/.+/.+/.+", url).group(1)
        equipment_class = re.search(".*/.+/(.+)/.+/.+/.+", url).group(1)

    if (image_el := page.find("div", class_="slick-current")) is not None:
        image = image_el.find("a")['href']

    # Full name
    if (full_name_el := page.find('div', class_="car_detail2__h1")) is not None:
        full_name = __clear_text(full_name_el.text)

    # Monthly price
    if (monthly_price_el := page.find("div", class_="car_detail2__topline").find(string="Měsíčně od")) is not None:
        monthly_price = __clear_integer(__clear_text(monthly_price_el.parent.find_next_sibling("strong").get_text(strip=True, separator=' ')))

    # Action price
    if (action_price_el := page.find("div", class_="car_detail2__topline").find(string="Akční cena na úvěr")) is not None:
        special_price = __clear_integer(__clear_text(action_price_el.parent.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))

    # Price of new car
    if (new_car_price_el := page.find("div", class_="car_detail2__bottomline").find(string="Cena nového vozu")) is not None:
        new_car_price = __clear_integer(__clear_text(new_car_price_el.parent.find_next_sibling("span").get_text(strip=True, separator=' ')))

    # Price in cash and discount
    if (price_el := page.find("div", class_="car_detail2__bottomline").find(string="Cena v hotovosti")) is not None:
        price = __clear_integer(__clear_text(price_el.parent.find_next_sibling("strong").get_text(strip=True, separator=' ')))
        discount = __clear_integer(__clear_text(price_el.parent.find_next_sibling("span", class_="text-color-blue").get_text(strip=True, separator=' ')))

    lowcost = page.find('img', class_="lowcost-icon") is not None
    premium = page.find('img', class_="premium-icon") is not None

    condition = len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star")) + \
                len([] if (stars := page.find('div', class_="stars")) is None else stars.findAll("i", "fa-star-half-o")) + 0.5

                                                                                                # Detail box
    detail_box = page.find('div', class_="detail_attr_inner")
    year = __clear_integer(__extract_detail_box_element(detail_box, "Rok"))
    gear = __extract_detail_box_element(detail_box, "Převodovka")
    engine = __extract_detail_box_element(detail_box, "Motor")
    color = __extract_detail_box_element(detail_box, "Barva")
    power = __clear_integer(__extract_detail_box_element(detail_box, "Výkon"))

    if (consumption_caption := __extract_detail_box_element(detail_box, "Spotřeba paliva")) is not None:
        consumption_out = consumption_caption.split(" / ")[0]
        consumption_city = consumption_caption.split(" / ")[1]
        consumption_mixed = consumption_caption.split(" / ")[2]

    fuel = __extract_detail_box_element(detail_box, "Palivo")
    mileage = __clear_integer(__extract_detail_box_element(detail_box, "Stav tach."))
    num_of_doors = __clear_integer(__extract_detail_box_element(detail_box, "Počet dveří"))
    car_body = __extract_detail_box_element(detail_box, "Karosérie")
    wheel_drive = __extract_detail_box_element(detail_box, "Pohon")
    stk = __extract_detail_box_element(detail_box, "STK")

    return EsaCar(url, image, esa_id, brand, full_name, engine, equipment_class, year, gear, power, fuel, car_body, mileage, lowcost, premium, monthly_price, special_price, [] ,condition, price, discount, datetime.now())

def __extract_detail_box_element(detail_box: BeautifulSoup, label: str) -> Optional[str]:
    if (el := detail_box.find(string=label)) is not None:
        return __clear_text(el.parent.find_next_sibling("span").get_text(strip=True, separator=' '))
    else:
        return None


def __clear_text(text: str) -> str:
    return re.sub("\s+", " ", text).strip()


def __clear_integer(text_with_number: str) -> int:
    return int(re.sub("\D", "", text_with_number))

import logging
from unittest import TestCase

from normalizer.normalizer import Norm


class Test(TestCase):

    def test_normalize_url_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            logger = logging.getLogger()
            logger.warning("Dummy warning")

            Norm.URL("/peugeot/partner/mpv/benzin/909276887")
            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

    def test_normalize_url_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.URL(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_url. Expected: str, Got: <class 'int'>"]
            )

    def test_normalize_url_starting_with_slash(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            url = 'https://www.aaaauto.cz/cz/skoda-superb/car.html?id=547359742#limit=48'
            Norm.URL(url)

            # Then
            self.assertEqual(
                cm.output,
                [f"WARNING:normalizer:Url does not start with '/', Got: {url}"]
            )

    def test_normalize_price_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.PRICE(100000)
            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

    def test_normalize_price_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.PRICE("100000")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_price. Expected: int, Got: <class 'str'>"]
            )

    def test_normalize_price_negative(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.PRICE(-100000)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Price is negative, Got: -100000"]
            )

    def test_normalize_price_too_high(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.PRICE(5000000)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Price is too high, Got: 5000000"]
            )

    def test_normalize_image_url_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.IMAGE_URL("https://cdn.aaaauto.cz/external/autoweb/1000x700/")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

    def test_normalize_image_url_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.IMAGE_URL(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_image_url. Expected: str, Got: <class 'int'>"]
            )

    def test_normalize_image_url_starting_with_https(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            url = 'http://cdn.aaaauto.cz/external/autoweb/1000x700/'
            Norm.IMAGE_URL(url)

            # Then
            self.assertEqual(
                cm.output,
                [f"WARNING:normalizer:Image url does not start with 'https://', Got: {url}"]
            )

    def test_normalize_reseller_id_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.RESELLER_ID('1')

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

    def test_normalize_reseller_id_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.RESELLER_ID(1)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_reseller_id. Expected: str, Got: <class 'int'>"]
            )

    def test_normalize_reseller_id_not_number(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.RESELLER_ID("a")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Reseller id is not a number, Got: a"]
            )

    def test_normalize_normalize_brand_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.BRAND("Peugeot")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

    def test_normalize_brand_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            Norm.BRAND(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_brand. Expected: str, Got: <class 'int'>"]
            )

    def test_normalize_brand_mapping_peugeot(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_brand = Norm.BRAND("peugeot")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_brand, "Peugeot")

    def test_normalize_brand_mapping_citroen(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_brand = Norm.BRAND("citroen")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_brand, "Citroen")

    def test_normalize_brand_mapping_mercedes(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_brand = Norm.BRAND("mercedes benz")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_brand, "Mercedes-Benz")

    def test_normalize_brand_mapping_unknown(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_brand = Norm.BRAND("unknown")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Brand not found in mapping, Got: unknown"]
            )

            self.assertEqual(normalized_brand, "unknown")

    def test_normalize_gear_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_gear = Norm.GEAR("manual")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_gear, "Manual")

    def test_normalize_gear_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_gear = Norm.GEAR(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_gear. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_gear, 5)

    def test_normalize_gear_mapping_unknown(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_gear = Norm.GEAR("unknown")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Gear not found in mapping, Got: unknown"]
            )

            self.assertEqual(normalized_gear, "unknown")

    def test_normalize_full_name_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_full_name = Norm.FULL_NAME("Peugeot 308 SW 1.6 HDi 80 kW, r.v. 2009")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_full_name, "Peugeot 308 SW 1.6 HDi 80 kW, r.v. 2009")

    def test_normalize_full_name_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_full_name = Norm.FULL_NAME(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_full_name. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_full_name, 5)

    def test_normalize_engine_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_engine = Norm.ENGINE("1.6 HDi")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_engine, "1.6 HDi")

    def test_normalize_engine_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_engine = Norm.ENGINE(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_engine. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_engine, 5)

    def test_normalize_year_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_year = Norm.YEAR(2009)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_year, 2009)

    def test_normalize_year_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_year = Norm.YEAR("2009")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_year. Expected: int, Got: <class 'str'>"]
            )

            self.assertEqual(normalized_year, "2009")

    def test_normalize_year_max_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_year = Norm.YEAR(3000)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Year is too high, Got: 3000"]
            )

            self.assertEqual(normalized_year, 3000)

    def test_normalize_year_min_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_year = Norm.YEAR(1000)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Year is too low, Got: 1000"]
            )

            self.assertEqual(normalized_year, 1000)

    def test_normalize_power_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_power = Norm.POWER(80)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_power, 80)

    def test_normalize_power_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_power = Norm.POWER("80")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_power. Expected: int, Got: <class 'str'>"]
            )

            self.assertEqual(normalized_power, "80")

    def test_normalize_power_max_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_power = Norm.POWER(1001)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Power is too high, Got: 1001"]
            )

            self.assertEqual(normalized_power, 1001)

    def test_normalize_power_min_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_power = Norm.POWER(-1)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Power is negative, Got: -1"]
            )

            self.assertEqual(normalized_power, -1)

    def test_normalize_fuel_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_fuel = Norm.FUEL("Diesel")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_fuel, "Diesel")

    def test_normalize_fuel_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_fuel = Norm.FUEL(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_fuel. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_fuel, 5)

    def test_normalize_fuel_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_fuel = Norm.FUEL("nafta")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_fuel, "Diesel")

    def test_normalize_mileage_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_mileage = Norm.MILEAGE(100000)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_mileage, 100000)

    def test_normalize_mileage_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_mileage = Norm.MILEAGE("100000")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_mileage. Expected: int, Got: <class 'str'>"]
            )

            self.assertEqual(normalized_mileage, "100000")

    def test_normalize_mileage_max_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_mileage = Norm.MILEAGE(2000001)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Mileage is too high, Got: 2000001"]
            )

            self.assertEqual(normalized_mileage, 2000001)

    def test_normalize_mileage_min_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_mileage = Norm.MILEAGE(-1)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Mileage is negative, Got: -1"]
            )

            self.assertEqual(normalized_mileage, -1)

    def test_normalize_equipment_class_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_equipment_class = Norm.EQUIPMENT_CLASS("Superb")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_equipment_class, "Superb")

    def test_normalize_equipment_class_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_equipment_class = Norm.EQUIPMENT_CLASS(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_equipment_class. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_equipment_class, 5)

    def test_normalize_body_type_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_body_type = Norm.BODY_TYPE("Combi")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_body_type, "Combi")

    def test_normalize_body_type_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_body_type = Norm.BODY_TYPE("kombi")

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_body_type, "Combi")

    def test_normalize_body_type_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_body_type = Norm.BODY_TYPE(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_body_type. Expected: str, Got: <class 'int'>"]
            )

            self.assertEqual(normalized_body_type, 5)

    def test_normalize_condition_success(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION(1)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_condition, 1)

    def test_normalize_condition_success_mid(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION(0.5)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_condition, 0.5)

    def test_normalize_condition_success_min(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION(0)

            logger = logging.getLogger()
            logger.warning("Dummy warning")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:root:Dummy warning"]
            )

            self.assertEqual(normalized_condition, 0)

    def test_normalize_condition_type(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION("1")

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Unexpected type passed to normalize_condition. Expected: float | int, Got: <class 'str'>"]
            )

            self.assertEqual(normalized_condition, "1")

    def test_normalize_condition_max_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION(5)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Condition is too high, Got: 5"]
            )

            self.assertEqual(normalized_condition, 5)

    def test_normalize_condition_min_value(self):
        with self.assertLogs(level='WARN') as cm:
            # When
            normalized_condition = Norm.CONDITION(-1)

            # Then
            self.assertEqual(
                cm.output,
                ["WARNING:normalizer:Condition is negative, Got: -1"]
            )

            self.assertEqual(normalized_condition, -1)




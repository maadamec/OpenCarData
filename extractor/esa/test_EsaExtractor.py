from unittest import TestCase
from bs4 import BeautifulSoup
from extractor.esa.EsaExtractor import extract_from_list_page, extract_car_from_page
from model.EsaCar import EsaCar


class Test(TestCase):
    def test_extract_from_page(self):
        with open("../../testData/testlist.html", encoding="utf-8") as fp:
            page = BeautifulSoup(fp, 'html.parser')
            try:
                result: list[EsaCar] = extract_from_list_page(page)
                print(result[0])
                self.assertEqual(len(result), 10)
                first_car = result[0]
                self.assertEqual('/skoda/citigo/hatchback/elektro/861263085', first_car.url)
                self.assertEqual('/files/cars/861263085/950_713_e/861263085-1.jpg', first_car.image)
                self.assertEqual('skoda', first_car.brand)
                self.assertEqual('Škoda Citigo Elektro Style Plus IV', first_car.full_name)
                self.assertEqual('citigo', first_car.equipment_class)
                self.assertEqual(2020, first_car.year)
                self.assertEqual('elektro', first_car.gear)
                self.assertEqual(61, first_car.power)
                self.assertEqual('elektro', first_car.fuel)
                self.assertEqual('hatchback', first_car.body_type)
                self.assertEqual(13, first_car.mileage)
                self.assertEqual(False, first_car.lowcost)
                self.assertEqual(True, first_car.premium)
                self.assertEqual(1978, first_car.monthly_price)
                self.assertEqual(515000, first_car.special_price)
                self.assertEqual(['servisní kniha', 'zánovní vůz'], first_car.tags)
                self.assertAlmostEqual(0.5, first_car.condition, delta=0.01)
                self.assertEqual(0, first_car.price)
                self.assertEqual(0, first_car.discount)

                self.assertTrue(result[1].premium)
                self.assertFalse(result[1].lowcost)

                self.assertFalse(result[3].premium)
                self.assertFalse(result[3].lowcost)

            except Exception as e:
                self.fail()

    def test_extract_car_from_page(self):
        with open("../../testData/testcar.html", encoding="utf-8") as fp:
            page = BeautifulSoup(fp, 'html.parser')
            try:
                first_car: EsaCar = extract_car_from_page(page)
                self.assertIsNotNone(first_car)
                self.assertEqual("861263085", first_car.esa_id)
                self.assertEqual("/skoda/citigo/hatchback/elektro/861263085", first_car.url)
                self.assertEqual('/files/cars/861263085/861263085-1.jpg', first_car.image)
                self.assertEqual('skoda', first_car.brand)
                self.assertEqual('Škoda Citigo Elektro Style Plus IV', first_car.full_name)
                self.assertEqual('Elektro', first_car.engine)
                self.assertEqual('citigo', first_car.equipment_class)
                self.assertEqual(2020, first_car.year)
                self.assertEqual('automat', first_car.gear)
                self.assertEqual(61, first_car.power)
                self.assertEqual('elektro', first_car.fuel)
                self.assertEqual('hatchback', first_car.body_type)
                self.assertEqual(13, first_car.mileage)
                self.assertEqual(False, first_car.lowcost)
                self.assertEqual(True, first_car.premium)
                self.assertEqual(1978, first_car.monthly_price)
                self.assertEqual(515000, first_car.special_price)
                self.assertEqual([], first_car.tags)
                self.assertAlmostEqual(7.5, first_car.condition, delta=0.01)
                self.assertEqual(565000, first_car.price)
                self.assertEqual(35000, first_car.discount)

            except Exception as e:
                self.fail()

            with open("../../testData/testcar2.html", encoding="utf-8") as fp:
                page = BeautifulSoup(fp, 'html.parser')
                try:
                    first_car: EsaCar = extract_car_from_page(page)
                    self.assertIsNotNone(first_car)
                    self.assertEqual("305241218", first_car.esa_id)
                    self.assertEqual("/opel/astra/kombi/benzin/305241218", first_car.url)
                    self.assertEqual('/files/cars/305241218/305241218-1.jpg', first_car.image)
                    self.assertEqual('opel', first_car.brand)
                    self.assertEqual('Opel Astra 1.6 16V', first_car.full_name)
                    self.assertEqual('1.6 16V', first_car.engine)
                    self.assertEqual('astra', first_car.equipment_class)
                    self.assertEqual(2012, first_car.year)
                    self.assertEqual('manual/5', first_car.gear)
                    self.assertEqual(85, first_car.power)
                    self.assertEqual('benzín', first_car.fuel)
                    self.assertEqual('kombi', first_car.body_type)
                    self.assertEqual(278536, first_car.mileage)
                    self.assertEqual(False, first_car.lowcost)
                    self.assertEqual(False, first_car.premium)
                    self.assertEqual(361, first_car.monthly_price)
                    self.assertEqual(75000, first_car.special_price)
                    self.assertEqual([], first_car.tags)
                    self.assertAlmostEqual(7.5, first_car.condition, delta=0.01)
                    self.assertEqual(100000, first_car.price)
                    self.assertEqual(15000, first_car.discount)

                except Exception as e:
                    self.fail()

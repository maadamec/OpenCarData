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
                self.assertEqual("/skoda/octavia/liftback/benzin/261228219", first_car.url)
                self.assertEqual('/files/cars/261228219/800_496_e/261228219-1.jpg', first_car.image)
                self.assertEqual('skoda', first_car.brand)
                self.assertEqual('Škoda Octavia II 1.2 TSI Elegance', first_car.full_name)
                self.assertEqual('1.2 TSI', first_car.engine)
                self.assertEqual('octavia', first_car.equipment_class)
                self.assertEqual(2011, first_car.year)
                self.assertEqual('automat/6', first_car.gear)
                self.assertEqual(77, first_car.power)
                self.assertEqual('benzín', first_car.fuel)
                self.assertEqual('liftback', first_car.body_type)
                self.assertEqual(90921, first_car.mileage)
                self.assertEqual(False, first_car.lowcost)
                self.assertEqual(False, first_car.premium)
                self.assertEqual(613, first_car.monthly_price)
                self.assertEqual(130000, first_car.special_price)
                self.assertEqual(['servisní kniha'], first_car.tags)
                self.assertAlmostEqual(7.5, first_car.condition, delta=0.01)
                self.assertEqual(0, first_car.price)
                self.assertEqual(48000, first_car.discount)

                self.assertTrue(result[1].premium)
                self.assertFalse(result[1].lowcost)

                self.assertFalse(result[2].premium)
                self.assertTrue(result[2].lowcost)

            except Exception as e:
                self.fail()

    def test_extract_car_from_page(self):
        with open("../../testData/testcar.html", encoding="utf-8") as fp:
            page = BeautifulSoup(fp, 'html.parser')
            try:
                first_car: EsaCar = extract_car_from_page(page)
                self.assertIsNotNone(first_car)
                self.assertEqual("205250228", first_car.esa_id)
                self.assertEqual("/mitsubishi/outlander/suv/hybridni/205250228", first_car.url)
                self.assertEqual('/files/cars/205250228/205250228-1.jpg', first_car.image)
                self.assertEqual('mitsubishi', first_car.brand)
                self.assertEqual('Mitsubishi Outlander 2.4PHEV Instyle 4x4', first_car.full_name)
                self.assertEqual('2.4PHEV PHEV', first_car.engine)
                self.assertEqual('outlander', first_car.equipment_class)
                self.assertEqual(2020, first_car.year)
                self.assertEqual('automat', first_car.gear)
                self.assertEqual(99, first_car.power)
                self.assertEqual('hybridní', first_car.fuel)
                self.assertEqual('SUV', first_car.body_type)
                self.assertEqual(43712, first_car.mileage)
                self.assertEqual(False, first_car.lowcost)
                self.assertEqual(True, first_car.premium)
                self.assertEqual(2660, first_car.monthly_price)
                self.assertEqual(710000, first_car.special_price)
                self.assertEqual([], first_car.tags)
                self.assertAlmostEqual(7.5, first_car.condition, delta=0.01)
                self.assertEqual(760000, first_car.price)
                self.assertEqual(420000, first_car.discount)

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

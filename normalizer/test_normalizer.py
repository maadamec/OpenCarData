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
                ["WARNING:normalizer:Unexpected type passed to __normalize_url. Expected: str, Got: <class 'int'>"]
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

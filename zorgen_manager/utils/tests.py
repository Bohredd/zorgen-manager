from django.test import SimpleTestCase
from zorgen_manager.utils.decimal import currency_format
from decimal import Decimal


class UtilsTest(SimpleTestCase):
    def test_currency_format(self):
        """A função currency_format não deve arredondar para cima condicionalmente"""
        self.assertEqual(
            "123,34",
            currency_format(123.349, arredondar=False),
        )
        self.assertEqual(
            "123,35",
            currency_format(123.349),
        )
        self.assertEqual("123,34", currency_format(Decimal(123.349), arredondar=False))
        self.assertEqual("123,35", currency_format(Decimal(123.34987)))

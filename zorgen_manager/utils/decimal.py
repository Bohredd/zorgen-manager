from decimal import ROUND_DOWN, Decimal
import locale
import math


def reduce_decimal_places(number, places):
    # Create a Decimal object from the number
    decimal_number = Decimal(str(number))

    # Set the desired number of decimal places
    decimal_places = Decimal(10) ** (-places)

    # Reduce the decimal places using quantize with ROUND_DOWN
    reduced_decimal = decimal_number.quantize(decimal_places, rounding=ROUND_DOWN)

    return reduced_decimal


def arredondar_valor(f, n):
    return math.floor(f * 10**n) / 10**n


def currency_format(value, arredondar=True) -> str:
    """
    formata um número para uma string no formato da moeda brasileira

    # value [Decimal | float]
    """

    if value:
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        value = locale.currency(
            arredondar_valor(value, 2) if not arredondar else value,
            grouping=True,
            symbol=False,
        )
    return value

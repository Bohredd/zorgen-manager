import re
import decimal
from localflavor.br.validators import (
    BRCPFValidator,
    BRCNPJValidator,
    cpf_digits_re,
    cnpj_digits_re,
)
from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def widget_attrs(self, widget: forms.Widget):
        return {**super().widget_attrs(widget), "multiple": "true"}

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MaskedInput(forms.TextInput):
    """
    ATENÇÃO: adicione jquery no template!
    Não está sendo incluido pois pode impedir funcionamento de outras funcionalidades como selec2
    """

    class Media:
        js = (
            "hcc_lib_integra/inputmask/jquery.inputmask.min.js",
            "hcc_lib_integra/inputmask/bindings/inputmask.binding.js",
            "hcc_lib_integra/maskMoney/jquery.maskMoney.min.js",
        )

    def __init__(self, mask: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["data-inputmask"] = f"'mask': {mask}"


class BRCPFValidatorCustom(BRCPFValidator):
    """Validador com mensagem traduzida"""

    def __init__(self, *args, **kwargs):
        super(BRCPFValidator, self).__init__(
            *args, regex=cpf_digits_re, message="Número de CPF inválido", **kwargs
        )


class BRCNPJValidatorCustom(BRCNPJValidator):
    """Validador com mensagem traduzida"""

    def __init__(self, *args, **kwargs):
        super(BRCNPJValidator, self).__init__(
            *args, regex=cnpj_digits_re, message="Número de CNPJ inválido", **kwargs
        )


def extrair_somente_numeros(valor: str):
    return re.sub(r"\D", "", valor or "")


class SomenteDigitosMixin:
    def to_python(self, value):
        return extrair_somente_numeros(value)


class MoedaField(forms.Field):
    """
    ATENÇÃO: adicione well mask money no template base
    """

    def __init__(
        self,
        locales="pt-br",
        currency="BRL",
        allow_empty=True,
        allow_netative=True,
        decimal_places=2,
        use_currency_symbol=True,
        is_decimal=False,
        *args,
        **kwargs,
    ):
        (
            self.locales,
            self.currency,
            self.allow_empty,
            self.allow_netative,
            self.decimal_places,
            self.use_currency_symbol,
            self.is_decimal,
        ) = (
            locales,
            currency,
            allow_empty,
            allow_netative,
            decimal_places,
            use_currency_symbol,
            is_decimal,
        )
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return {
            **attrs,
            "data-toggle": "well-mask-money",
            "data-locales": self.locales,
            "data-currency": self.currency,
            "data-allow-empty": str(self.allow_empty).lower(),
            "data-allow-negative": str(self.allow_netative).lower(),
            "data-use-currency-symbol": str(self.use_currency_symbol).lower(),
            "data-decimal-places": self.decimal_places,
        }

    def to_python(self, value):
        if isinstance(value, str):
            if not value.strip():
                return None
            is_negative = "-" in value
            numeros = extrair_somente_numeros(value)
            value = float(int(numeros or 0) / 10**self.decimal_places)
            if is_negative:
                value = -value
        if value is not None and self.is_decimal:
            return round(decimal.Decimal(value), self.decimal_places)
        return value

    def prepare_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return "{:,.{}f}".format(float(value), self.decimal_places)


class CPFField(SomenteDigitosMixin, forms.Field):
    widget = MaskedInput(
        mask="'999.999.999-99'", attrs={"pattern": "^\d{3}\.\d{3}\.\d{3}-\d{2}$"}
    )
    default_validators = (BRCPFValidatorCustom(),)


class CNPJField(SomenteDigitosMixin, forms.Field):
    widget = MaskedInput(
        mask="'99.999.999/9999-99'",
        attrs={"pattern": "^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$"},
    )
    default_validators = (BRCNPJValidatorCustom(),)


class DocumentoField(SomenteDigitosMixin, forms.Field):
    """Input com validação dinâmica entre cpf e cnpj"""

    widget = MaskedInput(
        mask="['999.999.999-99','99.999.999/9999-99']",
        attrs={
            "pattern": "^(\d{3}\.\d{3}\.\d{3}-\d{2})|(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})$"
        },
    )

    def run_validators(self, value):
        value = self.to_python(value)
        if len(value) <= 11:
            self.validators = (BRCPFValidatorCustom(),)
        else:
            self.validators = (BRCNPJValidatorCustom(),)
        return super().run_validators(value)


class TelefoneField(SomenteDigitosMixin, forms.Field):
    widget = MaskedInput(
        mask="['(99) 9999-9999','(99) 99999-9999']",
        attrs={"pattern": "^\(\d{2}\) \d{4,5}-\d{4}$"},
    )

    def validate(self, value):
        if (value and len(value) not in (10, 11)) or (not value and self.required):
            raise forms.ValidationError("O telefone deve ter 10 ou 11 dígitos")
        super().validate(value)


class CEPField(SomenteDigitosMixin, forms.Field):
    widget = MaskedInput(mask="'99999-999'", attrs={"pattern": "^\d{5}-\d{3}$"})

    def validate(self, value):
        if (value and not len(value) == 8) or (not value and self.required):
            raise forms.ValidationError("O CEP deve ter 8 dígitos")
        super().validate(value)


class GoogleMapsPolygonWidget(forms.Textarea):
    template_name = "hcc_lib_integra/admin/polygon_widget.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

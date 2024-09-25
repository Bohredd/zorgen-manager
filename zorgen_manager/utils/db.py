from django.db.models import ExpressionWrapper, Func, CharField, F


class CurrencyFormatFunc(ExpressionWrapper):
    """
    Retorna valores em moeda já formatados do banco de dados

    exemplo de uso:

    queryset = (
        <seu model>.objects.annotate(
            <campo no annotate, ex: valor_formatado>=CurrencyFormatFunc("<campo no model com valor a ser formatado>")
        )
    )

    print(queryset.first().valor_formatado)
    """

    class FormatCurrency(Func):
        template = "REPLACE(REPLACE(REPLACE(to_char(%(expressions)s, 'FMR$ 999,999,999,999,999,999,990.00'),'.',';'),',','.'),';',',')"

    def __init__(self, field_name):
        self.field_name = field_name
        super(ExpressionWrapper, self).__init__(output_field=CharField())
        self.expression = self.FormatCurrency(F(self.field_name))

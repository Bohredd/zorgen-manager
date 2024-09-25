from django.db.models import QuerySet, Case, When, Value, CharField


class GeradorDeRelatorios:
    """
    Classe para facilitar a geração de relatórios com campos de models de bancos externos

    exemplo de uso:

    no caso abaixo, o gerador irá adicionar um annotate na queryset com o nome "cidade_obra"
    que irá conter o nome da cidade do endereço com o pk contido no campo "execution_address_id" do model Process
    relatorio = GeradorDeRelatorios(
        "idf",
        "title",
        queryset=User.objects.filter(idf__gt=1000),
        campos_externos={
            "cidade_obra": {
                "model_externo": Endereco,
                "campo_model_externo": "cidade__nome",
                "campo_model_interno": "execution_address_id",
            }
        },
    ).values() ou values_list()
    """

    def __init__(self, *fields: str, queryset: QuerySet, campos_externos={}):
        self.queryset = queryset
        self.fields = fields
        self.campos_externos = campos_externos
        self.todos_os_campos = [*fields, *campos_externos.keys()]

    @staticmethod
    def get_tuplas_when(
        *,
        queryset,
        model_externo,
        campo_model_interno,
        campo_model_externo,
        model_externo_pk="pk",
    ):
        return model_externo.objects.filter(
            pk__in=list(
                queryset.filter(
                    **{f"{campo_model_interno}__isnull": False}
                ).values_list(campo_model_interno, flat=True)
            ),
            **{f"{campo_model_externo}__isnull": False},
        ).values_list(model_externo_pk, campo_model_externo)

    def get_queryset(self) -> QuerySet:
        annotates = {}
        for field_name, config in self.campos_externos.items():
            model_externo = config.get("model_externo")
            campo_model_interno = config["campo_model_interno"]
            model_externo_pk = config.get("model_externo_pk", "pk")
            campo_model_externo = config.get("campo_model_externo")
            output_field = config.get("output_field", CharField())
            default = config.get("default")
            tuplas_when = config.get("tuplas_when")
            if tuplas_when is None:
                tuplas_when = self.get_tuplas_when(
                    queryset=self.queryset,
                    model_externo=model_externo,
                    campo_model_interno=campo_model_interno,
                    campo_model_externo=campo_model_externo,
                    model_externo_pk=model_externo_pk,
                )
            annotates[field_name] = Case(
                *[
                    When(
                        **{campo_model_interno: resultado[0]},
                        then=Value(resultado[1]),
                    )
                    for resultado in tuplas_when.iterator()
                ],
                default=default,
                output_field=output_field,
            )
        return self.queryset.annotate(**annotates)

    def values(self):
        return self.get_queryset().values(*self.todos_os_campos)

    def values_list(self):
        return self.get_queryset().values_list(*self.todos_os_campos)

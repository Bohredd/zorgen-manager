import operator
from typing import Iterable
from django.db import models
from functools import reduce


class SearchFilter:
    """ """

    lookup_prefixes = {
        "^": "istartswith",
        "=": "iexact",
        "@": "search",
        "$": "iregex",
    }

    def get_search_terms(self, params=""):
        params = params.replace("\x00", "")
        params = params.replace(",", " ")
        return params.split()

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return "__".join([field_name, lookup])

    def filter_queryset(self, queryset, search_fields: Iterable[str], search_value):
        search_terms = self.get_search_terms(search_value)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field)) for search_field in search_fields
        ]

        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term}) for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        return queryset


def search_in_queryset(queryset, search_fields: Iterable[str], search_value=""):
    """
    facilitador de filtragem tipo search

    queryset: auto explicativo
    search_fields: Iterable[str] - lista de campos para filtro
    search_value: termo da busca

    exemplo de uso em FilterSet do django-filters
        search = django_filters.filters.CharFilter(
            method=lambda queryset, _, value: search_in_queryset(
                queryset,
                (
                    "titulo",
                    "idf",
                ),
                value,
            ),
        )
    """
    searchFilter = SearchFilter()
    return searchFilter.filter_queryset(queryset, search_fields, search_value)

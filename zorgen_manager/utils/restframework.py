from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param


class PageNumberPaginationCustomizada(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_first_link(self):
        if self.page.number <= 2:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, 1)

    def get_last_link(self):
        if not self.page.has_next():
            return None
        next_page_number = self.page.next_page_number()
        last_page_number = self.page.paginator.num_pages
        if next_page_number == last_page_number:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, last_page_number)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("first", self.get_first_link()),
                    ("last", self.get_last_link()),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    (
                        "page_links",
                        [
                            {
                                "url": page_link.url,
                                "number": page_link.number,
                                "is_break": page_link.is_break,
                                "is_active": page_link.is_active,
                            }
                            for page_link in self.get_html_context()["page_links"]
                        ],
                    ),
                    ("results", data),
                ]
            )
        )

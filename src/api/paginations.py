from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
from rest_framework.response import Response


class IngredientsPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100
    page_size = 15
    status = "ok"

    def get_paginated_response(self, data):

        return Response(OrderedDict([
            ('status', self.status),
            ('data', {
                'count': self.page.paginator.count,
                'limit': self.page.paginator.per_page,
                'total_pages': self.page.paginator.num_pages,
                'pagination_next': self.get_next_link(),
                'list': data
                }
             )
            # ('count', self.page.paginator.count),
            # ('pagination_next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            # ('current_page', self.page.number),
            # ('total_pages', self.page.paginator.num_pages),
            # ('limit', self.page.paginator.per_page),
            # ('data', data),
        ]))

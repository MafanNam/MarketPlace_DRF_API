from rest_framework.pagination import PageNumberPagination


class CartAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000



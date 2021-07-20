from rest_framework.pagination import PageNumberPagination
from rest_framework_gis.pagination import GeoJsonPagination


class LocationsGEOPagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 14


class LocationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 14

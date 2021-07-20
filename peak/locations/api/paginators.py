from rest_framework_gis.pagination import GeoJsonPagination


class LocationsPagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

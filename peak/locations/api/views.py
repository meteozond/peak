from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Location
from .paginators import LocationsPagination
from .serializers import LocationSerializer


class LocationsViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    """
    Список областей обслуживания.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = Location.objects.all().prefetch_related('company', 'locservice_set')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = LocationsPagination

from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import Company
from .paginators import CompaniesPagination
from .serializers import CompanySerializer


class CompaniesViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    """
    Управление службами эксплуатации
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    queryset = Company.objects.prefetch_related('address', 'address__city')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    pagination_class = CompaniesPagination

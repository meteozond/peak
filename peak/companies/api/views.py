from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from django.utils.translation import gettext_lazy as _

from ..models import Company
from .paginators import CompaniesPagination
from .serializers import CompanySerializer


@extend_schema_view(
    list=extend_schema(description=_('Список служб эксплуатации')),
    create=extend_schema(description=_('Создать службу эксплуатации')),
    update=extend_schema(description=_('Обновить службу эксплуатации')),
    retrieve=extend_schema(description=_('Информация о службе эксплуатации')),
    destroy=extend_schema(description=_('Удалить службу эксплуатации')),
)
class CompaniesViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    """
    Управление службами эксплуатации
    """
    http_method_names = ['get', 'post', 'put']
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    queryset = Company.objects.prefetch_related('address', 'address__city')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    pagination_class = CompaniesPagination

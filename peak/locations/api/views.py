from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema, extend_schema_view)
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.utils.translation import gettext_lazy as _

from ..models import Location
from .paginators import LocationsGEOPagination
from .serializers import (GeofilterSerializer, LocationListSerializer,
                          LocationSerializer)


@extend_schema_view(
    list=extend_schema(description=_('Список областей обслуживания')),
    create=extend_schema(description=_('Создать область обслуживания')),
    update=extend_schema(description=_('Обновить область обслуживания')),
    retrieve=extend_schema(description=_('Информация об области обслуживания')),
    destroy=extend_schema(description=_('Удалить область обслуживания')),
)
class LocationsViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    """
    Управления областями обслуживания.
    """
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, ]
    serializer_class = LocationSerializer
    queryset = Location.objects.all().prefetch_related('company', 'locservice_set__service')
    pagination_class = LocationsGEOPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='service',
                description=_('Выборка по услуге'),
                required=False, type=str,
                examples=[OpenApiExample(_('Пример'), value='Перекладка плитки'), ],
            ),
            OpenApiParameter(
                name='point',
                type=str,
                description=_('Выборка по локации'),
                examples=[OpenApiExample(_('Пример'), value='SRID=4326;POINT (66 66)'), ],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # проверка параметров запроса и фильтрация
        serializer = GeofilterSerializer(data={
            'service': request.GET.get('service', ''),
            'point': request.GET.get('point', ''),
        })
        if not serializer.is_valid():
            return Response(serializer.errors)
        if serializer.data['service']:
            queryset = queryset.filter(
                locservice__service__name=serializer.data['service']
            )
        if serializer.data['point']:
            queryset = queryset.filter(
                location__contains=serializer.data['point']
            )

        # пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LocationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LocationListSerializer(queryset, many=True)
        return Response(serializer.data)

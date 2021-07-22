from rest_framework import serializers

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException
from django.utils.translation import gettext_lazy as _


class ValidateGeo:
    """
    Проверяет, что гео поле можно преобразовать в заданный тип геопозиции.
    """

    def __init__(self, geom_typeid):
        self.geom_typeid = geom_typeid

    def __call__(self, value):
        try:
            poly = GEOSGeometry(value)
        except (GEOSException, ValueError):
            raise serializers.ValidationError({
                'location': _('Значение не распознано, допустимые форматы: WKT, EWKT, HEXEWKB.')
            })
        if poly.geom_typeid != self.geom_typeid:
            raise serializers.ValidationError({
                'location': _(f'Неверный тип геопозиции. Допустимый тип: {self.geom_typeid}')
            })
        srids = [4326, ]
        if poly.srid not in srids:
            raise serializers.ValidationError({
                'location': _(f'Недопустимый SRID, возможные значения: {srids}')
            })
        return value

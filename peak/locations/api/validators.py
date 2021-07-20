from rest_framework import serializers

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException
from django.utils.translation import gettext_lazy as _


def validate_poly(value):
    """
    Проверяет, что гео поле можно преобразовать в полигон.
    """
    try:
        poly = GEOSGeometry(value)
    except (GEOSException, ValueError):
        raise serializers.ValidationError({
            'location': _('Значение не распознано, допустимые форматы: WKT, EWKT, HEXEWKB.')
        })

    if not poly.valid and poly.geom_typeid != 3:
        raise serializers.ValidationError({
            'location': _('Значение не является полигоном.')
        })
    srids = [4326, ]
    if poly.srid not in srids:
        raise serializers.ValidationError({
            'location': _(f'Недопустимый SRID, возможные значения: {srids}')
        })
    return value

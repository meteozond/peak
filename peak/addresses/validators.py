from cities_light.models import City

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_city(value: str):
    """
    Проверяет наличие города в БД.
    """
    if not City.objects.filter(name=value):
        msg = _('Такого города не существует.')
        code = 'Несуществующий город'
        raise ValidationError(msg, code)

from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City

from .managers import AddressManager


class Address(models.Model):
    """
    Адреса.
    """
    city = models.ForeignKey(
        City,
        verbose_name=_('Город'),
        help_text=_('Город'),
        on_delete=models.PROTECT,
    )
    postcode = models.PositiveIntegerField(
        verbose_name=_('Почтовый индекс'),
        help_text=_('Почтовый индекс'),
    )
    street_name = models.CharField(
        verbose_name=_('Название улицы'),
        help_text=_('Название улицы'),
        max_length=50,
    )
    building_number = models.CharField(
        verbose_name=_('Номер дома'),
        help_text=_('Номер дома'),
        max_length=10,
    )
    room = models.CharField(
        verbose_name=_('Помещение'),
        help_text=_('Помещение'),
        max_length=10,
        blank=True,
    )
    objects = AddressManager.as_manager()

    class Meta:
        verbose_name = _('Адрес')
        verbose_name_plural = _('Адреса')

    def __str__(self):
        return self.city.name

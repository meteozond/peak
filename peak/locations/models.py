from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import LocationManager, ServiceManager


class Service(models.Model):
    """
    Оказываемые услуги.
    """
    name = models.CharField(
        verbose_name=_('Название услуги'),
        help_text=_('Название услуги'),
        max_length=200,
        unique=True,
    )
    price = models.DecimalField(
        verbose_name=_('Локация'),
        help_text=_('Локация'),
        max_digits=11,
        decimal_places=2,
    )
    objects = ServiceManager.as_manager()

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')

    def __str__(self):
        return f'{self.name}'


class Location(models.Model):
    """
    Области обслуживания.
    """
    name = models.CharField(
        verbose_name=_('Название локации'),
        help_text=_('Название локации'),
        max_length=200,
    )
    location = models.PolygonField(
        verbose_name=_('Локация'),
        help_text=_('Локация'),
        spatial_index=True,
        # geography=True,
    )
    services = models.ManyToManyField(
        Service,
        verbose_name=_('Оказываемые услуги'),
        help_text=_('Оказываемые услуги'),
    )
    objects = LocationManager.as_manager()

    class Meta:
        verbose_name = _('Область обслуживания')
        verbose_name_plural = _('Области обслуживания')

    def get_absolute_url(self):
        return reverse('api:locations-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'

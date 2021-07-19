from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from peak.companies.models import Company

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
    company = models.ForeignKey(
        Company,
        verbose_name=_('Служба эксплуатации'),
        help_text=_('Служба эксплуатации'),
        on_delete=models.CASCADE,
    )

    objects = LocationManager.as_manager()

    class Meta:
        verbose_name = _('Область обслуживания')
        verbose_name_plural = _('Области обслуживания')

    def get_absolute_url(self):
        return reverse('api:locations-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'


class LocServices(models.Model):
    """
    Цена за услугу в области обслуживания.
    """
    location = models.ForeignKey(
        Location,
        verbose_name=_('Локация'),
        help_text=_('Локация'),
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        verbose_name=_('Услуга'),
        help_text=_('Услуга'),
        on_delete=models.PROTECT,
    )
    price = models.DecimalField(
        verbose_name=_('Цена за услугу'),
        help_text=_('Цена за услугу'),
        max_digits=11,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _('Область обслуживания')
        verbose_name_plural = _('Области обслуживания')

    def __str__(self):
        return f'{self.location.name}: {self.service.name} {self.price}'

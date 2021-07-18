from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.postgres.fields import CICharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from peak.addresses.models import Address

from .managers import CompanyManager, CompanySerializerManager


class Company(models.Model):
    """
    Службы эксплуатации.
    """
    name = CICharField(
        verbose_name=_('Название компании'),
        help_text=_('Название компании'),
        max_length=200,
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_('Электронная почта"'),
        help_text=_('Электронная почта'),
        unique=True,
    )
    phone = PhoneNumberField(
        verbose_name=_('Номер телефона'),
        help_text=_('Номер телефона в международном формате'),
    )
    address = models.OneToOneField(
        Address,
        verbose_name=_('Адрес центрального офиса'),
        help_text=_('Адрес центрального офиса'),
        on_delete=models.PROTECT,
    )
    objects = CompanyManager.as_manager()
    s_objects = CompanySerializerManager.as_manager()

    class Meta:
        verbose_name = _('Служба эксплуатации')
        verbose_name_plural = _('Службы эксплуатации')

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'id': self.pk})

    def __str__(self):
        return f'{self.name}'

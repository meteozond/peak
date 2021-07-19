from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    name = 'peak.locations'
    verbose_name = _('Области обслуживания')

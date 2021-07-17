from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompaniesConfig(AppConfig):
    name = 'peak.companies'
    verbose_name = _('Службы эксплуатации')

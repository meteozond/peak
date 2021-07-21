from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularSwaggerView

from django.conf import settings


class CustomSpectacularSwaggerView(SpectacularSwaggerView):

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        response = super(CustomSpectacularSwaggerView, self).get(request, *args, **kwargs)
        response.data['api_version'] = settings.SPECTACULAR_SETTINGS.get('VERSION', '0.0.1')
        return response

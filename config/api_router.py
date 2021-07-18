from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from peak.users.api.views import UserViewSet
from peak.companies.api.views import CompaniesViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("companies", CompaniesViewSet, basename='companies')


app_name = "api"
urlpatterns = router.urls

from django.urls import path, include
from rest_framework import routers

from teams.views import TeamViewSet

router = routers.DefaultRouter()
router.register("teams", TeamViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "teams"

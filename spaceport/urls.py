from django.urls import path, include
from spaceport.views import (
    SpaceshipViewSet,
    SpaceflightViewSet,
    CrewViewSet,
    OrderViewSet,
    SpaceshipTypeViewSet,
    PlanetViewSet,
    SpaceportViewSet,
    RouteViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()

router.register("spaceship_types", SpaceshipTypeViewSet)
router.register("crews", CrewViewSet)
router.register("spaceships", SpaceshipViewSet)
router.register("planets", PlanetViewSet)
router.register("spaceports", SpaceportViewSet)
router.register("routes", RouteViewSet)
router.register("spaceflights", SpaceflightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "spaceport"

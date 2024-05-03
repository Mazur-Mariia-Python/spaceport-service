from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from spaceport.models import (
    Spaceship,
    Spaceflight,
    Crew,
    Order,
    SpaceshipType,
    Planet,
    Spaceport,
    Route,
)
from spaceport.permissions import IsAdminOrIfAuthenticatedReadOnly

from spaceport.serializers import (
    SpaceshipSerializer,
    SpaceshipTypeSerializer,
    CrewSerializer,
    SpaceshipListSerializer,
    OrderSerializer,
    OrderListSerializer,
    SpaceshipImageSerializer,
    SpaceflightListSerializer,
    PlanetSerializer,
    RouteSerializer,
    RouteListSerializer,
    SpaceportListSerializer,
)


class SpaceshipTypeViewSet(viewsets.ModelViewSet):
    queryset = SpaceshipType.objects.all()
    serializer_class = SpaceshipTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_permissions(self):
        if self.action in (
            "destroy",
            "update",
            "partial_update",
        ):
            return [IsAdminUser()]
        return super().get_permissions()


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_permissions(self):
        if self.action in (
            "destroy",
            "update",
            "partial_update",
        ):
            return [IsAdminUser()]
        return super().get_permissions()


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class SpaceportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Spaceport.objects.all()
    serializer_class = SpaceportListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteSerializer

        return RouteSerializer


class SpaceshipViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Spaceship.objects.all()
    serializer_class = SpaceshipSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        crews = self.request.query_params.get("crews")

        if crews:
            crew_ids = self._params_to_ints(crews)
            queryset = Spaceship.objects.filter(crews__id__in=crew_ids)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("crews")
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return SpaceshipListSerializer
        if self.action == "retrieve":
            return SpaceshipListSerializer
        if self.action == "upload_image":

            return SpaceshipImageSerializer

        return SpaceshipSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific bus"""
        spaceship = self.get_object()
        serializer = self.get_serializer(spaceship, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="crew.id",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by crews id (ex. ?crews=2,5)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SpaceflightViewSet(viewsets.ModelViewSet):
    queryset = Spaceflight.objects.all()
    serializer_class = SpaceflightListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset.select_related("spaceship").annotate(
                    tickets_available=F("spaceship__seats_in_row")
                    * F("spaceship__rows")
                    - Count("tickets")
                )
            ).order_by("id")
        return queryset


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user.id)

        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__spaceflight__spaceship")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

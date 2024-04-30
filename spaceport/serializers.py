from django.db import transaction
from rest_framework import serializers
from spaceport.models import (
    SpaceshipType,
    Crew,
    Spaceship,
    Planet,
    Route,
    Spaceflight,
    Order,
    Ticket,
    Spaceport,
)


class SpaceshipTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpaceshipType
        fields = ("id", "spaceship_type_name")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class SpaceshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spaceship
        fields = (
            "id",
            "spaceship_name",
            "rows",
            "seats_in_row",
            "image",
            "spaceship_types",
            "crews",
        )


class SpaceshipListSerializer(SpaceshipSerializer):
    spaceship_types = serializers.CharField(
        source="spaceship_types.spaceship_type_name",
        read_only=True,
    )

    crews = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Spaceship
        fields = (
            "id",
            "spaceship_name",
            "rows",
            "seats_in_row",
            "image",
            "spaceship_types",
            "crews",
        )


class SpaceshipDetailSerializer(SpaceshipSerializer):
    crews = CrewSerializer(many=True, read_only=True)


class SpaceshipImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spaceship
        fields = ("id", "image")


class PlanetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Planet
        fields = ("id", "planet_name")


class SpaceportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spaceport
        fields = ("id", "spaceport_name")


class SpaceportListSerializer(SpaceportSerializer):
    planet = serializers.CharField(
        source="closest_planet.planet_name",
        read_only=True,
    )

    class Meta:
        model = Spaceport
        fields = ("id", "spaceport_name", "planet")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "distance")


class RouteListSerializer(RouteSerializer):
    source_name = serializers.CharField(
        source="source.spaceport_name",
        read_only=True,
    )
    destination = serializers.CharField(
        source="destination.spaceport_name",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = ("id", "distance", "source_name", "destination")


class SpaceflightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spaceflight
        fields = ("id", "departure_time", "arrival_time", "route", "spaceship")


class SpaceflightListSerializer(SpaceflightSerializer):
    spaceship_name = serializers.CharField(
        source="spaceship.spaceship_name",
        read_only=True,
    )
    spaceship_num_seats = serializers.IntegerField(
        source="spaceship.num_seats",
        read_only=True,
    )
    tickets_available = serializers.IntegerField(read_only=True)
    route = serializers.CharField(
        source="route.full_route",
        read_only=True,
    )

    class Meta:
        model = Spaceflight
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "spaceship_name",
            "spaceship_num_seats",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_seat(
            attrs["seat"],
            attrs["spaceflight"].spaceship.num_seats,
            serializers.ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "spaceflight", "order")


class TicketListSerializer(TicketSerializer):
    spaceflight = SpaceflightListSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "spaceflight")


class SpaceflightDetailSerializer(SpaceflightSerializer):
    spaceship = SpaceshipDetailSerializer(many=False, read_only=True)

    taken_seats = serializers.SlugRelatedField(
        source="ticket_set", many=True, read_only=True, slug_field="seat"
    )

    class Meta:
        model = Spaceflight
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "spaceship",
            "taken_seats",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
        )

    def create(self, validated_data):

        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

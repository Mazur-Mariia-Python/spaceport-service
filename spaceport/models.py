import os
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify


def spaceship_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.spaceship_name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/spaceships/", filename)


class SpaceshipType(models.Model):
    spaceship_type_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "spaceship_types"

    def __str__(self):
        return self.spaceship_type_name


class Crew(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Spaceship(models.Model):
    spaceship_name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    image = models.ImageField(null=True, upload_to=spaceship_image_file_path)
    spaceship_types = models.ForeignKey(
        SpaceshipType,
        on_delete=models.CASCADE,
        related_name="spaceship_types",
    )
    crews = models.ManyToManyField(Crew, related_name="spaceships")

    class Meta:
        verbose_name_plural = "spaceships"

    @property
    def num_seats(self):
        return self.seats_in_row * self.rows

    def __str__(self):
        return self.spaceship_name


class Planet(models.Model):
    planet_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.planet_name)


class Spaceport(models.Model):
    spaceport_name = models.CharField(max_length=255)
    closest_planet = models.ForeignKey(
        Planet,
        on_delete=models.CASCADE,
        related_name="spaceports",
    )

    def __str__(self):
        return str(self.spaceport_name)


class Route(models.Model):
    distance = models.IntegerField()
    source = models.ForeignKey(
        Spaceport,
        on_delete=models.CASCADE,
        related_name="sources",
    )
    destination = models.ForeignKey(
        Spaceport,
        on_delete=models.CASCADE,
        related_name="destinations",
    )

    class Meta:

        indexes = [
            models.Index(fields=["source", "destination"]),
            models.Index(fields=["source"]),
        ]

    @property
    def full_route(self):
        return self.source.spaceport_name + " - " + self.destination.spaceport_name

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.distance} km)"


class Spaceflight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="routes",
    )
    spaceship = models.ForeignKey(
        Spaceship,
        on_delete=models.CASCADE,
        related_name="spaceships",
    )

    def __str__(self):
        return f"{self.route}: {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    spaceflight = models.ForeignKey(
        "Spaceflight",
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("spaceflight", "seat")
        ordering = ("seat",)

    def __str__(self):
        return f"{self.spaceflight.spaceship.spaceship_name} (row: {self.row}, seat: {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise(
                {"seat": f"seat must be in range [1, {num_seats}], not {seat}"}
            )

    def clean(self):
        Ticket.validate_seat(
            self.seat,
            self.spaceflight.spaceship.seats_in_row,
            ValidationError,
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

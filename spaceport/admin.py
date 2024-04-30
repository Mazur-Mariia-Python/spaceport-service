from django.contrib import admin

from spaceport.models import (
    Ticket,
    Order,
    SpaceshipType,
    Crew,
    Spaceship,
    Planet,
    Spaceport,
    Route,
    Spaceflight,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(SpaceshipType)
admin.site.register(Crew)
admin.site.register(Spaceship)
admin.site.register(Planet)
admin.site.register(Spaceport)
admin.site.register(Route)
admin.site.register(Spaceflight)
admin.site.register(Ticket)

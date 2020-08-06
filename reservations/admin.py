from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):
    """ Reservation Admin Definition """

    list_display = (
        "user",
        "room",
        "reservation_date",
        "match_start",
        "match_end",
    )
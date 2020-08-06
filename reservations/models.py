from django.db import models
from core import models as core_models


class Reservation(core_models.TimeStampedModel):
    """
    Reservation Model Definition
    예약한사람 / 전화번호 / 방(예약장소)  /예약일  /예약 시간
    """
    # user = models.CharField(max_length=50)
    user = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE)
    call = models.CharField(max_length=150)
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE)
    reservation_date = models.DateField()
    match_start = models.TimeField()
    match_end = models.TimeField()

    def __str__(self):
        return f"{self.room}"
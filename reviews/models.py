from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """
     Review Model Definition
     리뷰내용 / 작성자(유저) / 예약일/ 위치 / 구장관리상태 / 시설 / 사용자 / 방(경기장)
     """

    review = models.TextField()
    reservation_date = models.DateField()

    # 별점 기준
    # 위치 / 구장관리상태 / 시설
    location_rating = models.IntegerField()
    Management_status_rating = models.IntegerField()
    facility_rating = models.IntegerField()

    # user 삭제시 review 삭제
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE)
    # Room 삭제시 review 삭제
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE)

    # ForeignKey 로 연결되어 있으면 객체에 접근가능
    # def __str__(self):
    #    return self.room.name
    def __str__(self):
        return f"{self.room} : {self.user}"

    # 평균평점
    def rating_average(self):
        avg = (
                      self.location_rating
                      + self.Management_status_rating
                      + self.facility_rating
              ) / 3
        return round(avg, 1)

    # rating_average.short_description = "AVG"
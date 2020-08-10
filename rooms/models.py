from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 축구장 or 풋살장
class RoomType(AbstractItem):
    """ RoomType Model Definition """
    pass


# 편의시설
class Facility(AbstractItem):
    """ Facility Model Definition """

    # 표기 이름 변경
    class Meta:
        verbose_name_plural = "Facilities"


# 규칙
class FieldRule(AbstractItem):
    """ FieldRule Model Definition """

    class Meta:
        verbose_name = "Field Rule"


# 사진
class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    title = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")

    # Room 과 Photo 연결
    # Room 삭제시 Photo 삭제
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Room(core_models.TimeStampedModel):
    """
    Room Model Definition
    이름/내용/가격/예약일/체크인/체크아웃/연락처/방형식/편의시설 /필드규칙/구장위치
    """
    name = models.CharField(max_length=50)
    info = models.TextField()
    price = models.IntegerField()
    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    contact = models.CharField(max_length=50)
    location = models.CharField(max_length=150)
    # room_type 삭제시 Room 을 보존
    # room_type = models.ForeignKey("RoomType",  on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    # 다 대 다 관계
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", blank=True)
    field_rules = models.ManyToManyField(
        "FieldRule", related_name="rooms", blank=True)

    # 등록자는 필요없을듯 어짜피 관리자가 관리할것
    # registrant = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # name 을  Room 객체를 표기함
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 이 방(경기장)의 평점
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        # self.reviews.all()
        # reivews 모델 객체를 모두 가져온다.
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
                # 반올림 round
            return round(all_ratings / len(all_reviews), 2)
        return 0

    # 방의 첫번째 사진만 보여줌
    def first_photo(self):
        photo, = self.photos.all()[:1]
        return photo.file.url

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        print(photos)
        return photos

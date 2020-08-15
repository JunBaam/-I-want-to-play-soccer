from django.utils import timezone
from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models
from cal import Calendar
from bs4 import BeautifulSoup
import requests


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
    date = models.DateField(blank=True, null=True)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    contact = models.CharField(max_length=50)
    district = models.CharField(max_length=10, null=True)
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
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        # print(photos)
        return photos

    # 달력
    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        # 13월 되는것을 방지.
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)

        return [this_month_cal, next_month_cal]

    def get_weather(self):
        district = self.district
        html = requests.get('https://search.naver.com/search.naver?query=날씨' + district)
        soup = BeautifulSoup(html.text, 'html.parser')
        data1 = soup.find('div', {'class': 'weather_box'})
        # 구장위치
        find_address = data1.find('span', {'class': 'btn_select'}).text
        # 온도
        find_currenttemp = data1.find('span', {'class': 'todaytemp'}).string+"℃"
        data2 = data1.findAll('dd')
        # 미세먼지
        find_dust = data2[0].find('span', {'class': 'num'}).string
        # 초미세먼지
        find_ultra_dust = data2[1].find('span', {'class': 'num'}).string
        # 현재상태
        find_currentstate = data1.find('p', {'class': 'cast_txt'}).text

        return [find_currenttemp, find_address, find_dust, find_ultra_dust, find_currentstate]



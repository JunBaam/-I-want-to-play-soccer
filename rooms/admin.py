from django.contrib import admin
from . import models
from django.utils.html import mark_safe


@admin.register(models.RoomType, models.Facility, models.FieldRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    pass


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)
    # 미리보기
    list_display = (
        "name",
        "price",
        "location",
        "date",
        "check_in",
        "check_out",
        "room_type",
        "total_rating",

    )
    # 이름으로 검색 =을 붙이면 대소문자 구분을 안함
    search_fields = ("=name",)
    # 정렬 순서
    ordering = ("name", "date")

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition """
    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

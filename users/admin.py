from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

"""
Django UserAdmin 을 사용
"""


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """
    fieldsets = UserAdmin.fieldsets + (
        (
            "Add Profile Content",
            {
                "fields": (
                    "user_image",
                    "login_method",
                )
            },
        ),
    )

    # ID/ 성/이름/이메일 / 슈퍼유저(관리자)
    list_display = (
        "username",
        "email",
        "is_superuser",
        "login_method",

    )
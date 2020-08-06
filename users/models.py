from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class User(AbstractUser):
    user_image = models.ImageField(upload_to="user", blank=True)

    # 로그인 방법
    LOGIN_EMAIL = "email"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGING_KAKAO, "Kakao"),
    )

    # 이메일 검증.
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    # 로그인 방법선택
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )


    # user model에서 view on site 생성
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

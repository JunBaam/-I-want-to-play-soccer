import os
import requests
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from django.core.files.base import ContentFile
from django.contrib import messages


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def kakao_login(request):
    client_id = os.environ.get("KAKAO")
    print(client_id)
    redirect_uri = "http://15.165.223.171:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


# kakao Host로 request해야함
# kakao_login 함수에서 redirect를 통해 code 값을 받아온다.
def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO")
        redirect_uri = "http://15.165.223.171:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        # access_token
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        # 카카오에서 응답하는 가입하려는 유저의 정보
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        # print(profile_request.json())
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email")
        # print(email)
        if email is None:
            raise KakaoException("이메일을 제공해주세요.")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = profile_json.get("kakao_account").get("profile").get("profile_image_url")

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException(f"로그인해주세요:{user.login_method}")
        except models.User.DoesNotExist:
         
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            # 프로필 이미지 확인
            if profile_image is not None:
                # print(profile_image)
                # print(requests.get(profile_image))
                photo_request = requests.get(profile_image)
                # content() : 0,1만 있는 파일 //바이트파일
                user.user_image.save(
                    # f"{nickname}-user_image", ContentFile(photo_request.content)
                    f"{nickname}.jpg", ContentFile(photo_request.content)
                )

        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"
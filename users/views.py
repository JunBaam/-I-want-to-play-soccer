import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins
from django.core.files.base import ContentFile


class LoginView(mixins.LoggedOutOnlyView, FormView):
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


class SignUpView(mixins.LoggedOutOnlyView, FormView):
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
                print(profile_image)
                print(requests.get(profile_image))
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

    # users 모델 속성확인용
    # print(vars(model))

    # 템플릿안에 더많은 context 를 사용할수 있게해준다.
    # get_context_data 는 기본적으로 user_obj를 준다.
    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["hi"]="test"
    #    return context


# UpdateView : 모델 또는 객체를 가져옴 , Form 도 만들어준다.
class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
        "user_image",
    )

    # 수정하고 싶어하는 객체를 반환한다.
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form


"""
 def form_valid(self, form):
     email = form.cleaned_data.get("email")

     self.object.username = email
     self.object.save()
     return super().form_valid(form)
 """


# PasswordChangeView : 디폴트는 admin 비밀번호 변경페이지로 보내버림
# 1.현재비밀번호 2.새로운비밀번호 3.비밀번호검증
# 번경시(성공시) 반드시 password_change_done 이라는 url로 가야됨
class UpdatePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update_password.html"
    success_url = reverse_lazy("")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재 비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새로운 비밀번호"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "새로운 비밀번호 확인"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()

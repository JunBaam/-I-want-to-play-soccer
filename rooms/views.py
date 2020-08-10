from django.views.generic import ListView, DetailView, View, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from . import models, forms
from users import models as user_models
from users import mixins as user_mixins
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    """ HomeView Definition """
    model = models.Room
    paginate_by = 12

    # 정렬방식 
    # ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ RoomDetail Definition """

    model = models.Room
    user = user_models.User


# 방검색
def search(request):
    # 내가 name 폼에 입력한 값을 받아온다.
    name = request.GET.get("name")
    if name:
        # form : 모든 form 값 html 포함.
        form = forms.SearchForm(request.GET)

        # is_valid() : 에러 판별
        if form.is_valid():
            # cleaned_data : form 에서 정리된 데이터를 가져온다.
            # print(form.cleaned_data)
            # name = form.cleaned_data.get("name")
            room_type = form.cleaned_data.get("room_type")

            filter_args = {}

            if name != "Anywhere":
                filter_args["name__startswith"] = name
            if room_type is not None:
                filter_args["room_type"] = room_type

            rooms = models.Room.objects.filter(**filter_args)
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


# 방수정
class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"

    fields = {
        "name",
        "info",
        "price",
        "contact",
        "location",
        "room_type",
        "facilities",
        "field_rules",
    }


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "mixins/room/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)

        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    try:
        # 방이름
        # room = models.Room.objects.get(pk=room_pk)
        models.Photo.objects.filter(pk=photo_pk).delete()
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


# room_pk 방안에 photo_pk를 삭제해야한다.
# print(f"삭제 {photo_pk} from {room_pk}")

class EditPhotoView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = {
        "title",
    }
    success_url = reverse_lazy()

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})

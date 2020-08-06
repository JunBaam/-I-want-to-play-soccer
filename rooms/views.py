from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from . import models, forms


class HomeView(ListView):
    """ HomeView Definition """
    model = models.Room
    paginate_by = 12

    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ RoomDetail Definition """

    model = models.Room


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
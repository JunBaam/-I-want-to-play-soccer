from django import forms
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(initial="Anywhere")
    # ModelChoice 는 queryset을 필요로 한다.
    room_type = forms.ModelChoiceField(
        required=False, empty_label="모두", queryset=models.RoomType.objects.all()
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("title", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        print(pk)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


# 새로운 form 을 만든다.
class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room

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

    def save(self, *args, **kwargs):
        # commit = False : 객체를 생성하지만 DB에 넣지 않는다.
        room = super().save(commit=False)
        return room

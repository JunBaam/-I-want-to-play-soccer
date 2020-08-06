from django import forms
from . import models


class SearchForm(forms.Form):
    name = forms.CharField(initial="Anywhere")
    # ModelChoice 는 queryset을 필요로 한다.
    room_type = forms.ModelChoiceField(
        required=False, empty_label="모두", queryset=models.RoomType.objects.all()
    )
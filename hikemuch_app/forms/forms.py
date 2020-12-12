from hikemuch_app.forms.common import DisabledFormMixin
from hikemuch_app.models import Hike, Comment, MOUNTAINS
from django import forms



class HikeCreateForm(forms.ModelForm):
    class Meta:
        model = Hike
        widgets = {
            'mountain': forms.Select(choices=MOUNTAINS, attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'image': forms.FileInput(attrs={'class': 'custom-file-input'}), #to add gps coordinates
        }
        # exclude = ('created_by',)
        exclude = ('created_by',)


# class FilterForm(forms.Form):
#     Rila = 'RILA'
#     Pirin = 'PIRIN'
#
#     FILTER_CHOICES = (
#         (ORDER_ASC, 'Ascending'),
#         (ORDER_DESC, 'Descending'),
#     )
#
#     text = forms.CharField(
#         required=False,
#     )
#     order = forms.ChoiceField(
#         choices=ORDER_CHOICES,
#         required=False,
#     )


class FilterForm(forms.Form):
    ORDER_ASC = 'asc'
    ORDER_DESC = 'desc'

    ORDER_CHOICES = (
        (ORDER_ASC, 'Ascending'),
        (ORDER_DESC, 'Descending'),
    )

    text = forms.CharField(
        required=False,
    )
    order = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False,
    )


class DeleteHikeForm(HikeCreateForm, DisabledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DisabledFormMixin.__init__(self)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
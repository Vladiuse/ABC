from django import forms
from .models import Avatar


class AvatarsAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['sex'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Avatar
        fields = ['category', 'sex']


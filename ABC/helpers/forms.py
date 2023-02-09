from django import forms
from .models import Element, SiteElementRecord
from datetime import date
from django.forms import BaseModelFormSet


class SiteElementForm(forms.Form):
    element_contains = forms.ModelMultipleChoiceField(
        label='Включает элементы',
        queryset=Element.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-select', 'aria-label': 'multiple select example', 'multiple': ''}, )
    )
    urls = forms.CharField(
        label='Список urls',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )


class SiteElementRecordForm(forms.ModelForm):
    # site = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = SiteElementRecord
        fields = ['site', 'is_collect']
        widgets = {
            'site': forms.TextInput(attrs={ 'style': 'display:none;'})
        }

class SiteElementBaseFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = SiteElementRecord.objects.all()

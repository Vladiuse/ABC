from django.shortcuts import render
from .models import FormExample

# Create your views here.


def examples(requests):
    forms = FormExample.objects.all()
    content = {
        'forms': forms
    }
    return render(requests, 'forms/examples.html', content)


def show_form(requests, form_id):
    form = FormExample.objects.get(pk=form_id)
    content = {
        'form': form,
    }
    return render(requests, 'forms/show_form.html', content)

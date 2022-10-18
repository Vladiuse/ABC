from django.shortcuts import render
from .models import FormExample

# Create your views here.


def examples(requests):
    forms = FormExample.objects.all()
    content = {
        'forms': forms
    }
    return render(requests, 'forms/examples.html', content)

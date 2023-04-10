from django.shortcuts import render
from .models import FormExampleOLD, FormExample, CasinoExample
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def examples(requests):
    forms = FormExample.objects.only('id', 'image_url',).all()
    content = {
        'forms': forms
    }
    return render(requests, 'forms/examples.html', content)

@login_required
def show_form(requests, form_id):
    form = FormExample.objects.get(pk=141)
    content = {
        'form': form,
    }
    return render(requests, 'forms/show_form.html', content)

@login_required
def casino(requests):
    forms = CasinoExample.objects.only('id', 'image_url').all()
    content = {
        'forms': forms,
    }
    return render(requests, 'forms/casino.html', content)

@login_required
def show_casino(request, casino_id):
    # casino = CasinoExample.objects.get(pk=casino_id)
    form = FormExample.objects.get(pk=141)
    content = {
        'form': form,
    }
    return render(request, 'forms/show_form.html', content)

def form_localization(request):
    return render(request, 'forms/localization/index.html')
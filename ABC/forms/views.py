from django.shortcuts import render
from .models import FormExample
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def examples(requests):
    forms = FormExample.objects.only('id','image_url', 'url').all()
    content = {
        'forms': forms
    }
    return render(requests, 'forms/examples.html', content)

@login_required
def show_form(requests, form_id):
    form = FormExample.objects.get(pk=form_id)
    content = {
        'form': form,
    }
    return render(requests, 'forms/show_form.html', content)
@login_required
def casino(requests):
    return render(requests, 'forms/casino.html')

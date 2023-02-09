from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SiteElementForm, SiteElementBaseFormSet, SiteElementRecordForm
from .models import Site, Element, SiteElementRecord
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.db.models import Count, Q


def side_elements_links():
    query_set = Element.objects.annotate(count=Count('sites',filter=Q(siteelementrecord__is_collect=False)))
    return query_set

def index(request):
    return HttpResponse('HELPERS!')



def create_site_element_record(request):
    elements_links = side_elements_links()
    if request.method == 'POST':
        form = SiteElementForm(request.POST)
        if form.is_valid():
            elements = form.cleaned_data['element_contains']
            urls = form.cleaned_data['urls'].split('\n')
            urls = map(lambda x: x.strip(), urls)
            urls = set(urls)
            if '' in urls:
                urls.remove('')
            for url in urls:
                try:
                    v = URLValidator()
                    v(url)
                except ValidationError:
                    continue

                try:
                    site = Site.objects.get(pk=url)
                except Site.DoesNotExist:
                    site = Site.objects.create(url=url)
                site.element.add(*elements)
            content = {
                'form': SiteElementForm(),
                'elements': elements_links,
            }
            return render(request, 'helpers/site_element/create_site_element_record.html', content)
        else:
            content = {
                'form': form,
                'elements': elements_links,
            }
            return render(request, 'helpers/site_element/create_site_element_record.html', content)
    else:
        form = SiteElementForm()
        content = {
            'form': form,
            'elements': elements_links,
        }
        return render(request, 'helpers/site_element/create_site_element_record.html', content)


def site_elem_record(request, elem_id):
    elements_links = side_elements_links()
    current_element = Element.objects.get(pk=elem_id)
    records = SiteElementRecord.objects.filter(element=current_element)
    SERFormSet = modelformset_factory(
        SiteElementRecord,
        form=SiteElementRecordForm,
        fields=['site', 'is_collect'],
        extra=0,
    )
    if request.method == 'POST':
        formset = SERFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('helpers:site_elem_record', args=[elem_id]))
        else:
            content = {
                'current_element': current_element,
                'records': records,
                'formset': formset,
                'elements': elements_links,
            }
            return render(request, 'helpers/site_element/site_elem_record.html', content)
    else:
        formset = SERFormSet(queryset=SiteElementRecord.objects.filter(element=current_element), )
        content = {
            'current_element': current_element,
            'records': records,
            'formset': formset,
            'elements': elements_links,
        }
        return render(request, 'helpers/site_element/site_elem_record.html', content)



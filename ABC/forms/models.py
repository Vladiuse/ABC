from django.db import models
from django.contrib import admin
from django.utils.html import format_html

from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavascriptLexer, CssLexer
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name

# Create your models here.

class OrderFormManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=FormExampleOLD.FORM)

class CasinoFormManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=FormExampleOLD.CASINO)


class CodeExample(models.Model):
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)

    image_url = models.URLField(blank=True)
    original_site =  models.URLField(blank=True)

    def get_colored_code(self, code, lexer):
        return highlight(code, lexer(encodings='utf-8'), HtmlFormatter())

    def html_colored(self):
        return self.get_colored_code(self.html, HtmlLexer)

    def css_colored(self):
        return self.get_colored_code(self.css, CssLexer)

    def js_colored(self):
        return self.get_colored_code(self.js, JavascriptLexer)

    def colored_styes(self):
        return HtmlFormatter(style=FormExampleOLD.COLORED_STYLE).get_style_defs('.highlight')

    @admin.display
    def image_prew(self):
        return format_html(
            '<img src="{}" / style="width:{}px;height: {}px">',
            self.image_url,
            80,80,
        )

class FormExample(CodeExample):
    COLORS = [
        ['black', 'Черный'],
        ['white', 'Белый'],
        ['grey', 'Серый'],
        ['blue', 'Синий'],
        ['pink', 'Розовый'],
        ['red', 'Красный'],
        ['yellow', 'Желтый'],
        ['green', 'Зеленый'],
    ]
    color = models.CharField(max_length=30,blank=True, choices=COLORS)


class CasinoExample(CodeExample):
    ROULETTE = 'roulette'
    BOX = 'box'
    OTHER = 'other'
    TYPES = [
        [ROULETTE, 'Рулетка'],
        [BOX, 'Коробки'],
        [OTHER, 'Прочее'],
    ]
    type = models.CharField(max_length=30, default=OTHER, choices=TYPES)



class FormExampleOLD(models.Model):
    FORM = 'form'
    CASINO = 'casino'
    FORM_TYPES = [
        (FORM, 'Форма заказа'),
        (CASINO, 'Розыгрышь'),
    ]

    COLORED_STYLE = 'gruvbox-dark'

    image_url = models.URLField(blank=True)
    type = models.CharField(max_length=50, default=FORM, choices=FORM_TYPES)
    url = models.URLField(blank=True)
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)

    objects = models.Manager()
    forms = OrderFormManager()
    casino = CasinoFormManager()


    def get_colored_code(self, code, lexer):
        return highlight(code, lexer(encodings='utf-8'), HtmlFormatter())

    def html_colored(self):
        return self.get_colored_code(self.html, HtmlLexer)

    def css_colored(self):
        return self.get_colored_code(self.css, CssLexer)

    def js_colored(self):
        return self.get_colored_code(self.js, JavascriptLexer)

    def colored_styes(self):
        return HtmlFormatter(style=FormExampleOLD.COLORED_STYLE).get_style_defs('.highlight')

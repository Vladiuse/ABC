from django.db import models


from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavascriptLexer, CssLexer
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name

# Create your models here.


class FormExample(models.Model):

    COLORED_STYLE = 'gruvbox-dark'

    image_url = models.URLField(blank=True)
    url = models.URLField(blank=True)
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)


    def get_colored_code(self, code, lexer):
        return highlight(code, lexer(encodings='utf-8'), HtmlFormatter())

    def html_colored(self):
        return self.get_colored_code(self.html, HtmlLexer)

    def css_colored(self):
        return self.get_colored_code(self.css, CssLexer)

    def js_colored(self):
        return self.get_colored_code(self.js, JavascriptLexer)

    def colored_styes(self):
        return HtmlFormatter(style=FormExample.COLORED_STYLE).get_style_defs('.highlight')

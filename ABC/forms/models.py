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

    def html_colored(self):
        lexer = HtmlLexer
        html_colored = highlight(self.html, lexer(encodings='utf-8'), HtmlFormatter())
        return html_colored

    def css_colored(self):
        lexer = CssLexer
        css_colored = highlight(self.css, lexer(encodings='utf-8'), HtmlFormatter())
        return css_colored

    def js_colored(self):
        lexer = CssLexer
        js_colored = highlight(self.js, lexer(encodings='utf-8'), HtmlFormatter())
        return js_colored

    def colored_styes(self):
        return HtmlFormatter(style=FormExample.COLORED_STYLE).get_style_defs('.highlight')

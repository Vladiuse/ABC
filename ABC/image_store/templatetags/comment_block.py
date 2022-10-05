from django import template
from django.template import loader


register = template.Library()

@register.tag
def comment_block(parser,token):
    return CommentBlock(parser)


class CommentBlock(template.Node):
    TEMPLATE_PATH = 'image_store/tags/comment_block.html'

    def __init__(self, parser):
        self.nodelist = parser.parse(('end',))
        parser.delete_first_token()

    def render(self, context):
        output = self.nodelist.render(context)
        image_link = output.strip()
        template = loader.get_template(self.TEMPLATE_PATH)
        output = template.render({'image_url': image_link})
        return output



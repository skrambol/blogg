from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from streams import blocks

class BlogIndexPage(Page):

    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPage.objects.live().public().order_by('-last_published_at')

        context['posts'] = posts

        return context;

class BlogPage(Page):
    content = StreamField(
        [
            ('section', blocks.SectionBlock()),
            ('image', blocks.ImageBlock())
        ],
        block_counts = {
            'section': {'min_num': 1}
        }
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    @property
    def is_modified(self):
        return self.first_published_at != self.last_published_at

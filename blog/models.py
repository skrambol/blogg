from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from streams import blocks

class BlogIndexPage(Page):
    max_count = 1

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

    @property
    def is_modified(self):
        return self.first_published_at != self.last_published_at

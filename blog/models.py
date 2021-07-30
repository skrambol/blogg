from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from streams import blocks

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPage.objects.live().public().order_by('-last_published_at')
        tags = request.GET.get('tag')

        if tags:
            posts = posts.filter(tags__slug__in=[tags])

        paginator = Paginator(posts, 3)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

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
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('tags'),
        StreamFieldPanel('content')
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    @property
    def is_modified(self):
        return self.first_published_at != self.last_published_at

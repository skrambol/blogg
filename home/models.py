from django.db import models

from wagtail.core.models import Page
from django.http.response import HttpResponseRedirect


class HomePage(Page):
    max_count = 1

    parent_page_types = []
    subpage_types = ['blog.BlogIndexPage']

    def serve(self, request):
        return HttpResponseRedirect('/blog-index')

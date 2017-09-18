from django.conf.urls import url

from .views import BlogPageServe

urlpatterns = [
    url(
        regex=r'^(?P<blog_path>[-\w\/]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=BlogPageServe.as_view(),
        name='blog_page_serve_slug'
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=BlogPageServe.as_view(),
        name='blog_page_serve'
    ),
]
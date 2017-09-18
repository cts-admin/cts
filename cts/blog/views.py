from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from wagtail.wagtailcore import hooks

from .utils import strip_prefix_and_ending_slash


class BlogPageServe(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        if not request.site:
            raise Http404
        if request.resolver_match.url_name == 'blog_page_serve_slug':
            # Splitting the request path and obtaining the path_components
            # this way allows you to place the blog at the level you want on
            # your sitemap.
            # Example:
            # splited_path =  ['es', 'blog', '2016', '06', '23', 'blog-entry']
            # slicing this way you obtain:
            # path_components =  ['es', 'blog', 'blog-entry']
            # with the oldest solution you'll get ['es', 'blog-entry']
            # and a 404 will be raised
            split_path = strip_prefix_and_ending_slash(request.path).split("/")
            path_components = split_path[:-4] + split_path[-1:]
        else:
            path_components = [strip_prefix_and_ending_slash(request.path).split('/')[-1]]
        page, args, kwargs = request.site.root_page.specific.route(request, path_components)

        for fn in hooks.get_hooks('before_serve_page'):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result
        return page.serve(request, *args, **kwargs)

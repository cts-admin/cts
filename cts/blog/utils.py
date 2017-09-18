from django.core.urlresolvers import reverse


def strip_prefix_and_ending_slash(path):
    return path.replace(reverse('wagtail_serve', args=[""]), '', 1).rstrip("/")

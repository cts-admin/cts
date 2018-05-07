from django.test import SimpleTestCase
from django.utils.safestring import SafeData

from .templatetags.markdown import markdownify


class MarkdownifyTests(SimpleTestCase):
    def test_str(self):
        result = markdownify('Line\n\n[Link](https://conservationtechnologysolutions.org)')
        self.assertEqual(
            result,
            '<p>Line</p>\n<p><a href="https://conservationtechnologysolutions.org">Link</a></p>',
        )
        self.assertIsInstance(result, SafeData)

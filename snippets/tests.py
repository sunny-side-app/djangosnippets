from django.test import TestCase
from django.urls import resolve
from snippets.views import top, snippet_new, snippet_edit, snippet_detail

class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_top_returns_expected_content(self):
        response = self.client.get('/')
        self.assertEqual(b'Hello World', response.content)

class CreateSnippetViewTest(TestCase):
    def test_should_resolve_snippet_new_view(self):
        found = resolve('/snippets/new/')
        self.assertEqual(found.func, snippet_new)

class DetailSnippetViewTest(TestCase):
    def test_should_resolve_snippet_detail_view(self):
        found = resolve('/snippets/1/')
        self.assertEqual(found.func, snippet_detail)

class EditSnippetViewTest(TestCase):
    def test_should_resolve_snippet_edit_view(self):
        found = resolve('/snippets/1/edit/')
        self.assertEqual(found.func, snippet_edit)
from urllib.parse import quote

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from wiki.models import Page
from .views import PageCreateView

class WikiTestSuite(TestCase):
    def test_identity(self):
        """canary test"""
        self.assertTrue(True)

    def test_page_slugify_on_save(self):
        """slug should be generated on saving a Page"""
        user = User()
        user.save()

        page = Page(title="Test Page", content="test content", author=user)
        page.save()

        self.assertEqual(page.slug, "test-page")


class PageListViewTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        Page.objects.create(title="Test Page",
                            content="test content",
                            author=self.user)
        Page.objects.create(title="Second Test Page",
                            content="test content",
                            author=self.user)

    def test_multiple_pages(self):
        res = self.client.get("/")

        self.assertEqual(res.status_code, 200)
        pages = res.context["pages"]
        self.assertEqual(len(pages), 2)

        self.assertQuerysetEqual(
            pages, ["<Page: Test Page>", "<Page: Second Test Page>"],
            ordered=False)


class PageDetailViewTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        Page.objects.create(title="Test Page",
                            content="test content",
                            author=self.user)
        Page.objects.create(title="Second Test Page",
                            content="test content",
                            author=self.user)

    def test_detail_page_load_success(self):
        res = self.client.get("/test-page/")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/second-test-page/")
        self.assertEqual(res.status_code, 200)


class WikiPageCRUDTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create()

    def test_creation_form_load_successful(self):
        res = self.client.get(reverse("wiki-create-page"))
        self.assertEqual(res.status_code, 200)

    def test_create_view(self):
        form_data = {
            "title": "It's a Test Page",
            "content": "It's some test content",
            "author": self.user.id
        }
        pcv = PageCreateView(data=form_data)
        self.assertEqual(len(Page.objects.all()), 1)

    def test_create_page(self):
        form_data = {
            "title": "It's a Test Page",
            "content": "It's some test content",
            "author": self.user.id
        }
        res = self.client.post(reverse("wiki-create-page"), form_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(Page.objects.all()), 1)

        res = self.client.get(reverse("wiki-list-page"))

        # check that our new page exists on home
        self.assertIn(b"It's a test page", res.content)

        res = self.client.get(quote("It's-a-test-page"))
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"It's a test page", res.content)
        #self.assertIn(b")

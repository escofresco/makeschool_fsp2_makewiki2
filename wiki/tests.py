from django.test import TestCase
from django.contrib.auth.models import User

from wiki.models import Page


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
    def test_multiple_pages(self):
        user = User.objects.create()
        Page.objects.create(title="Test Page",
                            content="test content",
                            author=user)
        Page.objects.create(title="Second Test Page",
                            content="test content",
                            author=user)
        res = self.client.get("/")

        self.assertEqual(res.status_code, 200)
        pages = res.context["pages"]
        self.assertEqual(len(pages), 2)

        self.assertQuerysetEqual(
            pages, ["<Page: Test Page>", "<Page: Second Test Page>"],
            ordered=False)

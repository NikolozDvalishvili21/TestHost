# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wagtail.images.tests.utils import get_test_image_file
from wagtail.images.models import Image
from .models import BlogPage


class BlogPageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file()
        )
        self.blog_page = BlogPage.objects.create(
            title="Test Blog",
            body="<p>This is a test blog post.</p>",
            featured_image=self.image,
            category="Test Category",
            dot="Test Dot"
        )
        self.blog_page_url = reverse('blog-posts-detail', args=[self.blog_page.id])
        self.blog_page_list_url = reverse('blog-posts-list')

    def test_get_blog_page_list(self):
        response = self.client.get(self.blog_page_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_blog_page_detail(self):
        response = self.client.get(self.blog_page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Blog")

    def test_create_blog_page(self):
        data = {
            "title": "New Test Blog",
            "body": "<p>This is another test blog post.</p>",
            "featured_image": self.image.pk,
            "category": "New Category",
            "dot": "New Dot"
        }
        response = self.client.post(self.blog_page_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPage.objects.count(), 2)

    def test_update_blog_page(self):
        data = {
            "title": "Updated Test Blog",
            "body": "<p>This is an updated test blog post.</p>",
            "featured_image": self.image.pk,
            "category": "Updated Category",
            "dot": "Updated Dot"
        }
        response = self.client.put(self.blog_page_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_page.refresh_from_db()
        self.assertEqual(self.blog_page.title, "Updated Test Blog")

    def test_delete_blog_page(self):
        response = self.client.delete(self.blog_page_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPage.objects.count(), 0)

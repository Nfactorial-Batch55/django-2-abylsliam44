from django.test import TestCase
from .models import News, Comment

class NewsModelTest(TestCase):

    def setUp(self):
        self.news_with_comments = News.objects.create(title="Test News 1", content="Test content 1")
        self.news_without_comments = News.objects.create(title="Test News 2", content="Test content 2")
        Comment.objects.create(news=self.news_with_comments, content="Test comment")

    def test_has_comments_true(self):
        self.assertTrue(self.news_with_comments.has_comments())

    def test_has_comments_false(self):
        self.assertFalse(self.news_without_comments.has_comments())


from django.urls import reverse

class NewsViewsTest(TestCase):

    def setUp(self):
        News.objects.create(title="Older News", content="Older content")
        News.objects.create(title="Newer News", content="Newer content")

    def test_news_list_order(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        news_list = response.context['news']
        self.assertEqual(news_list[0].title, "Newer News")
        self.assertEqual(news_list[1].title, "Older News")



class NewsDetailViewTest(TestCase):

    def setUp(self):
        self.news = News.objects.create(title="Test News", content="Test Content")
        self.comment = Comment.objects.create(news=self.news, content="Test Comment")

    def test_news_detail_view(self):
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        self.assertContains(response, self.news.content)

    def test_news_comments_order(self):
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        comments = response.context['comments']
        self.assertEqual(comments[0].content, "Test Comment")

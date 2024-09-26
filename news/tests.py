from django.test import TestCase
from django.urls import reverse
from .models import News, Comment
from django.utils import timezone

class NewsModelTest(TestCase):
    def setUp(self):
        
        self.news_with_comments = News.objects.create(title="News with Comments", content="Content with comments")
        self.news_without_comments = News.objects.create(title="News without Comments", content="Content without comments")
        
        
        Comment.objects.create(news=self.news_with_comments, content="This is a comment")

    def test_has_comments_true(self):

        self.assertTrue(self.news_with_comments.has_comments())

    def test_has_comments_false(self):
        
        self.assertFalse(self.news_without_comments.has_comments())


class NewsViewsTest(TestCase):
    def setUp(self):
        
        self.news1 = News.objects.create(title="Older News", content="Content 1", created_at=timezone.now())
        self.news2 = News.objects.create(title="Newer News", content="Content 2", created_at=timezone.now() + timezone.timedelta(hours=1))
        
        
        self.news_with_comments = News.objects.create(title="News with Comments", content="Content")
        
        
        Comment.objects.create(news=self.news_with_comments, content="First comment", created_at=timezone.now())
        Comment.objects.create(news=self.news_with_comments, content="Second comment", created_at=timezone.now() + timezone.timedelta(minutes=10))

    def test_news_list_order(self):
        
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        news_list = response.context['news']
        self.assertEqual(news_list[0].title, "Newer News")
        self.assertEqual(news_list[1].title, "Older News")

    def test_news_detail_view(self):
        
        response = self.client.get(reverse('news_detail', args=[self.news_with_comments.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news_with_comments.title)
        self.assertContains(response, self.news_with_comments.content)

    def test_news_comments_order(self):
        
        response = self.client.get(reverse('news_detail', args=[self.news_with_comments.id]))
        comments = response.context['comments']
        self.assertEqual(comments[0].content, "Second comment")
        self.assertEqual(comments[1].content, "First comment")


class AdminCustomTest(TestCase):
    def setUp(self):
        
        self.news = News.objects.create(title="Test News", content="Test Content")

    def test_admin_display(self):

        self.assertFalse(self.news.has_comments())

        
        Comment.objects.create(news=self.news, content="This is a comment")
        self.assertTrue(self.news.has_comments())

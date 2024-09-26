
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import News, Comment
from .forms import NewsForm, CommentForm


def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = news.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.created_at = timezone.now()
            comment.save()
            return redirect('news_detail', news_id=news.id)
    else:
        comment_form = CommentForm()

    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'comment_form': comment_form
    })


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_at = timezone.now()
            news.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/news_create.html', {'form': form})

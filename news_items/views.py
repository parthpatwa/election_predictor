from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Article, Feed, Query
from authentication.models import Usertype
from .forms import FeedForm
from django.shortcuts import redirect
import ssl
import feedparser
import datetime


# Create your views here.
@login_required
def articles_list(request):
    articles = Article.objects.filter(feed__query__query_fk__user=request.user)

    rows = [articles[x:x+1] for x in range(0, len(articles), 1)]

    return render(request, 'news_items/articles_list.html', {'rows': rows})


@login_required
def feeds_list(request):
    feeds = Feed.objects.filter(query__query_fk__user=request.user)
    return render(request, 'news_items/feeds_list.html', {'feeds': feeds})


@login_required
def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        k = Feed.objects.filter(query__query=form.data['query'])
        k.delete()
        l = Query.objects.filter(query=form.data['query'])
        l.delete()

        if form.is_valid():
            feed = form.save(commit=False)
            q = feed.query
            url = "https://news.google.com/rss/search?cf=all&pz=1&q="+q+"&hl=en-US&gl=US&ceid=US:en"
            existingFeed = Feed.objects.filter(url=url)
            que = Query()
            que.query = feed.query
            que.query_fk = Usertype.objects.get(user=request.user)
            feed = Feed()
            feed.url = url
            if len(existingFeed) == 0:
                if hasattr(ssl, '_create_unverified_context'):
                    ssl._create_default_https_context = ssl._create_unverified_context
                feedData = feedparser.parse(feed.url)
                # set some fields
                feed.title = feedData.feed.title
                feed.query = que
                que.save()
                feed.save()

                for entry in feedData.entries:
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = dateString
                    article.feed = feed
                    article.save()
            articles = Article.objects.filter(feed__url=url)
            rows = [articles[x:x + 1] for x in range(0, len(articles), 1)]
            return render(request, 'news_items/search_results.html', {'rows': rows})
    else:
        form = FeedForm()
    return render(request, 'news_items/new_feed.html', {'form': form})


@login_required
def saved_queries(request):
    if request.method == "POST":
        query = request.POST.get('delete')
        if query:
            f = Article.objects.filter(feed__query__query=query)
            f.delete()
            a = Feed.objects.filter(query__query=query)
            a.delete()
            r = Query.objects.filter(query=query)
            r.delete()

    savedqps = Query.objects.filter(query_fk__user=request.user)
    return render(request, 'news_items/queries_saved.html', {'savedqps': savedqps})
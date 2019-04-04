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
from django.db import connection

# Create your views here.
@login_required
def articles_list(request):
    #articles = Article.objects.filter(feed__query__query_fk__user=request.user)
    if request.method == "POST": 
        que = "SELECT 'news_items_article'.'id', 'news_items_article'.'feed_id', 'news_items_article'.'title', 'news_items_article'.'url', 'news_items_article'.'description', 'news_items_article'.'publication_date' FROM 'news_items_article' INNER JOIN 'news_items_feed' ON ('news_items_article'.'feed_id' = 'news_items_feed'.'id') INNER JOIN 'news_items_query' ON ('news_items_feed'.'query_id' = 'news_items_query'.'query') WHERE 'news_items_query'.'query_fk_id' =" +request.user+";"
#    f = open("queries.txt",'a')
#    f.write('articles_list'+ str(articles.query))
#    f.close()
        with connection.cursor() as cursor:
            cursor.execute(que)
            articles = cursor.fetchall()
        rows = [ut[x:x+1] for x in range(0, len(articles), 1)]

        return render(request, 'news_items/articles_list.html', {'rows': rows})
    else:
        return render(request, 'news_items/articles_list.html', {'rows': None})

@login_required
def feeds_list(request):#1
    feeds = Feed.objects.filter(query__query_fk__user=request.user)
    return render(request, 'news_items/feeds_list.html', {'feeds': feeds})


@login_required
def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        k = Feed.objects.filter(query__query=form.data['query'])
        k.delete()#2
        l = Query.objects.filter(query=form.data['query'])
        l.delete()#2

        if form.is_valid():
            feed = form.save(commit=False)
            q = feed.query
            url = "https://news.google.com/rss/search?cf=all&pz=1&q="+q+"&hl=en-US&gl=US&ceid=US:en"
            existingFeed = Feed.objects.filter(url=url)#4
            que = Query()
            que.query = feed.query
            que.query_fk = Usertype.objects.get(user=request.user)#5
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
            articles = Article.objects.filter(feed__url=url)#6
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
            f.delete()#7
            a = Feed.objects.filter(query__query=query)
            a.delete()#8
            r = Query.objects.filter(query=query)
            r.delete()#9

    savedqps = Query.objects.filter(query_fk__user=request.user)#10
    return render(request, 'news_items/queries_saved.html', {'savedqps': savedqps})

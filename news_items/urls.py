from django.conf.urls import url
from . import views

app_name = 'news_items'

urlpatterns = [
    url(r'^$', views.articles_list, name='articles_list'),
    url(r'^feeds/new', views.new_feed, name='feed_new'),
    url(r'^feeds/', views.feeds_list, name='feeds_list'),
    url(r'^saved_queries', views.saved_queries, name='saved_queries'),
]

from django.db import models
from authentication.models import Usertype
# Create your models here.


class Query(models.Model):
    query = models.CharField(max_length=200, primary_key=True)
    query_fk = models.ForeignKey(Usertype, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.query


class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title

from django.db import models
from authentication.models import Party


class Group(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=200)
    admin_id = models.ForeignKey(Party, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'admin_id')

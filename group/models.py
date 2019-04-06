from django.db import models
from authentication.models import Party, Profile


class Group(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=5000)
    admin_id = models.ForeignKey(Party, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'admin_id')


class Group_members(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


days_choices = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class Event(models.Model):
    name = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=200)
    location = models.CharField(max_length=100)
    date = models.DateField()
    day = models.CharField(max_length=15, choices=days_choices)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'group_id')

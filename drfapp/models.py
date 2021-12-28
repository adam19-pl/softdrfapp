from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATUS = ((0, 'new'), (1, 'in-progress'))


class Project(models.Model):
    owner = models.ForeignKey('auth.User', related_name='projects', on_delete=models.CASCADE, )
    title = models.CharField(blank=False, null=False, max_length=256)
    description = models.TextField(blank=False, null=False, )
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(default=None, null=True)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=256)
    employers = models.ManyToManyField(User, related_name='employers', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='project', on_delete=models.CASCADE)
    autor = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True, )

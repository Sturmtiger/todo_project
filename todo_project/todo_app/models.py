from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from time import time
from django.shortcuts import reverse
from django.db import connection
# Create your models here.


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Project(models.Model):
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=7)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'colour', 'user')

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Task(models.Model):
    LOW = 3
    MID = 2
    HIGH = 1
    CHOICES_OF_PRIORITY = (
        (LOW, 'Low'),
        (MID, 'Mid'),
        (HIGH, 'High')
    )
    name = models.CharField(max_length=30)
    priority = models.PositiveSmallIntegerField(choices=CHOICES_OF_PRIORITY, default=LOW)
    date_until = models.DateTimeField()
    status = models.CharField(max_length=4, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


class Project(models.Model):
    name = models.CharField(max_length=30, unique=True)
    colour = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    CHOICES_OF_PRIORITY = (
        ('red', 'High'),
        ('orange', 'Mid'),
        ('white', 'Low')
    )
    name = models.CharField(max_length=30)
    priority = models.CharField(max_length=6, choices=CHOICES_OF_PRIORITY)
    date_until = models.DateTimeField()
    status = models.CharField(max_length=4, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
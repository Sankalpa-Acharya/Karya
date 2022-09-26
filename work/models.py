from email.policy import default
from venv import create
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid


# Create your models here.
task_status = (
    ('undone', 'undone'),
    ('working', 'working'),
    ('blocked', 'blocked'),
    ('done', 'done'),
    ('today', 'today')
)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=150, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pic',
        blank=True,
        default='profile_pic/Karya.png')
    created_at = models.DateTimeField(auto_now_add=True)
    github = models.URLField(max_length=300, null=True, blank=True)
    twitter = models.URLField(max_length=300, null=True, blank=True)
    linkedin = models.URLField(max_length=300, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    is_complete = models.BooleanField(default=False)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


class Card(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=7,
        choices=task_status,
        default='undone')
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Card, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class History(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=7,
        choices=task_status,
        default='undone')
    date = models.DateTimeField(auto_now_add=True)


class InviteLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

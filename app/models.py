from django.db import models
from django.contrib.auth.models import User
from app.managers import AnswerManager, _CustomTagManager
from taggit.managers import TaggableManager
from django.urls import reverse
from gbosa.settings import SITE_URL
from datetime import datetime

# Create your models here.

class PsuedoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    avatar = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=8)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)

class Region(models.Model):
    ip = models.GenericIPAddressField()
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country_name = models.CharField(max_length=128, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class View(models.Model):
    ip = models.GenericIPAddressField()
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country_name = models.CharField(max_length=128, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.TextField(db_index=True)
    likes = models.ManyToManyField(Upvote, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_anonymous = models.BooleanField(default=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.comment

class Answer(models.Model):
    answer = models.TextField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comments = models.ManyToManyField(Comment)
    views = models.ManyToManyField(View)
    upvotes = models.ManyToManyField(Upvote)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    objects = models.Manager()
    by_upvotes = AnswerManager()

    def __str__(self):
        return self.answer

class Post(models.Model):
    TYPE_CHOICES = (
        ('Q', 'Question'),
        ('E', 'Experience')
    )
    FLAG_CHOICES = (
        ('offensive', 'Offensive'),
        ('abusive', 'Abusive'),
        ('lacks-credibility', 'Lacks Credibility')
    )
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True, blank=True)
    description = models.TextField(db_index=True, blank=True, null=True)
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='Q', null=False)
    is_anonymous = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answers = models.ManyToManyField(Answer, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    views = models.ManyToManyField(View, blank=True)
    subscribers = models.ManyToManyField(Subscribe, blank=True)
    upvotes = models.ManyToManyField(Upvote, blank=True)
    tags = TaggableManager(manager=_CustomTagManager)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    is_flagged = models.BooleanField(default=False)
    flagged_reason = models.CharField(max_length=18, choices=FLAG_CHOICES, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app:view-post', kwargs={'pk': self.pk, 'slug':self.slug})

    def get_relative_url(self):
        return ''.join([ SITE_URL, reverse('app:view-post', kwargs={'pk': self.pk, 'slug':self.slug})])

    def user_subscribed(self):
        if self.user.is_authenticated:
            try:
                return Subscribe.objects.filter(user=self.user, post__pk=self.pk).first()
            except:
                print('Not Found In Model!!!')

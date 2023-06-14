from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rate = Post.objects.filter(author_id=self.pk).aggregate(sum_post=Coalesce(Sum('rating') * 3, 0))['sum_post']
        comments_rate = Comment.objects.filter(user_id=self.user).aggregate(sum_comment=Coalesce(Sum('rating'), 0))['sum_comment']
        comments_post_rate = Comment.objects.filter(post__author__user=self.user).aggregate(sum_comment=Coalesce(Sum('rating'), 0))['sum_comment']
        self.rating = post_rate + comments_rate + comments_post_rate
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    news = 'news'
    post = 'post'

    CHOICES = [
        (news, 'Новости'),
        (post, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=CHOICES)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

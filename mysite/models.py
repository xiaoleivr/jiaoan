from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from uuslug import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    following = models.ManyToManyField('self', through='Contact',
                                       related_name='followers',
                                       symmetrical=False)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    intro = models.CharField(max_length=250, blank=True)

    def get_absolute_url(self):
        return reverse('pro_detail', kwargs={
            'pk': self.pk
        })

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                  related_name='user_from_set')
    user_to = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='user_to_set')
    created = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    """
    文章分类
    """
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    文章表
    """
    STATUS_CHOICES = (
        (-1, "删除"),
        (0, '草稿'),
        (1, '发表'),
        (2, '热门'),
        (3, '推荐'),
    )
    title = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pro_posts')
    slug = models.SlugField(max_length=250, unique_for_date='publish', default="1")
    clicks = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(max_length=10, choices=STATUS_CHOICES, default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])

    def increase_views(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField(verbose_name='评论内容')

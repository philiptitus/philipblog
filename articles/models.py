from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
import markdown
from django.urls import reverse
from django.contrib.auth.models import User as U

User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=265)
    message = models.TextField(max_length=264)
    image = models.ImageField(upload_to='articles/', default='swift.jpg')
    user = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="articles", on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = markdown.markdown(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:single', kwargs={'username': self.user.username, 'pk': self.pk})

    @property
    def total_likes(self):
        return Like.objects.filter(article=self).count()

    class Meta:
        ordering = ['-created_date']
        unique_together = ('user', 'message')

    @property
    def total_bookmarks(self):
        return Bookmark.objects.filter(article=self).count()

    class Meta:
        ordering = ['-created_date']
        unique_together = ('user', 'message')

class Like(models.Model):
    liker = models.ForeignKey(U, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Bookmark(models.Model):
    booker = models.ForeignKey(U, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

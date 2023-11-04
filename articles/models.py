from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
import markdown
from django.urls import reverse


User = get_user_model()

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=265)
    message = models.TextField(max_length=264)
    user = models.ForeignKey(User,related_name="articles",on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group,related_name="articles",on_delete=models.CASCADE)


    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        self.message_html = markdown.markdown(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('articles:single',
                       kwargs={'username': self.user.username,
                               'pk':self.pk}
                       )
    class Meta:
        ordering = ['-created_date']
        unique_together = ('user','message')
    
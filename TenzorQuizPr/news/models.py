from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/%Y-%m-%d/', blank=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

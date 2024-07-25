from django.db import models


class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='news/%Y-%m-%d/', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

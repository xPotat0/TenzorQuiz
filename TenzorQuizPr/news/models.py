from django.db import models
from games.models import Game

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news/%Y-%m-%d/', blank=True)
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
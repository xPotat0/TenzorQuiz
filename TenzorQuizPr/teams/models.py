from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    captain_id = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(default=0.0, blank=True)
    is_available = models.BooleanField(default=True)
    played_games_count = models.IntegerField(default=0, blank=True)
    members_count = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.name
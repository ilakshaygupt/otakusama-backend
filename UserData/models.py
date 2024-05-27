from django.db import models

# Create your models here.


from authentication.models import User

class Manga(models.Model):
    manga_id = models.BigAutoField(primary_key=True)
    manga_title = models.CharField(max_length=100)
    manga_url = models.CharField(max_length=100)
    manga_image = models.CharField(max_length=100)

    def __str__(self):
        return self.manga_title
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favouriteMangas = models.ManyToManyField(Manga, blank=True, null=True)

    def __str__(self):
        return self.user.username

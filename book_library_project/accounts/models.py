from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Біографія")
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name="Аватар")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    favorite_genre = models.CharField(max_length=50, blank=True, verbose_name="Улюблений жанр")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return f"Профіль {self.user.username}"
    

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.save(user = instance)

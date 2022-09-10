from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Card(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.username + " - " + self.name + " - " + str(self.date)[:16]

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserUpgrade(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='media/profile-img/', default="media/profile-img/person-icon.png")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Расширение'
        verbose_name_plural = 'Расширения'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserUpgrade.objects.create(user=instance)

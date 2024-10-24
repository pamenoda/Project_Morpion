from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Crée un profil associé à l'utilisateur lors de la création de l'utilisateur
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Sauvegarde le profil associé à l'utilisateur lors de la sauvegarde de l'utilisateur
    instance.profile.save()

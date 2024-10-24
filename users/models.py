from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    # Modèle de profil utilisateur avec une relation OneToOne vers le modèle User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    symbol = models.ImageField(default='ic_coin.png',upload_to='symbole_pics')

    def __str__(self):
        # Méthode pour afficher une représentation lisible du profil
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Méthode pour sauvegarder le profil et redimensionner l'image si nécessaire
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        symbol = Image.open(self.symbol.path)
        # Redimensionne l'image si elle est plus grande que 300x300 pixels
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        # Redimensionne l'image du symbole si elle est plus grande que 40x40 pixels
        if symbol.height > 50 or symbol.width > 50:
            output_size_symbol = (50, 50)
            symbol.thumbnail(output_size_symbol)
            symbol.save(self.symbol.path)
        
from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True,
                              upload_to='pokemon_images/')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

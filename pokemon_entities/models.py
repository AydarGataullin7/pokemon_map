from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True,
                              upload_to='pokemon_images/')
    description = models.TextField(blank=True)
    title_jp = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)

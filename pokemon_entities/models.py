from django.db import models


class Pokemon(models.Model):
    title = models.CharField("Название", max_length=200)
    image = models.ImageField("Изображение", null=True, blank=True,
                              upload_to='pokemon_images/')
    description = models.TextField("Описание", blank=True)
    title_jp = models.CharField(
        "Название на японском", max_length=200, blank=True)
    title_en = models.CharField(
        "Название на английском", max_length=200, blank=True)
    previous_evolution = models.ForeignKey("Pokemon", on_delete=models.SET_NULL, null=True,
                                           blank=True, related_name='next_evolutions', verbose_name="Из кого эволюционировал")

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name="entities")
    appeared_at = models.DateTimeField("Время появления")
    disappeared_at = models.DateTimeField("Время исчезновения")
    level = models.IntegerField("Уровень", null=True, blank=True)
    health = models.IntegerField("Здоровье", null=True, blank=True)
    strength = models.IntegerField("Сила", null=True, blank=True)
    defence = models.IntegerField("Защита", null=True, blank=True)
    stamina = models.IntegerField("Выносливость", null=True, blank=True)

    class Meta:
        verbose_name = "Экземпляр покемона"
        verbose_name_plural = "Экземпляры покемонов"

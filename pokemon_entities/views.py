import folium
import json
import time

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now, disappeared_at__gte=now)
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        if entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, entity.latitude,
            entity.longitude,
            img_url
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if pokemon.image:
        img_url = request.build_absolute_uri(pokemon.image.url)
    else:
        img_url = DEFAULT_IMAGE_URL

    now = localtime()
    pokemon_entities = pokemon.pokemonentity_set.filter(
        appeared_at__lte=now, disappeared_at__gte=now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        add_pokemon(
            folium_map, entity.latitude,
            entity.longitude,
            img_url
        )

    previous_evolution = None
    if pokemon.previous_evolution:
        if pokemon.previous_evolution.image:
            previous_img_url = request.build_absolute_uri(
                pokemon.previous_evolution.image.url)
        else:
            previous_img_url = DEFAULT_IMAGE_URL

        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': previous_img_url
        }

    next_evolution = None
    next_evolutions_qs = pokemon.next_evolutions.all()
    if next_evolutions_qs.exists():
        next_pokemon = next_evolutions_qs.first()
        if next_pokemon.image:
            next_img_url = request.build_absolute_uri(next_pokemon.image.url)
        else:
            next_img_url = DEFAULT_IMAGE_URL

        next_evolution = {
            'title_ru': next_pokemon.title,
            'pokemon_id': next_pokemon.id,
            'img_url': next_img_url
        }

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'img_url': img_url if pokemon.image else DEFAULT_IMAGE_URL,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })

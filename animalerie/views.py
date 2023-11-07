from django.shortcuts import render
from .models import Equipement, Character

def pokemon_list(request):
    pokemons = Character.objects.all()
    return render(request, 'animalerie/pokemon_list.html', {'pokemons': pokemons})

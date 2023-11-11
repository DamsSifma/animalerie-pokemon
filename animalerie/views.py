from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement, Character

def character_list(request):
    pokemons = Character.objects.all()
    return render(request, 'animalerie/pokemon_list.html', {'characters': pokemons})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            form.save()
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
        return render(request,
                    'animalerie/character_detail.html',
                    {'character': character, 'lieu': character.lieu, 'form': form})
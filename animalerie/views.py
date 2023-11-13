from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement, Character

def character_list(request):
    pokemons = Character.objects.all()
    return render(request, 'animalerie/pokemon_list.html', {'characters': pokemons})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        # print("ancien lieu : ", ancien_lieu)
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            form.save(commit="False")
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            # print("nouveau lieu : ", nouveau_lieu)
            # print("dispo : ", nouveau_lieu.disponibilite)
            if nouveau_lieu.disponibilite == "libre":
                nombre_lieu = Character.objects.filter(lieu=nouveau_lieu).count()
                # print("nombre dans le lieu : ", nombre_lieu)
                if nombre_lieu > nouveau_lieu.taille_max - 1: # On regarde si le lieu se rempli
                    nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
            else:
                character.lieu = ancien_lieu
                character.save()
                occupants = Character.objects.filter(lieu=nouveau_lieu)
                occupants_names = ", ".join([o.id_character for o in occupants])
                print(occupants_names)
                message = f"Le lieu est occupé par {occupants_names}"
                return render(request, 'animalerie/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message})
                

                
            return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
        return render(request,
                    'animalerie/character_detail.html',
                    {'character': character, 'lieu': character.lieu, 'form': form})
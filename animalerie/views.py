from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement, Character
from random import randint

def character_list(request):
    pokemons = Character.objects.all()
    return render(request, 'animalerie/pokemon_list.html', {'characters': pokemons})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    # print("ancien lieu : ", ancien_lieu)
    characters_dans_lieu = Character.objects.filter(lieu=ancien_lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            form.save(commit="False")
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            if nouveau_lieu == ancien_lieu:
                message = f"{character.id_character} est déjà dans ce lieu"
                return render(request, 'animalerie/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
            print("nouveau_lieu : ", nouveau_lieu)

            if nouveau_lieu.disponibilite == "libre":
                print("nouveau lieu est bien libre")
                nombre_lieu = Character.objects.filter(lieu=nouveau_lieu).count()
                print(character.etat != "repu")
                print("arene", nouveau_lieu == "arene")

                # Si il n'est pas en état d'aller dans l'arène
                if nouveau_lieu.id_equip == "arene" and character.etat != "repu":
                    print("n'est pas en état d'aller dans l'arène")
                    message = f"{character.id_character} n'est pas en état pour aller dans l'arène"
                    return render(request, 'animalerie/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
                
                # Il va aller dans le nouveau lieu
                if nombre_lieu > nouveau_lieu.taille_max - 1: # On regarde si le lieu se rempli (en comptant le nouveau personnage)
                    print("on est dans le if")
                    nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

                # si il est repu et dans l'arene
                print("nouveau_lieu : " + nouveau_lieu.id_equip)
                if nouveau_lieu.id_equip == "arene" and character.etat == "repu":
                    if randint(0, 1):
                        character.etat = "fatigué"
                    else:
                        character.etat = "blessé"
                    character.save()

                # si il est fatigué et dans le nid
                elif nouveau_lieu.id_equip == "nid" and character.etat == "fatigué":
                    character.etat = "affamé"
                    character.save()

                # si il est blessé et dans l'infirmerie
                elif nouveau_lieu.id_equip == "infirmerie" and character.etat == "blessé":
                    character.etat = "affamé"
                    character.save()
                elif nouveau_lieu.id_equip == "mangeoire" and character.etat == "affamé":
                    character.etat = "repu"
                    character.save()

            else:
                character.lieu = ancien_lieu
                character.save()
                occupants = Character.objects.filter(lieu=nouveau_lieu)
                occupants_names = ", ".join([o.id_character for o in occupants])
                print(occupants_names)
                message = f"Le lieu est déjà occupé par {occupants_names}"
                return render(request, 'animalerie/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
                

                
            return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
        return render(request,
                    'animalerie/character_detail.html',
                    {'character': character, 'lieu': character.lieu, 'form': form, 'characters_dans_lieu': characters_dans_lieu})
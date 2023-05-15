import random
import requests
from datetime import date

# BdD : lits - operations - booking ( avec nom patient | date oeration etc... )
# on commence par un test sur un mois de 30 jours
# 2 types de couchage : lit ( arrivee a l'hopital la veille de l'operation ) / ambulatoire ( pour le jour de l'opération )


#DONNE REÇU PAR LE FRONTEND
saisieMedicin = {
                "age": 10,    
                "entree": date(1996, 12, 11),
                "nomChirurgien":"Thomas",
                "diagnostic": "BFGA427",
                "actePrevu":"coloscopie"
                }

#REQUEST IA
responseIA = 3 # = nb_jour_planning

nb_jour_planning = 10
occupation = [0] * nb_jour_planning
nb_lits = [0] * nb_jour_planning   # nb arbritaire de lits totaux dispos, a adapter # a faire varier !
nb_blocs = [0] * nb_jour_planning     # nb arbritaire de blocs dispos, sans prendre en compte de quelconque marge pour les urgences pour le moment
seuil = [0] * nb_jour_planning # seuil de 1 à 4 pour la couleur des cases + 0 pour 'pas de bloc' le jour de l'operation + ajouter 10 / 20 / 30 / 40 selon la dispo des deambulatoires
classement = [0] * 10 # liste des 10 meilleurs jours pour l'algo


#REQUEST API
#verifier nombre des lits dispo pour chaque jour - les dates
#quantité des lits max est de 105
""" r = requests.get('https://inputhc.onxzy.dev/api/NIGHT/LIST')

reponse = r.json()[0]
print(reponse.get('name')) 


"""
#Verifier la quantité de place par bloc pour chaque maladie par jour - les dates et la maladie 
""" r = requests.get('https://inputhc.onxzy.dev/api/disease/find')

print(r.json())
reponse = r.json()[0]
print(reponse.get('name')) 


"""
#fonction pour creer la reservation de l'operation - les dates + operation 
#verifier combien de sejours on a dans une periode (/operations)


#frontend ajouter une place pour mettre la date qu'on veut chercher l'operation
#	il faut avoir une minimum ou standart de 60 jours +-








""" for i in range(nb_jour_planning):
    nb_lits[i] = random.randint(80,120)  # remplissage aleatoire du nombre de lits fournis par l'hosto

for i in range(nb_jour_planning):
    occupation[i] = random.randint(20,nb_lits[i])  # remplissage aleatoire des lits dispos dans le planning

for i in range(nb_jour_planning):
    nb_blocs[i] = random.randint(0,7)  # remplissage aleatoire blocs dispos dans le planning

for i in range(nb_jour_planning):
    nb_ambulatoires[i] = random.randint(2,7) """



def generation_seuil():

    for i in range(nb_jour_planning): # chaque date d'entree a l'hosto => un jour de trop grande contrainte ?
        if nb_blocs[i] == 0 and i != 0:  # eviter la sortie de tableau
            seuil[i-1] = 0

        else:
            for j in range(estimation_convalescence):   # pendant la convalescence estimée -> jour rouge ?
                if i+j < nb_jour_planning:   # sinon on depasse la capacite du planning
                    if occupation[i+j] <= 0.8 * nb_lits[i+j] and seuil[i] < 1:
                        seuil[i] = 1
                    elif 0.8 * nb_lits[i+j] < occupation[i+j] <= 0.95 * nb_lits[i+j] and seuil[i] < 2:
                        seuil[i] = 2
                    elif 0.95 * nb_lits[i+j] < occupation[i+j] <= nb_lits[i+j] and seuil[i] < 3:
                        seuil[i] = 3
                    elif occupation[i+j] > nb_lits[i+j]:
                        seuil[i] = 4

def generation_classement():
    score = [0] * 10   # score grand = meilleur choix # a classer par ordre decroissant ( important )
    s = 0 # score local
    for i in range(nb_jour_planning):
        if seuil[i] != 0:# un bloc est dispo le lendemain pour l'operation
            for j in range(estimation_convalescence):
                if i+j < nb_jour_planning: # eviter une sortie de tableau
                    s = s + 1/((occupation[i+j] / nb_lits[i+j])+1)

            for k in range(10) :     # on acutalise le classement
                if score[k] < s:
                    classement[k] = i+1
                    score[k] = s
                    break            # ne pas changer plusieurs elements du tableau ( verifier ! )
        print(classement)

changement_jour = input("jour suivant ? [y/n] ")

if changement_jour == 'y':
    for i in range(nb_jour_planning - 1):
        occupation[i] = occupation[i+1]
    occupation[len(occupation) - 1] = 0 # il faut prevoir large pour que tous les changements soient dans la plage de nb_jour_planning

estimation_convalescence = int(input("Resultat de l'IA -> estimation du nombre de jours de convalescence post-opération : "))

generation_seuil()
print("---------------------")
generation_classement()
print("----------------------")

print("Seuils : ")
print(seuil)
print("Classement : ")
print(classement)
print("Nbre de blocs dispos : ")
print(nb_blocs)
print("Nbre de lits occupés : ")
print(occupation)
print("Nbre de lits fournis : ")
print(nb_lits)

jour_reservation = int(input("jour de la reservation : "))

# Actualisation du planning

nb_blocs[i] = nb_blocs[i] + 1
for j in range(estimation_convalescence):
    occupation[jour_reservation-1+j] = occupation[jour_reservation-1+j] + 1

print("Nombre de lits occupés après réservation : ")
print(occupation)

generation_seuil()

print("Actualisation des seuils : ")
print(seuil)
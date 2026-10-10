import sys
import time
from features.pwd import deletUser, login, modifierProfil, register, printUsers, donnerCodeSecret
from features.tool import *

# Temps exprimer en seconde
_Waiting_Time = 1.5

def home(user,cnx):
  while(1):
    print("""         
┌───────────────────────────────────────────────┐
│  /$$      /$$                                 │
│ | $$$    /$$$                                 │
│ | $$$$  /$$$$  /$$$$$$  /$$$$$$$  /$$   /$$   │
│ | $$ $$/$$ $$ /$$__  $$| $$__  $$| $$  | $$   │
│ | $$  $$$| $$| $$$$$$$$| $$  \ $$| $$  | $$   │
│ | $$\  $ | $$| $$_____/| $$  | $$| $$  | $$   │
│ | $$ \/  | $$|  $$$$$$$| $$  | $$|  $$$$$$/   │
│ |__/     |__/ \_______/|__/  |__/ \______/    │
└───────────────────────────────────────────────┘                    
""")
    print("\nP. Mon profil")
    print("A. Menu Admin\n")
    print("1. Tableau des masques\n───────────────────────────────")
    print("2. Ajouter une IP")
    print("3. Afficher les IP entrées")
    print("4. Supprimer une IP\n───────────────────────────────")
    print("5. Classe d'une IP")
    print("6. Détermination du réseau et du sous-réseau")
    print("7. Vérifier même réseau\n───────────────────────────────")
    print("8. Convertir en binaire une IP")
    print("\n0. Quitter")

    key = str(input("Entrer votre choix : ")).strip().lower()
    match key:
      case "1":
        cleanScreen()
        printTable()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "2":
        cleanScreen()
        inputIP()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "3":
        cleanScreen()
        showInputIP()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "4":
        cleanScreen()
        deleteIP()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "5":
        cleanScreen()
        classIP()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "6":
        cleanScreen()
        calculerReseauClassfull()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "7":
        cleanScreen()
        compareNetwork()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "8":
        cleanScreen()
        convertDecimalBinaire()
        input("\nAppuyer sur ENTER pour continuer...")
        cleanScreen()
      case "0":
        leave()
      case "a":
        if user[2] == "admin" or user[2] == "superadmin":
          menuAdmin(user,cnx)
        else:
          print("Accès refusé")
          time.sleep(_Waiting_Time)
          cleanScreen()
      case "p":
         user = modifierProfil(user,cnx)
      case _:
        print("Choix invalide")
        time.sleep(_Waiting_Time)
        cleanScreen()

def leave():
  print("───────── Fin de programme ─────────")
  sys.exit()

def menuAdmin(user,cnx):
  
  while(1):
    print("\n───────── ADMINISTRATION ─────────")
    print("1. Ajouter un utilisateur")
    print("2. Afficher les utilisateurs")
    print("3. Supprimer un utilisateur")
    print("4. Generer un code secret pour un user")
    print("5. Se déconnecter")
    key = str(input("Entrer votre choix : ")).strip()
    match key:
      case "1":
        print("\n───────── AJOUTER UN UTILISATEUR ─────────")
        register(cnx)
      case "2":
        print("\n───────── LISTE DES UTILISATEURS ─────────")
        printUsers(cnx)
      case "3":
        print("\n───────── SUPPRIMER UN UTILISATEUR ─────────")
        deletUser(cnx)
      case "4":
        donnerCodeSecret(cnx)
      case "5":
        home(user,cnx)
      case _:
        print("Choix invalide")
        time.sleep(_Waiting_Time)
        cleanScreen()
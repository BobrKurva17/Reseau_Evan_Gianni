import random
import string
import bcrypt as bc
import json

_security = 12

#Charger les utilisateurs depuis un fichier JSON
def loadUsers(cnx):
    cursorSelect = cnx.cursor()
    cursorSelect.execute("SELECT * FROM user")
    user = cursorSelect.fetchall()
    if len(user) == 0:
        return []
    return user


#Sauvegarder les utilisateurs dans un fichier JSON
def saveUsers(users,cnx):
    with open("features/users.json", "w") as f:
        json.dump(users, f, indent=4)

#Hasher mot de passe avec bcrypt
def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bc.gensalt(rounds=_security)
    hashed = bc.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

#Vérifier mot de passe
def verify_password(password_input, stored_hash):
    return bc.checkpw(
        password_input.encode('utf-8'),
        stored_hash.encode('utf-8')
    )

#Générer un code secret aléatoire de 8 caractères
def genererCodeSecret():
    caracteres = string.ascii_uppercase + string.digits
    code = "".join(random.choice(caracteres) for _ in range(8))
    return code

#Afficher les conseils pour un bon mot de passe
def conseilsMDP():
    print("╔══════════════════════════════════════════════╗")
    print("║     Conseils pour un bon mot de passe        ║")
    print("║  - Minimum 8 caractères                      ║")
    print("║  - Au moins 1 majuscule                      ║")
    print("║  - Au moins 1 chiffre                        ║")
    print("║  - Au moins 1 caractère spécial (!@#$%&*?)   ║")
    print("╚══════════════════════════════════════════════╝")

#Vérifier si le mot de passe respecte les conditions
def verifierMotDePasse(password):
    if len(password) < 8:
        print("Le mot de passe doit contenir au moins 8 caractères")
        return False
    if not any(c.isupper() for c in password):
        print("Le mot de passe doit contenir au moins une majuscule")
        return False
    if not any(c.isdigit() for c in password):
        print("Le mot de passe doit contenir au moins un chiffre")
        return False
    if not any(c in "!@#$%&*?" for c in password):
        print("Le mot de passe doit contenir au moins un caractère spécial (!@#$%&*?)")
        return False
    return True

#Premier lancement : créer le super admin si aucun utilisateur n'existe
def firstLaunch(cnx):
    users = loadUsers(cnx)
    if len(users) == 0:
        print("\n───────── PREMIER LANCEMENT ─────────")
        print("Aucun administrateur trouvé. Créez le super admin :")
        username = input("Nom d'utilisateur : ").strip()
        conseilsMDP()
        # On boucle jusqu'à ce que le mot de passe soit valide
        while True:
            password = input("Mot de passe : ").strip()
            if verifierMotDePasse(password):
                break
        # On génère et affiche le code secret une seule fois
        code = genererCodeSecret()
        print(f"╔══════════════════════════════════╗")
        print(f"║  Code secret : {code}            ║")
        print(f"║  Notez-le bien, il ne sera       ║")
        print(f"║  affiché qu'une seule fois !     ║")
        print(f"╚══════════════════════════════════╝")
        superAdmin = {
            "username": username,
            "pswd": hash_password(password),
            "roles": "superadmin",
            "codeSecret": hash_password(code)
        }
        cursortInsert = cnx.cursor()
        cursortInsert.execute("INSERT INTO user (username, pswd, roles, codeSecret) VALUES (%s, %s, %s, %s)", 
                              (superAdmin["username"], superAdmin["pswd"], superAdmin["roles"], superAdmin["codeSecret"]))  
        cnx.commit()
        print(f"Super admin '{username}' créé avec succès !")
        print("Votre mot de passe à correctement été HASH et stocker")

#Inscription d'un nouvel utilisateur (admin ou superadmin seulement)
def register(admin_user,cnx):
    if admin_user["role"] != "admin" and admin_user["role"] != "superadmin":
        print("Accès refusé")
        return
    users = loadUsers(cnx)
    username = input("Nom d'utilisateur : ").strip()
    # On vérifie si le username existe déjà
    for u in users:
        if u["username"] == username:
            print("Nom d'utilisateur déjà existant")
            return
    conseilsMDP()
    # On boucle jusqu'à ce que le mot de passe soit valide
    while True:
        password = input("Mot de passe : ").strip()
        if verifierMotDePasse(password):
            break
    role = input("Rôle (admin/user) : ").strip()
    # On génère et affiche le code secret une seule fois
    code = genererCodeSecret()
    print(f"╔══════════════════════════════════╗")
    print(f"║  Code secret : {code}            ║")
    print(f"║  Notez-le bien, il ne sera       ║")
    print(f"║  affiché qu'une seule fois !     ║")
    print(f"╚══════════════════════════════════╝")
    new_user = {
        "username": username,
        "password": hash_password(password),
        "role": role,
        "code_secret": hash_password(code)
    }
    users.append(new_user)
    saveUsers(users,cnx)
    print("Utilisateur ajouté avec succès")
    print("Votre mot de passe à correctement été HASH et stocker")

#Connexion au programme
def login(cnx):
    print("\n───────── CONNEXION ─────────")
    users = loadUsers(cnx)
    tentatives = 0
    
    while True:
        username = input("Nom d'utilisateur : ").strip()
        # On vérifie si le username existe avant de demander le mot de passe
        userTrouve = None
        for user in users:
            if user["username"] == username:
                userTrouve = user
                break
        
        if userTrouve is None:
            print("Utilisateur introuvable")
            continue
        
        # Username trouvé, on demande le mot de passe jusqu'à 3 fois
        while tentatives < 3:
            password = input("Mot de passe : ").strip()
            if verify_password(password, userTrouve["password"]):
                print("Connexion réussie !")
                return userTrouve
            else:
                print("Mot de passe incorrect")
                tentatives += 1
                print(f"╔══════════════════════════════════╗")
                print(f"║  Tentative {tentatives}/3                   ║")
                print(f"╚══════════════════════════════════╝")
        break
    
    # Après 3 tentatives échouées
    print("╔══════════════════════════════════════╗")
    print("║      TENTATIVES ÉPUISÉES !           ║")
    print("╚══════════════════════════════════════╝")
    print("1. Réessayer")
    print("2. Réinitialiser mon mot de passe")
    print("0. Quitter")
    key = input("Votre choix : ").strip()
    match key:
        case "1":
            return login(cnx)
        case "2":
            reinitialiserMDP(username)
            return login(cnx)
        case _:
            exit()

#Réinitialiser le mot de passe avec le code secret
def reinitialiserMDP(username,cnx):
    users = loadUsers(cnx)
    code = input("Code secret : ").strip()
    for user in users:
        if user["username"] == username:
            if verify_password(code, user["code_secret"]):
                conseilsMDP()
                while True:
                    newPassword = input("Nouveau mot de passe : ").strip()
                    if verifierMotDePasse(newPassword):
                        break
                user["password"] = hash_password(newPassword)
                saveUsers(users,cnx)
                print("Mot de passe réinitialisé avec succès !")
                return
            else:
                print("Code secret incorrect !")
                return
    print("Utilisateur introuvable !")

#Afficher la liste des utilisateurs
def printUsers(cnx):
    users = loadUsers(cnx)
    for user in users:
        print(f"Utilisateur: {user['username']}, Rôle: {user['role']}")

#Supprimer un utilisateur (impossible de supprimer le superadmin)
def deletUser(admin_user,cnx):
    users = loadUsers(cnx)
    username = input("Nom d'utilisateur à supprimer : ").strip()
    for user in users:
        if user["username"] == username:
            if user["role"] == "superadmin":
                print("Impossible de supprimer le super admin !")
                return
            users.remove(user)
            saveUsers(users)
            print("Utilisateur supprimé avec succès")
            return
    print("Utilisateur introuvable")

#Modifier le profil de l'utilisateur connecté
def modifierProfil(user,cnx):
    users = loadUsers(cnx)
    print("\n───────── MODIFIER MON PROFIL ─────────")
    print("1. Changer mon nom d'utilisateur")
    print("2. Changer mon mot de passe")
    print("3. Changer mon code secret")
    print("4. Retour")
    
    key = input("Votre choix : ").strip()
    match key:
        case "1":
            newUsername = input("Nouveau nom d'utilisateur : ").strip()
            # On vérifie si le nouveau username existe déjà
            for u in users:
                if u["username"] == newUsername:
                    print("Nom d'utilisateur déjà existant")
                    return user
            # On met à jour le username
            for u in users:
                if u["username"] == user["username"]:
                    u["username"] = newUsername
                    saveUsers(users)
                    print("Nom d'utilisateur modifié avec succès !")
                    user["username"] = newUsername
                    return user
        case "2":
            conseilsMDP()
            # On boucle jusqu'à ce que le mot de passe soit valide
            while True:
                newPassword = input("Nouveau mot de passe : ").strip()
                if verifierMotDePasse(newPassword):
                    break
            # On met à jour le mot de passe hashé
            for u in users:
                if u["username"] == user["username"]:
                    u["password"] = hash_password(newPassword)
                    saveUsers(users,cnx)
                    print("Mot de passe modifié avec succès !")
                    return user
        case "3":
            # On génère un nouveau code secret et on l'affiche une seule fois
            newCode = genererCodeSecret()
            print(f"╔══════════════════════════════════╗")
            print(f"║  Nouveau code secret : {newCode} ║")
            print(f"║  Notez-le bien !                 ║")
            print(f"╚══════════════════════════════════╝")
            # On sauvegarde le code hashé
            for u in users:
                if u["username"] == user["username"]:
                    u["code_secret"] = hash_password(newCode)
                    saveUsers(users,cnx)
            print("Code secret modifié avec succès !")
            return user
        case "4":
            return user
        case _:
            print("Choix invalide")
            return user
        
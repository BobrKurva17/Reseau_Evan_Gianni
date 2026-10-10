import random
import string
import bcrypt as bc
import json

_security = 12
    


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

def donnerCodeSecret(cnx):
    cursor = cnx.cursor()
    
    printUsers(cnx)
    indice = input("Insérez l'indice : ").strip()

    cursor.execute("SELECT * FROM user WHERE id = %s", (indice,))
    user = cursor.fetchone()

    while user is None:
        if user is None:
            print("Utilisateur introuvable")
        indice = input("Insérez l'indice : ").strip()
        cursor.execute("SELECT * FROM user WHERE id = %s", (indice,))
        user = cursor.fetchone()

    newcode = genererCodeSecret()
    hashedCode = hash_password(newcode)
    cursor.execute("UPDATE user SET codeSecret = %s WHERE id = %s", (hashedCode, indice))
    cnx.commit()
    print(f"╔══════════════════════════════════╗")
    print(f"║  Code secret : {newcode}         ║")
    print(f"║  Notez-le bien, il ne sera       ║")
    print(f"║  affiché qu'une seule fois !     ║")
    print(f"╚══════════════════════════════════╝")


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

    #Vérifier si la base de données est vide
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    (count,) = cursor.fetchone()
    cursor.close()

    if count == 0:
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
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO user (username, pswd, roles, codeSecret) VALUES (%s, %s, %s, %s)", 
                              (superAdmin["username"], superAdmin["pswd"], superAdmin["roles"], superAdmin["codeSecret"]))  
        cnx.commit()
        print(f"Super admin '{username}' créé avec succès !")
        print("Votre mot de passe à correctement été HASH et stocker")

#Inscription d'un nouvel utilisateur (admin ou superadmin seulement)
def register(cnx):
    cursor = cnx.cursor()

    username = input("Nom d'utilisateur : ").strip()
    # On vérifie si le username existe déjà
    cursor.execute("SELECT username FROM user where username = %s", (username,))
    userAlreadyExists = cursor.fetchone()

    while userAlreadyExists is not None:
        print("Nom d'utilisateur déjà existant")
        username = input("Nom d'utilisateur : ").strip()
        cursor.execute("SELECT username FROM user where username = %s", (username,))
        userAlreadyExists = cursor.fetchone()

    conseilsMDP()
    # On boucle jusqu'à ce que le mot de passe soit valide
    while True:
        password = input("Mot de passe : ").strip()
        if verifierMotDePasse(password):
            break
    role = input("Rôle (admin/user) : ").strip()

    new_user = {
        "username": username,
        "pswd": hash_password(password),
        "roles": role
    }
    
    cursor.execute("INSERT INTO user (username, pswd, roles) VALUES (%s, %s, %s)", 
                            (new_user["username"], new_user["pswd"], new_user["roles"]))  
    cnx.commit()

    print("Utilisateur ajouté avec succès")
    print("Votre mot de passe à correctement été HASH et stocker")

#Connexion au programme
def login(cnx):
    print("\n───────── CONNEXION ─────────")
    cursor = cnx.cursor()
    tentatives = 0
    
    while True:
        username = input("Nom d'utilisateur : ").strip()
        # On vérifie si le username existe avant de demander le mot de passe
        cursor.execute("SELECT * FROM user where username = %s", (username,))
        userExists = cursor.fetchone()

        if userExists is None:
            print("Utilisateur introuvable")
            continue
        
        # Username trouvé, on demande le mot de passe jusqu'à 3 fois
        while tentatives < 3:
            password = input("Mot de passe : ").strip()
            if verify_password(password, userExists[3]):
                print("Connexion réussie !")
                return userExists
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
            reinitialiserMDP(username,cnx)
            return login(cnx)
        case _:
            exit()

#Réinitialiser le mot de passe avec le code secret
def reinitialiserMDP(username,cnx):

    cursor = cnx.cursor()
    cursor.execute("SELECT codeSecret FROM user WHERE username = %s", (username,))
    result = cursor.fetchone() #fetchone() récupère le contenu de la ligne dès qu'elle est trouvée

    if result is None or result[0] is None:
        print("Vous n'avez pas de code secret enregistré. Veuillez contacter un administrateur pour réinitialiser votre mot de passe.")
        return
    
    code = input("Code secret : ").strip()
    if(verify_password(code, result[0])):
        conseilsMDP()
        while True:
            newPassword = input("Nouveau mot de passe : ").strip()
            if verifierMotDePasse(newPassword):
                break
        hashedPassword = hash_password(newPassword)
        cursor.execute("UPDATE user SET pswd = %s WHERE username = %s", (hashedPassword, username))
        cnx.commit()
        print("Mot de passe réinitialisé avec succès !")

#Afficher la liste des utilisateurs
def printUsers(cnx):
    cursorSelect = cnx.cursor()
    cursorSelect.execute("SELECT * FROM user")
    users = cursorSelect.fetchall()

    for user in users:
        print(f"{user[0]} Nom d'utilisateur : {user[1]}, Rôle : {user[2]}")
    

#Supprimer un utilisateur (impossible de supprimer le superadmin)
def deletUser(cnx):
    cursor = cnx.cursor()

    printUsers(cnx)
    indice = input("Insérez l'indice : ").strip()

    cursor.execute("SELECT * FROM user WHERE id = %s", (indice,))
    user = cursor.fetchone()

    while user is None or user[2] == "superadmin":
        if user is not None and user[2] == "superadmin":
            print("Impossible de supprimer le super admin !")
        if user is None:
            print("Utilisateur introuvable")

        indice = input("Insérez l'indice : ").strip()
        cursor.execute("SELECT * FROM user WHERE id = %s", (indice,))
        user = cursor.fetchone()

    print(f"Vous êtes sur le point de supprimer l'utilisateur : {user[1]} (Rôle : {user[2]})")
    confirmation = input("Êtes-vous sûr ? (O/N) : ").strip().lower()
    if confirmation != "o":
        print("Suppression annulée")
        return
    
    cursor.execute("DELETE FROM user WHERE id = %s", (indice,))
    cnx.commit()
    

#Modifier le profil de l'utilisateur connecté
def modifierProfil(user,cnx):
    cursor = cnx.cursor()
    print("\n───────── MODIFIER MON PROFIL ─────────")
    print("1. Changer mon nom d'utilisateur")
    print("2. Changer mon mot de passe")
    print("3. Retour")
    
    key = input("Votre choix : ").strip()
    match key:
        case "1":
            newUsername = input("Nouveau nom d'utilisateur : ").strip()
            # On vérifie si le nouveau username existe déjà
            cursor.execute("SELECT username FROM user where username = %s", (newUsername,))
            userAlreadyExists = cursor.fetchone()
        
            while userAlreadyExists is not None:
                print("Nom d'utilisateur déjà existant")
                newUsername = input("Nom d'utilisateur : ").strip()
                cursor.execute("SELECT username FROM user where username = %s", (newUsername,))
                userAlreadyExists = cursor.fetchone()

            # On met à jour le username
            cursor.execute("UPDATE user SET username = %s WHERE username = %s", (newUsername, user[1]))
            cnx.commit()
            print("Nom d'utilisateur modifié avec succès !")

        case "2":
            conseilsMDP()
            # On boucle jusqu'à ce que le mot de passe soit valide
            while True:
                newPassword = input("Nouveau mot de passe : ").strip()
                if verifierMotDePasse(newPassword):
                    break
            newPasswordHashed = hash_password(newPassword)
            # On met à jour le mot de passe hashé
            cursor.execute("UPDATE user SET pswd = %s WHERE username = %s", (newPasswordHashed, user[1]))
            cnx.commit()
            print("Nom d'utilisateur modifié avec succès !")
        case "3":
            return 
        case _:
            print("Choix invalide")
            return 
        
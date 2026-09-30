import os

userInputIP = {}
historicIP = []
index = 0


# ==========================================================================
# User method
# ==========================================================================

def printTable():
    print("\nCIDR | BINAIRE                              | DECIMAL")
    print("-" * 65)

    for cidr in range(8, 31):
        bits = "1" * cidr + "0" * (32 - cidr)
        binaire = ".".join([bits[i:i+8] for i in range(0, 32, 8)])

        octets = [bits[i:i+8] for i in range(0, 32, 8)]
        decimal = ".".join(str(int(octet, 2)) for octet in octets)

        print(f"/{cidr:<2}  | {binaire:<36} | {decimal}")


def selectOrInputIP():

    print("\n────────────────── Sélection de l'adresse IP ──────────────────")
    print("M. Saisie manuel d'adresse IP")
    
    # On affiche l'historique s'il existe
    if historicIP:
        showInputIP()
    else:
        print("(L'historique est vide)")

    try:
        choix = str(input("\nVotre choix (ID ou 'M' pour nouveau) : ")).strip().lower()
    except ValueError:
        print("Entrée invalide.")
        return None

    # Cas 1 : Nouvelle saisie manuelle
    if choix == "m":
        return validIP()
    
    if choix.isdigit():
        intChoix = int(choix)

        # Cas 2 : Sélection dans l'historique
        for entree in historicIP:
            if entree["id"] == intChoix:
                return entree["ip"],entree["cidr"]
        print(f"Aucun élément trouvé avec l'ID {intChoix}")
    else:
        print("Entrée invalide.")

    return None,None


def inputIP():
    global index
    
    ip_recuperee,cidr_recuperee = validIP()
    
    # On ne stocke que si une IP a vraiment été récupérée
    if ip_recuperee is not None:
        userInputIP[index] = ip_recuperee
        historicIP.append({"id": index, "ip": ip_recuperee, "cidr": cidr_recuperee})
        index += 1
        print("IP enregistrée avec succès.")
    else:
        print("Opération annulée.")

def showInputIP():
    print("\n────────────────── Historique des saisies ──────────────────")
    for entree in historicIP:
        # Reconstruction IP
        ip_string = ".".join(entree["ip"])

        # Ajout CIDR si présent
        if entree["cidr"] is not None:
            ip_string += f"/{entree['cidr']}"

        print(f"{entree['id']:4}. | {ip_string}")


def deleteIP():
    global index
    
    # On vérifie si l'historique est vide
    if not historicIP:
        print("L'historique est vide, rien à supprimer.")
        return
    
    showInputIP()

    # Demander quel ID supprimer
    try:
        id_a_supprimer = int(input("Entrez le numéro de l'IP à supprimer : "))
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Vérifier si l'ID existe
    found = False
    for i, entree in enumerate(historicIP):
        if entree["id"] == id_a_supprimer:
            historicIP.pop(i)
            found = True
            break
    
    if not found:
        print(f"Aucun élément trouvé avec l'ID {id_a_supprimer}")
        return

    userInputIP.clear() # dictionnaire supprimer
    
    for i, entree in enumerate(historicIP):
        entree["id"] = i           
        userInputIP[i] = {
            "ip": entree["ip"],
            "cidr": entree["cidr"]
        } # dictionnaire avec le nouvel index
    
    index = len(historicIP)
    
    print(f"L'ID {id_a_supprimer} a été supprimé.")


def validIP():

    while True:

        userIP = input("Entrer votre adresse ip : ").strip()
        segments = userIP.split(".")
        cidr = None

        if len(segments) == 4:

            if "/" in segments[3]:

                lastSegment, cidrPart = segments[3].split("/")
                segments[3] = lastSegment

                # Vérification CIDR
                if cidrPart.isdigit() and 8 <= int(cidrPart) <= 30:
                    cidr = int(cidrPart)
                else:
                    print("CIDR invalide.")
                    continue

            if all(
                s.isdigit() and 0 <= int(s) <= 255
                for s in segments
            ):
                return segments, cidr

        print("IP incorrecte.")

        restart = input("Voulez-vous recommencer ? (O/N) : ").strip().lower()

        if restart == "n":
            return None,None


def convertDecimalBinaire():
  # On crée une liste pour stocker chaque segment converti
    liste_binaires = []
    liste_decimal = []
    IP_decimal,CIDR_decimal = selectOrInputIP()

    for s in IP_decimal:
        binaire = f"{int(s):08b}"
        decimal = f"{int(s)}"
        liste_binaires.append(binaire)
        liste_decimal.append(decimal)
    ipBinaire = ".".join(liste_binaires)
    ipDecimal = ".".join(liste_decimal)

    if CIDR_decimal is not None:
        print(f"{ipDecimal} = {ipBinaire} | ( CIDR : {CIDR_decimal:02} )")
    else:
        print(f"{ipDecimal} = {ipBinaire}")


def classIP():
    ip,cidr = selectOrInputIP()

    if ip is None:
        print("Opération annulée.")
        return

    ipDecimalP1 = int(ip[0])
    ipDecimalP2 = int(ip[1])

    estPrivee = False
    estReserver = False

    if cidr is None:
        match ipDecimalP1:
            case _ if 0 <= ipDecimalP1 < 128:
                print("Classe A")
                cidr = 8
                
                if ipDecimalP1 == 10:
                    estPrivee = True

                if ipDecimalP1 == 127:
                    estReserver = True

            case _ if 128 <= ipDecimalP1 < 192:
                print("Classe B")
                cidr = 8 * 2
                
                if ipDecimalP1 == 172 and (16 <= ipDecimalP2 < 32):
                    estPrivee = True

            case _ if 192 <= ipDecimalP1 < 224:
                print("Classe C")
                cidr = 8 * 3
                
                if ipDecimalP1 == 192 and ipDecimalP2 == 168:
                    estPrivee = True
            
            case _ if 224 <= ipDecimalP1 < 240:
                print("Classe D")
                cidr = 0
                estReserver = True
            
            case _ if 240 <= ipDecimalP1 < 256:
                print("Classe E")
                cidr = 0
                estReserver = True
    else:
        print("Aucune classe")

    bits = "1" * cidr + "0" * (32 - cidr)

    masqueBinaire = ".".join( bits[i:i+8] for i in range(0, 32, 8) )
    masqueDecimal = ".".join( str(int(octet, 2)) for octet in masqueBinaire.split(".") )

    strEstPrivee = "Oui" if estPrivee == True else "Non"
    strEstReserver = "Oui" if estReserver == True else "Non"

    print(f"\nLe masque de votre IP est le suivant : {masqueDecimal}")
    print(f"Privée : {strEstPrivee}\nRéserver : {strEstReserver}")

    # return masqueBinaire


def calculerReseauClassfull():
    ip, cidr = selectOrInputIP()

    if ip is None:
        print("Opération annulée.")
        return

    if cidr is None:
        print("Cette fonctionnalité nécessite un masque CIDR (ex: /26) pour découper en sous-réseau.")
        return

    ipDecimalP1 = int(ip[0])

    cidr_classe = 8 if ipDecimalP1 < 128 else (16 if ipDecimalP1 < 192 else (24 if ipDecimalP1 < 224 else 0))
    
    if cidr_classe == 0:
        print("Les adresses de classes D et E n'ont pas de réseau Classful standard.")
        return

    ip_bits = "".join(f"{int(s):08b}" for s in ip)

    bits_masque_classe = "1" * cidr_classe + "0" * (32 - cidr_classe)
    net_bits_classe = "".join("1" if ip_bits[j] == "1" and bits_masque_classe[j] == "1" else "0" for j in range(32))
    
    octets_binaires_classe = [net_bits_classe[j:j+8] for j in range(0, 32, 8)]
    reseau_classe = ".".join(str(int(octet, 2)) for octet in octets_binaires_classe)
    print(f"Adresse Réseau (Classful) : {reseau_classe}")

    if cidr != cidr_classe:
        bits_masque_custom = "1" * cidr + "0" * (32 - cidr)
        net_bits_custom = "".join("1" if ip_bits[j] == "1" and bits_masque_custom[j] == "1" else "0" for j in range(32))
        
        octets_binaires_custom = [net_bits_custom[j:j+8] for j in range(0, 32, 8)]
        sous_reseau = ".".join(str(int(octet, 2)) for octet in octets_binaires_custom)
        print(f"Adresse de Sous-Réseau    : {sous_reseau}")
    else:
        print("L'adresse de sous-réseau est identique à l'adresse réseau.")


def compareNetwork():
    print("\n────────────────── COMPARAISON DE RÉSEAUX ──────────────────")
    machines = [
        {"ip": None, "cidr": None},
        {"ip": None, "cidr": None}
    ]
    
    i = 0
    
    while i < 2:
        print(f"\n─── Machine {i + 1} ───")
        
        ip, cidr = selectOrInputIP()
        
        if ip is None:
            print("Opération annulée.")
            return

        while cidr is None:
            print("Attention : Un masque (CIDR) est obligatoire pour comparer les réseaux.")
            print(f"Veuillez ressaisir l'IP de la Machine {i + 1} avec son CIDR (ex: 192.168.1.1/24) :")
            ip, cidr = validIP()
            
            if ip is None:
                print("Opération annulée.")
                return

        machines[i]["ip"] = ip
        machines[i]["cidr"] = cidr
        i += 1

    reseaux_calculés = []

    #Nouveau Calcul du réseau 
    reseauMachineBinaire=[]        #tableau contenant le réseau des 2 machines  (binaire)
    masqueMachineBinaire=[]        #tableau contenant le masque des 2 machines  (binaire)
    machineBinaire=[]              #tableau contenant l'ip des 2 machines       (binaire)
    
    for mach in machines:

        ip_bits = "".join(f"{int(s):08b}" for s in mach["ip"])
        machineBinaire.append(ip_bits)

        bits_masque = "1" * mach["cidr"] + "0" * (32 - mach["cidr"])
        masqueMachineBinaire.append(bits_masque)

        net_bits = "".join("1" if ip_bits[j] == "1" and bits_masque[j] == "1" else "0" for j in range(32))
        reseauMachineBinaire.append(net_bits)

        octets_binaires = [net_bits[j:j+8] for j in range(0, 32, 8)]
        
        reseau_decimal = ".".join(str(int(octet, 2)) for octet in octets_binaires)
        
        reseaux_calculés.append(reseau_decimal)
        
    for mach in machines:
     
        ##Nouveau calcul 
        vu_par_M1 = "".join(
        "1" if machineBinaire[1][j] == "1" and masqueMachineBinaire[0][j] == "1" else "0"
        for j in range(32)
        )

        # M2 regarde M1 avec son propre masque
        vu_par_M2 = "".join(
            "1" if machineBinaire[0][j] == "1" and masqueMachineBinaire[1][j] == "1" else "0"
            for j in range(32)
        )


    m1_consideration = vu_par_M1 == reseauMachineBinaire[0]
    m2_consideration = vu_par_M2 == reseauMachineBinaire[1]     
    #comparaison ip machine 2 avec masque machine 1 
   
    #comparaison ip machine 1 avec masque machine 2 
  

    print("\n───────── RÉSULTAT DU CALCUL RÉSEAU ─────────")
    print(f"Réseau Machine 1 : {reseaux_calculés[0]}/{machines[0]['cidr']}")
    print(f"Réseau Machine 2 : {reseaux_calculés[1]}/{machines[1]['cidr']}")
    
    print("\n───────── RÉSULTAT BILATÉRAL ─────────")
    if m1_consideration and m2_consideration:
        print(f"les deux machines se considèrent dans le même réseau")
    elif m1_consideration and not m2_consideration: 
        print(f"la machine 1 se considère dans le même réseau que la machine 2  mais pas inversément")  
    elif not m1_consideration and m2_consideration : 
        print(f"la machine 2 se considère dans le même réseau que la machine 1 mais pas inversément")
    else : 
        print(f"les deux machines sont sur des réseau différents !")

              


def cleanScreen():
    # 'nt' = Windows, 'posix' = Linux/macOS
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
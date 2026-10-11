import os
import pandas as pd

userInputIP = {}
historicIP = []
index = 0


# ==========================================================================
# User method
# ==========================================================================

#Modifié
def printTable():
    matSR = []

    #print("\nCIDR | BINAIRE                              | DECIMAL")
    #print("-" * 65)

    for cidr in range(8, 31): 
        cidrAffiche = "/"+str(cidr)
        bits = "1" * cidr + "0" * (32 - cidr)
        binaire = ".".join([bits[i:i+8] for i in range(0, 32, 8)])

        octets = [bits[i:i+8] for i in range(0, 32, 8)]
        decimal = ".".join(str(int(octet, 2)) for octet in octets)
        ligne = [cidrAffiche,binaire,decimal]
        matSR.append(ligne)
    #Nouveau - plus besoin de l'affichage 
    #for l in matSR:
    #    print(f"{l[0]} | {l[1]} | {l[2]}")
       

    
    return matSR
#Nouveau Fonction ajouté
def exporterTableau(fenetre):

    tableauSR = printTable()
    chemin = fenetre.entree_chemin.text()

    if chemin == "":
        fenetre.message_erreur.setText("Veuillez saisir un chemin.")
        return

    if not os.path.isdir(chemin):
        fenetre.message_erreur.setText("Le dossier indiqué n'existe pas.")
        return

    #chemin = str(input("Insérez le chemin absolue de votre dossier : "))
    #while chemin == "":
    #    print("Chemin vide")
    #    chemin = str(input("Insérez le chemin absolue de votre dossier : "))

    if not chemin.endswith("\\"):
        chemin += "\\"

    #Transformation du tableau créer en data
    df = pd.DataFrame(tableauSR, columns=["CIDR","Masque en Binaire","Masque en décimal"])#Ajoute un titre en plus pour les colonnes
    with pd.ExcelWriter(chemin+'TableauMasques.xlsx', engine="xlsxwriter") as fichier:
        df.to_excel(fichier, sheet_name="Matrice des sous réseaux", index=False)#Exporter en fichier excel

    feuille = fichier.sheets["Matrice des sous réseaux"]
    feuille.set_column("A:C", 24)

    print("Le fichier a été généré avec succès !")


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
        return ip_string 


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


def validIP(fenetre,ip):


    segments = ip.split(".")

    if len(segments) == 4:
        if all(s.isdigit() and 0 <= int(s) <= 255 for s in segments):
            fenetre.message_valide.setText(f"Le format de l'entrée {ip} est valide !")
            return segments
        else: 
            #permet de distinguer si on parle de l'adresse ip ou le masque puisque les deux utilisent cette fonction
            fenetre.message_erreur.setText(f"L'entrée {ip} contient une erreur ! Veuillez respecter le format.")
    else:
        fenetre.message_erreur.setText(f"L'entrée {ip} doit contenir 4 segments.")

def MasqueValide(fenetre,masque):
    MasqueVerif = masque.split('.')

    if MasqueVerif == ['255', '255', '255', '255']:
        fenetre.message_erreur.setText(f"le masque {masque} est invalide, les 4 octets ne peuvent pas être à 255")
        return
             
    if MasqueVerif == ['0', '0', '0', '0']:
        fenetre.message_erreur.setText(f"Le masque {masque} est invalide. Un masque ne peut pas être composé de 4 octets à 0.")
        return
        
    for i in range(len(MasqueVerif)):
        if MasqueVerif[i] not in ['0', '128', '192', '224', '240', '248', '252', '254', '255']:
            fenetre.message_erreur.setText(f"Le masque {masque} est invalide. Les nombres acceptés sont : 0, 128, 192, 224, 240, 248, 252, 254, 255")
            return            
             
        if i < 3 and int(MasqueVerif[i]) < int(MasqueVerif[i+1]):
            fenetre.message_erreur.setText(f"Le masque  {masque} est invalide. Il doit être une suite de 1 et de 0 sans interruption.")
            return

    
    fenetre.message_valide.setText(f"Le masque {masque} est valide !")

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


def classIP(fenetre,ip):
    if ip is None:
        return
    ip_a_tester= ip.split(".")

    ipDecimalP1 = int(ip_a_tester[0])
    ipDecimalP2 = int(ip_a_tester[1])
    #test 
    #print(ipDecimalP1,ipDecimalP2)

    estPrivee = False
    estReserver = False
    #variable permettant de générer le masque de classe 
    cidr =0
    match ipDecimalP1:
            case _ if 0 <= ipDecimalP1 < 128:
                #print("Classe A")
                fenetre.label_classe.setText("La classe de l'IP est : A")
                cidr = 8
                
                if ipDecimalP1 == 10:
                    estPrivee = True

                if ipDecimalP1 == 127:
                    estReserver = True

            case _ if 128 <= ipDecimalP1 < 192:
                #print("Classe B")
                fenetre.label_classe.setText("La classe de l'IP est : B")
                cidr = 8 * 2
                
                if ipDecimalP1 == 172 and (16 <= ipDecimalP2 < 32):
                    estPrivee = True

            case _ if 192 <= ipDecimalP1 < 224:
                fenetre.label_classe.setText("La classe de l'IP est : C")
                cidr = 8 * 3
                
                if ipDecimalP1 == 192 and ipDecimalP2 == 168:
                    estPrivee = True
            
            case _ if 224 <= ipDecimalP1 < 240:
                #print("Classe D")
                fenetre.label_classe.setText("La classe de l'IP est : D")
                cidr = 0
                estReserver = True
            
            case _ if 240 <= ipDecimalP1 < 256:
                #print("Classe E")
                fenetre.label_classe.setText("La classe de l'IP est : E")
                cidr = 0
                estReserver = True
    if(estReserver):
        fenetre.label_adresse_specifique.setText("l'adresse de L'Ip est : réservée")
    if(estPrivee):
         fenetre.label_adresse_specifique.setText("l'adresse de L'Ip est : privée")

    if ipDecimalP1 == 127:
        fenetre.label_adresse_specifique.setText("l'adresse de L'Ip est : une adresse IP de loopback")
    elif ipDecimalP1 == 169 and ipDecimalP2 == 254:
        fenetre.label_adresse_specifique.setText("l'adresse de L'Ip est : une adresse IP de lien local")
    else:
        fenetre.label_adresse_specifique.setText("l'adresse de L'Ip est : une adresse IP publique")
        
    
    bits = "1" * cidr + "0" * (32 - cidr)

    masqueBinaire = ".".join( bits[i:i+8] for i in range(0, 32, 8) )
    masqueDecimal = ".".join( str(int(octet, 2)) for octet in masqueBinaire.split(".") )

    fenetre.label_masque_classe.setText(f"Le masque de classe est :{masqueDecimal}")
    # return masqueBinaire


def calculerReseauClassfull(fenetre,ip,masque):
  
    ipDecimalP1 = int(ip.split(".")[0])

    ip_bits = "".join(f"{int(s):08b}" for s in ip.split("."))
   
    masqueBinaire = []

    for octet in DecimalVersBinaire(masque):
        for bit in octet:
            masqueBinaire.append(str(bit))

    masqueBinaire = "".join(masqueBinaire)

     # Détermination du CIDR de classe
    match ipDecimalP1:
        case _ if 0 <= ipDecimalP1 < 128: cidr = 8
        case _ if 128 <= ipDecimalP1 < 192: cidr = 16
        case _ if 192 <= ipDecimalP1 < 224: cidr = 24
        case _: cidr = 0

    masque_classe = "1" * cidr + "0" * (32 - cidr)

    # Réseau par défaut basé sur la classe
    net_bits_classe = "".join("1" if ip_bits[j] == "1" and masque_classe[j] == "1" else "0" for j in range(32))

    octets_binaires_classe = [net_bits_classe[j:j+8] for j in range(0, 32, 8)]

    reseau_classe = ".".join(str(int(octet, 2)) for octet in octets_binaires_classe)
    
    fenetre.label_reseau.setText(f"le réseau est :{reseau_classe}")
    fenetre.label_sous_reseau.setText("le sous-réseau : pas de sous-réseau")

   
        

    cidr_saisi = masqueBinaire.count("1")
    
    if cidr != cidr_saisi:
        bits_masque_custom = "1" * cidr_saisi + "0" * (32 - cidr_saisi)
        net_bits_custom = "".join("1" if ip_bits[j] == "1" and bits_masque_custom[j] == "1" else "0" for j in range(32))
        
        octets_binaires_custom = [net_bits_custom[j:j+8] for j in range(0, 32, 8)]
        sous_reseau = ".".join(str(int(octet, 2)) for octet in octets_binaires_custom)
        
        fenetre.label_sous_reseau.setText(f"le sous-réseau : {sous_reseau}")
    else:
        fenetre.label_sous_reseau.setText("le sous-réseau : identique au réseau")

    print("Masque binaire :", masqueBinaire)
    print("CIDR saisi :", cidr_saisi)
    print("CIDR classe :", cidr)
    print("Réseau calculé :", reseau_classe)


def DecimalVersBinaire(var):
    liste=[]
    # on sépare l'adresse ip en 4 parties correspondantes aux 4 octets
    liste = var.split(".")
    #cette variable contiendra les 4 octets binaires de notre IP 
    Masque=[]
    for i in range(4):
        octetEnBinaire=TraducteurBinaire(liste[i])
        Masque.append(octetEnBinaire)
    
    return Masque
    
def TraducteurBinaire(valeur):
    # la valeur est reçue en String donc conversion en entier 
    valeur_int=int(valeur)
     # On prépare un tableau de 8 zéros (notre octet)
    binaire = [0, 0, 0, 0, 0, 0, 0, 0]    
    # On commence à remplir par la DROITE (indice 7)
    i = 7
    while valeur_int > 0 and i >= 0:
        binaire[i] = valeur_int % 2  # On place le reste (0 ou 1)
        valeur_int = valeur_int // 2      # On divise pour passer au bit suivant
        i = i - 1                 # On recule d'une case vers la gauche
    return binaire

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
        ##appliquer le masque de machine 1 à la machine 2 
        vu_par_M1 = "".join(
        "1" if machineBinaire[1][j] == "1" and masqueMachineBinaire[0][j] == "1" else "0"
        for j in range(32)
        )

        # M2 regarde M1 avec son propre masque
        # appliquer le masque de la machine 2 à la machine 1 
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

#Nouveau découpe réseau sur base du nombre de sous-réseaux demandés 
def decoupe_reseau_par_nombre_sr(reseau,masque,nbr_sr):
    #fonction valide mais VALIDATION DU RESEAU A IMPLEMENTER 
    #vérifier la validité du reseau 
    reseau=validIPV2(reseau)
    # vérifier la validité du masque en classless 
    if(masque<8 or masque>30):
        print(" masque en classless invalide")
        return
    #vérifier la validité du nombre de sr 
    if(nbr_sr<=0):
        print("le nombre de sous-réseau est invalide !")
        return 
    #nombre de bits réservé pour les machines 
    nbr_bits_hote_min=2
    # exemple avec /24 alors il me reste 8 bits pour les hôtes 
    nbr_bits_machines= 32-masque 
    nbr_bits_empruntes = 0
    while True:
        if nbr_bits_hote_min > nbr_bits_machines-nbr_bits_empruntes:
            print("il n'y a pas assez de bits hôtes disponible pour ce nombre de SR. ")
            return 
        if(nbr_sr <= (2**nbr_bits_empruntes)):
            print("il y a donc ",nbr_bits_empruntes," empruntés aux bits hôtes")
            break
        
        nbr_bits_empruntes= nbr_bits_empruntes + 1
        ##nbr de bits empruntés jusqu'à 
    nouveau_masque = masque + nbr_bits_empruntes

    if nouveau_masque <= 16:
        octet_travaille = 1
        octet_report = 0
        nbr_bits_dans_octet = nouveau_masque - 8
    elif nouveau_masque <= 24:
        octet_travaille = 2
        octet_report = 1
        nbr_bits_dans_octet = nouveau_masque - 16
    else:
        octet_travaille = 3
        octet_report = 2
        nbr_bits_dans_octet = nouveau_masque - 24

    # conversion du réseau en entier ['192','168','1','0'] en [192,168,1,0]
    for i in range(len(reseau)):
        reseau[i] = int(reseau[i])

    matrice_sr = []             #adresse du SR
    matrice_sr_broadcast=[]     #adresse du broadcast 
    matrice_sr_premiere_ip=[]   #adresse de la première ip dans le SR
    matrice_sr_derniere_ip=[]   #adresse de la dernière ip dans le SR

    pas = 2**(8 - nbr_bits_dans_octet)  #calcul du pas 
    print("Num SR   adresse reseau      pas   broadcast          premiere IP             derniere IP")
    for i in range(nbr_sr):

        matrice_sr.append( reseau.copy())# le .copy me permet de garder une référence unique de chaque réseau 
        matrice_sr_broadcast.append(reseau.copy())
        # on récupère la valeur du dernier qu'on a ajouté dans la liste matrice_sr_broadcast 
        #le broadcast est égal à l'ip du réseau suivant -1 
        matrice_sr_broadcast[i][octet_travaille]+=(pas-1)

        matrice_sr_premiere_ip.append(reseau.copy())
        matrice_sr_premiere_ip[i][octet_travaille]+=1

        matrice_sr_derniere_ip.append(reseau.copy())
        matrice_sr_derniere_ip[i][octet_travaille]+=(pas-2)
        
        if reseau[octet_travaille] + pas <= 255:
            reseau[octet_travaille] += pas
        else:
            if (reseau[octet_report] + 1 )<=255:
                reseau[octet_travaille] = 0
                reseau[octet_report] += 1
            elif(reseau[octet_report-1] +1)<=255:
                reseau[octet_travaille]=0 
                reseau[octet_report]=0
                reseau[octet_report-1]+=1
            else: 
                reseau[octet_travaille]=0
                reseau[octet_report]=0
                reseau[octet_report-1]=0
                reseau[octet_report-2]+=1

        print("%-8s %-20s %-3s %-20s %-20s %-20s" % (i+1,matrice_sr[i],pas,matrice_sr_broadcast[i],matrice_sr_premiere_ip[i],matrice_sr_derniere_ip[i]))
    ##valeur_pas_sr=2**(nbr_bits_machines-nbr_bits_empruntes)
        
# nouveau pas défininif 
def validIPV2(ip):

    while True:

        userIP = ip.strip()
        segments = userIP.split(".")
        

        if len(segments) == 4:
            if all(
                s.isdigit() and 0 <= int(s) <= 255
                for s in segments
            ):
                return segments

        print("IP incorrecte.")

        

        
        return 



def cleanScreen():
    # 'nt' = Windows, 'posix' = Linux/macOS
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


##var_test ="192.168.255.0"
##test 
##decoupe_reseau_par_nombre_sr(var_test, 20, 20)
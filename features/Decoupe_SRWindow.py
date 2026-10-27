from . import tool
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout
from PyQt6.QtWidgets import QTableWidget,QTableWidgetItem,QAbstractItemView
# --- import fenêtre --- # 
from . import menuWindow
from . import session

class Decoupe_SRWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- instances des fenêtres appelées = null --- #
        self.menuWindow = None
        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")

        # --- layout haut (titre) --- #
        layout_haut = QHBoxLayout()

        label_titre = QLabel("Découpe en sous-réseaux sur base du nombre de sous-réseaux")
        label_titre.setObjectName("label_titre")
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_haut.addWidget(label_titre)

        # --- Layout principal de la fenêtre --- #
        layout_principal = QVBoxLayout()

        # --- Layout du widget action utilisateur --- #
        layout_entree = QVBoxLayout()

        # --- champ et label associé aux actions utilisateur --- #
        label_reseau = QLabel("Réseau :")
        self.champ_reseau = QLineEdit()
        self.champ_reseau.setObjectName("label_action")
        
        label_masqueCLess = QLabel("Masque classless :")
        self.champ_masqueCLess = QLineEdit()
 
        self.champ_masqueCLess.setObjectName("label_action")

        label_nb_sousreseau = QLabel("Nombre de sous-réseaux :")
        self.champ_nb_sousreseau = QLineEdit()
  
        self.champ_nb_sousreseau.setObjectName("label_action")

        # --- composition du layout d'actions --- #
        layout_champs = QHBoxLayout()

        layout_champs.addWidget(label_reseau)
        layout_champs.addWidget(self.champ_reseau)

        layout_champs.addWidget(label_masqueCLess)
        layout_champs.addWidget(self.champ_masqueCLess)

        layout_champs.addWidget(label_nb_sousreseau)
        layout_champs.addWidget(self.champ_nb_sousreseau)

        layout_champs.setSpacing(5)

        # --- labels de validation --- #
        self.message_erreur = QLabel("")
        self.message_erreur.setObjectName("message_erreur")
       
        self.message_valide = QLabel("")
        self.message_valide.setObjectName("message_valide")

        layout_entree.addLayout(layout_champs)
        layout_entree.addWidget(self.message_erreur)
        layout_entree.addWidget(self.message_valide)

        # --- création du tableau de données --- #
        Widget_table = QWidget()
        layout_table = QVBoxLayout(Widget_table)

        self.tableDecoupe_SR = QTableWidget()
        self.tableDecoupe_SR.setObjectName("tableau_decoupe_sr")
        
        self.tableDecoupe_SR.setMinimumWidth(520)
        self.tableDecoupe_SR.setMaximumHeight(350)
        self.tableDecoupe_SR.setColumnCount(6)
        self.tableDecoupe_SR.setHorizontalHeaderLabels([
                                "N°",
                                "Réseau",
                                "Pas",
                                "Broadcast",
                                "Première IP",
                                "Dernière IP"
                            ])
         
        # Largeur des colonnes
        self.tableDecoupe_SR.setColumnWidth(0, 30)   # N°
        self.tableDecoupe_SR.setColumnWidth(1, 110)  # Réseau
        self.tableDecoupe_SR.setColumnWidth(2, 35)   # Pas
        self.tableDecoupe_SR.setColumnWidth(3, 110)  # Broadcast
        self.tableDecoupe_SR.setColumnWidth(4, 110)  # Première IP
        self.tableDecoupe_SR.setColumnWidth(5, 110)  # Dernière IP
        
        # Empêcher la modification des cellules
        self.tableDecoupe_SR.setEditTriggers( QAbstractItemView.EditTrigger.NoEditTriggers)
         # Masquer les numéros de lignes à gauche
        self.tableDecoupe_SR.verticalHeader().setVisible(False)
        
        # Toujours afficher la barre de défilement verticale
        self.tableDecoupe_SR.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        layout_table.addWidget(self.tableDecoupe_SR)

        # Conteneur pour centrer le tableau
        layout_table_principal = QHBoxLayout()
        layout_table_principal.addStretch()
        layout_table_principal.addWidget(Widget_table)
        layout_table_principal.addStretch()

        # --- Layout principal de la fenêtre --- #
        layout_principal.addLayout(layout_entree)
        layout_principal.addLayout(layout_table_principal)

       # --- layout bas (bouton retour, valider) --- #
        layout_bas = QHBoxLayout()
        bouton_retour = QPushButton("Retour")
        bouton_Valider_DecoupeSR = QPushButton("Valider la découpe")
        
        layout_bas.addWidget(bouton_retour)
        layout_bas.addStretch()
        layout_bas.addWidget(bouton_Valider_DecoupeSR)

        # --- composition de la fenêtre --- #
        layout_fenetre = QVBoxLayout(self)
        layout_fenetre.addLayout(layout_haut)
        layout_fenetre.addLayout(layout_principal, stretch=1)
        layout_fenetre.addLayout(layout_bas)

        # --- appel des fonctions et autres fenêtres --- #
        bouton_Valider_DecoupeSR.clicked.connect(self.appel_DecoupeSRWindow)
        bouton_retour.clicked.connect(self.appel_menuWindow)

    def appel_DecoupeSRWindow(self):
        self.message_erreur.setText("")
        self.message_valide.setText("")
        reseau=self.champ_reseau.text()
        masqueCLess=self.champ_masqueCLess.text()
        nombre_sr = self.champ_nb_sousreseau.text()
        
        tool.validIP(self, reseau)
        if self.message_erreur.text() != "":
            return
        #vérfication des champs numériques
        if not masqueCLess.isdigit() or not nombre_sr.isdigit():
            self.message_erreur.setText("Le masque et le nombre de sous-réseaux doivent être des entiers positifs !")
            return
        # si les champs sont des digits, on les convertit en entiers pour les vérifications suivantes
        masqueCLess = int(masqueCLess)
        nombre_sr = int(nombre_sr)
        
        if(masqueCLess < 0 or masqueCLess > 32):
            self.message_erreur.setText("Masque classless invalide !")
            return
        if(nombre_sr <= 1):
            self.message_erreur.setText("Le nombre de sous-réseaux doit être supérieur ou égal à 2 !")
            return

        self.determinerDecoupe()
        matrice_sr, matrice_sr_broadcast, matrice_sr_premiere_ip, matrice_sr_derniere_ip, pas, nbr_sr = tool.decoupe_reseau_par_nombre_sr(
            self,
            self.champ_reseau.text(),
            int(self.champ_masqueCLess.text()),
            int(self.champ_nb_sousreseau.text())
        )
        if matrice_sr==[]:
            return 
        self.tableDecoupe_SR.setRowCount(nbr_sr)

        # Remplissage du tableau
        for i in range(nbr_sr):
            #variables vides pour stocker chaque information d'un seul sous-réseau
            reseauT = ""
            broadcast = ""
            premiere_ip = ""
            derniere_ip = ""
            # on boucle sur les 4 octet pour les transformer en chaînes de caractères 
            for j in range(4):
                reseauT += str(matrice_sr[i][j])
                broadcast += str(matrice_sr_broadcast[i][j])
                premiere_ip += str(matrice_sr_premiere_ip[i][j])
                derniere_ip += str(matrice_sr_derniere_ip[i][j])

                if j < 3:
                    reseauT += "."
                    broadcast += "."
                    premiere_ip += "."
                    derniere_ip += "."
            
            # on crée un tableau avec les infos d'un sous-réseau
            valeurs = [
                str(i + 1),
                reseauT,
                str(pas),
                broadcast,
                premiere_ip,
                derniere_ip
                    ]
            # permet d'accèder à chaque valeur de la ligne indépendament 
            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(valeur)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableDecoupe_SR.setItem(i, colonne, item)
                    
        # Ajustement de l'affichage
        self.tableDecoupe_SR.resizeColumnsToContents()
        self.tableDecoupe_SR.resizeRowsToContents()

    def determinerDecoupe(self):
            # --- récupération ID et username pour l'historique des résultats --- #
            cnx = tool.obtenir_connexion(self)
            curseur = cnx.cursor()
            curseur.execute("SELECT * FROM USER WHERE id = %s", (session.user_actuel,))
            iduser = curseur.fetchone()
           # ajout dans la base de données à la table subnet_division
            curseur.execute(
                 "INSERT INTO subnet_division(id_user,username,subnet , subnet_mask_classless, number_of_subnets) VALUES (%s,%s,%s, %s, %s)",
                 (session.utilisateur_actuel(),iduser[1],self.champ_reseau.text(), self.champ_masqueCLess.text(), self.champ_nb_sousreseau.text())
             )
            curseur.close()
            cnx.commit()
            
    def appel_menuWindow(self):
        # --- ouverture de la fenêtre appelée et fermeture la fenêtre actuelle --- # 
                if self.menuWindow is None :
                    self.menuWindow=menuWindow.Menu_Window()
                    self.menuWindow.show() 
                    self.close()
                else: 
                    self.menuWindow.close()
                    self.menuWindow = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Decoupe_SRWindow()
    fenetre.show()
    sys.exit(app.exec())
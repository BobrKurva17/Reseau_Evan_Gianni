from . import tool
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QComboBox, QHeaderView
# --- import fenêtre --- # 
from . import menuWindow
from . import Communication_MachineWindow
from . import Decoupe_SRWindow


class Historique_ActionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- instances des fenêtres appelées = null --- #
        self.menuWindow = None
        self.CMW = None
        self.D_SRW = None

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")

       # --- label instruction action --- #
        label_titre = QLabel(
            "Historique des actions utilisateurs pour les découpes en sous-réseaux "
            "et la communication entre machines"
        )
        label_titre.setObjectName("label_titre")
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_titre.setWordWrap(True)

        # Choix de l'historique
        self.liste_historique = QComboBox()
        self.liste_historique.addItems([
            "communication entre machines",
            "découpe réseau sur base du nombre de sous réseau"
        ])
        # --- Layout du widget action utilisateur --- #
        layout_choix = QHBoxLayout()
        layout_choix.addWidget(QLabel("Choisissez quel historique vous souhaitez consulter :"))
        layout_choix.addWidget(self.liste_historique, stretch=1)

        # --- création du tableau de données --- #
        self.table_historique = QTableWidget()
        self.table_historique.setFixedSize(750, 300)
        self.table_historique.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_historique.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_historique.verticalHeader().setVisible(False)
        self.table_historique.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table_historique.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Les colonnes se partagent toute la largeur du tableau
        self.table_historique.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Centrer le tableau
        layout_table = QHBoxLayout()
        layout_table.addStretch()
        layout_table.addWidget(self.table_historique)
        layout_table.addStretch()

        # --- layout bas (bouton retour, valider) --- #
        layout_bas = QHBoxLayout()
        bouton_retour = QPushButton("Retour")
        layout_bas.addWidget(bouton_retour)
        layout_bas.addStretch()

        # --- composition de la fenêtre --- #
        layout_fenetre = QVBoxLayout(self)
        layout_fenetre.addWidget(label_titre)
        layout_fenetre.addLayout(layout_choix)
        layout_fenetre.addLayout(layout_table)
        layout_fenetre.addStretch()
        layout_fenetre.addLayout(layout_bas)

        # --- appel des fonctions et autres fenêtres --- #
        self.table_historique.cellDoubleClicked.connect(self.preremplir_champs)
        self.liste_historique.currentTextChanged.connect(self.remplir_table)
        bouton_retour.clicked.connect(self.appel_menuWindow)

        self.remplir_table()

    def preremplir_champs(self):
        #creation du tableau contenant les valeurs de la lignes selectionnés 
        valeurs=[]
        # chaque cellule de la ligne sélectionnée sont ajoutées au tableau valeurs 
        for cellule in self.table_historique.selectedItems():
            valeurs.append(cellule.text())
        # si l'utilisateur choisi l'historique communication .. alors la fenêtre est appelée et 
        # ses champs sont remplis
        if self.liste_historique.currentText() == "communication entre machines":
            #ip1 = 2 , ip2 = 3 
            self.CMW= Communication_MachineWindow.Communication_MachineWindow()
            self.CMW.show()
            self.CMW.champ_ip_M1.setText(valeurs[2])
            self.CMW.champ_ip_M2.setText(valeurs[3])
            self.CMW.champ_masque_classfull_M1.setText(valeurs[4])
            self.CMW.champ_masque_classfull_M2.setText(valeurs[5])
            self.close()
        # idem pour la fenêtre découpe en sous réseaux 
        else : 
            self.D_SRW = Decoupe_SRWindow.Decoupe_SRWindow()
            self.D_SRW.show()
            self.D_SRW.champ_reseau.setText(valeurs[2])
            self.D_SRW.champ_masqueCLess.setText(valeurs[3])
            self.D_SRW.champ_nb_sousreseau.setText(valeurs[4])
            self.close()

    def remplir_table(self):
        if self.liste_historique.currentText() == "communication entre machines":
            # création de la requête à envoyer en bdd pour récupérer toutes les infos de la table concernée 
            requete = ("SELECT id, id_user,username, ip_device_1, ip_device_2, mask_device_1, mask_device_2 "
                       "FROM communication_btw_devices ORDER BY id DESC")
            # création dynamique de l'en tête du tableau car les colonnes différentes 
            entetes = ["N°", "ID utilisateur","Nom utilisateur", "IP machine 1", "IP machine 2",
                       "Masque machine 1", "Masque machine 2"]
        else:
            requete = ("SELECT id, id_user,username, subnet, subnet_mask_classless, number_of_subnets "
                       "FROM subnet_division ORDER BY id DESC")
            # création dynamique de l'en tête du tableau car les colonnes différentes
            entetes = ["N°", "ID utilisateur","Nom utilisateur", "Réseau", "Masque (CIDR)", "Nombre de sous-réseaux"]

        objet_connexion = tool.obtenir_connexion(self)
        curseur = objet_connexion.cursor()
        curseur.execute(requete)
        donnees = curseur.fetchall()
        curseur.close()
        # à chaque appel la table est premièrement vidée 
        self.table_historique.clearContents()
        # on définit les en-têtes 
        self.table_historique.setColumnCount(len(entetes))
        self.table_historique.setHorizontalHeaderLabels(entetes)
        self.table_historique.setRowCount(len(donnees))
        # parcours des valeurs et affectation aux cellules correspondantes 
        for i, valeurs in enumerate(donnees):
            for j, valeur in enumerate(valeurs):
                cellule = QTableWidgetItem(str(valeur))
                cellule.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_historique.setItem(i, j, cellule)

    def appel_menuWindow(self):
        self.menuWindow = menuWindow.Menu_Window()
        self.menuWindow.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Historique_ActionWindow()
    fenetre.show()
    sys.exit(app.exec())

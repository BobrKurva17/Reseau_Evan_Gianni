import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
# --- import fenêtre --- # 
from . import menuWindow
from . import tool
import getpass
from . import session 

class Communication_MachineWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        # --- instances des fenêtres appelées = null --- #
        self.menuW = None

        # --- Layout principal de la fenêtre --- #
        layout_principal = QVBoxLayout(self)

        # --- layout haut (titre) --- #
        layout_haut = QVBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        label_titre=QLabel("Déterminer la communication entre 2 machines")
        label_titre.setObjectName("label_titre")
        label_titre.setFixedSize(500,50)
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- widget contenant le bloc d'action utilisateur --- #
        Widget_input = QWidget()
        Widget_input.setObjectName("conteneur_action")

        # --- Layout du widget action utilisateur --- #
        layout_conteneur_input = QVBoxLayout(Widget_input)
        layout_conteneur_input.setSpacing(25)

        # --- labels de validation --- # 
        self.message_erreur = QLabel("")
        self.message_erreur.setObjectName("message_erreur")

        self.message_valide = QLabel("Résultat de la communication entre les machines :")
        self.message_valide.setObjectName("label_action")

        self.resultat = QLabel("")
        self.resultat.setObjectName("label_action")
        
        # layout des actions relatives aux 2 machines 
        layout_M1 = QHBoxLayout()
        layout_M2 = QHBoxLayout()
        layout_M1.setSpacing(10)
        layout_M2.setSpacing(10)

        # --- champ et label associé aux actions utilisateur --- #
        # MACHINE 1 
        label_ip_M1 = QLabel("Entrer l'IP de la machine 1 :")
        label_ip_M1.setObjectName("label_action")
        label_ip_M1.setFixedWidth(220)

        self.champ_ip_M1 = QLineEdit()
        self.champ_ip_M1.setObjectName("label_chemin")
        self.champ_ip_M1.setFixedWidth(130)

        label_masque_M1 = QLabel("Entrer le masque :")
        label_masque_M1.setObjectName("label_action")
        label_masque_M1.setFixedWidth(220)
        self.champ_masque_classfull_M1 = QLineEdit()
        self.champ_masque_classfull_M1.setObjectName("label_chemin")
        self.champ_masque_classfull_M1.setFixedWidth(130)

        # MACHINE 2 
        label_ip_M2 = QLabel("Entrer l'IP de la machine 2 :")
        label_ip_M2.setObjectName("label_action")
        label_ip_M2.setFixedWidth(220)

        self.champ_ip_M2 = QLineEdit()
        self.champ_ip_M2.setObjectName("label_chemin")
        self.champ_ip_M2.setFixedWidth(130)

        label_masque_M2 = QLabel("Entrer le masque :")
        label_masque_M2.setObjectName("label_action")
        label_masque_M2.setFixedWidth(220)
        self.champ_masque_classfull_M2 = QLineEdit()
        self.champ_masque_classfull_M2.setObjectName("label_chemin")
        self.champ_masque_classfull_M2.setFixedWidth(130)

        # --- composition du layout d'actions --- #
        layout_M1.addWidget(label_ip_M1)
        layout_M1.addWidget(self.champ_ip_M1)
        layout_M1.addStretch()
        layout_M1.addWidget(label_masque_M1)
        layout_M1.addWidget(self.champ_masque_classfull_M1)

        layout_M2.addWidget(label_ip_M2)
        layout_M2.addWidget(self.champ_ip_M2)
        layout_M2.addStretch()
        layout_M2.addWidget(label_masque_M2)
        layout_M2.addWidget(self.champ_masque_classfull_M2)

        # --- composition du layout d'actions --- #
        layout_conteneur_input.addLayout(layout_M1)
        layout_conteneur_input.addLayout(layout_M2)
        layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_conteneur_input.addWidget(self.message_valide, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_conteneur_input.addWidget(self.resultat, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- layout bas (bouton retour, valider) --- #
        layout_bas = QHBoxLayout()
       
        bouton_retour = QPushButton("Retour")
        bouton_valider = QPushButton("Déterminer le réseau")

        layout_bas.addWidget(bouton_retour, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_bas.addWidget(bouton_valider, alignment=Qt.AlignmentFlag.AlignRight)

        # --- composition de la fenêtre --- #
        layout_haut.addWidget(label_titre,alignment=Qt.AlignmentFlag.AlignCenter)
        layout_haut.addWidget(Widget_input)
        layout_principal.addLayout(layout_haut)
        layout_principal.addLayout(layout_bas)

        # --- appel des fonctions et autres fenêtres --- #
        bouton_valider.clicked.connect(self.determinerCommunication)
        bouton_retour.clicked.connect(self.appel_menuWindow)

    def appel_menuWindow(self):
    # --- ouverture de la fenêtre appelée et fermeture la fenêtre actuelle --- # 
        if self.menuW is None :
            self.menuW=menuWindow.Menu_Window()
            self.menuW.show() 
            self.close()
        else: 
            self.menuW.close()
            self.menuW = None

    def determinerCommunication(self):
        #si les champs sont valides, on appelle la fonction de comparaison des réseaux
        self.demandeValidation_IP()
        # --- récupération ID et username pour l'historique des résultats --- #
        cnx = tool.obtenir_connexion(self)
        curseur = cnx.cursor()
        curseur.execute("SELECT * FROM USER WHERE id = %s", (session.user_actuel,))
        iduser = curseur.fetchone()
        # ajout des données à la table historique communication .. 
        curseur.execute(
             "INSERT INTO communication_btw_devices (id_user,username,ip_device_1, ip_device_2, mask_device_1, mask_device_2) VALUES (%s,%s,%s, %s, %s, %s)",
             (session.utilisateur_actuel(),iduser[1],self.champ_ip_M1.text(), self.champ_ip_M2.text(), self.champ_masque_classfull_M1.text(), self.champ_masque_classfull_M2.text())
         )
        curseur.close()
        cnx.commit()
        
    def demandeValidation_IP(self):
        # Effacer les anciens messages
        self.message_erreur.setText("")
        self.message_valide.setText("")
        ip_M1 = self.champ_ip_M1.text().strip()
        masque_M1 = self.champ_masque_classfull_M1.text().strip()
        ip_M2 = self.champ_ip_M2.text().strip()
        masque_M2 = self.champ_masque_classfull_M2.text().strip()
        #Vérification de la validité des IP et masques
        #Machine1
        tool.validIP(self, ip_M1)
        if self.message_erreur.text() != "":
            return
        tool.validIP(self,masque_M1)
        if self.message_erreur.text() != "":
            return
        tool.MasqueValide(self, masque_M1)
        if self.message_erreur.text() != "":
            return
        #Machine2
        tool.validIP(self, ip_M2)
        if self.message_erreur.text() != "":
            return
        tool.validIP(self,masque_M2)
        if self.message_erreur.text() != "":
            return
        tool.MasqueValide(self, masque_M2)
        if self.message_erreur.text() != "":
            return
        tool.compareNetwork(self, self.champ_ip_M1.text(), self.champ_masque_classfull_M1.text(),
                                     self.champ_ip_M2.text(), self.champ_masque_classfull_M2.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Communication_MachineWindow()
    fenetre.show()
    sys.exit(app.exec())
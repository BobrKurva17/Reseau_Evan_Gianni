from . import tool
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
# --- import fenêtre --- # 
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit
from . import menuWindow

class Reseau_SousReseau_Window(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)

            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            # --- instances des fenêtres appelées = null --- #
            self.menuW = None
            # --- Layout principal de la fenêtre --- #
            layout_principal = QVBoxLayout(self)
            # --- layout haut (titre) --- #
            layout_haut=QVBoxLayout()
            layout_haut.setContentsMargins(150, 100, 150, 200)

            label_titre=QLabel("Déterminer le réseau")
            label_titre.setObjectName("label_titre")
            label_titre.setFixedSize(300,50)
            label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # --- widget contenant le bloc d'action utilisateur --- #
            Widget_input = QWidget()
            Widget_input.setObjectName("conteneur_action")

            # --- Layout du widget action utilisateur --- #
            layout_conteneur_input = QVBoxLayout(Widget_input)
  
           # --- labels de validation --- #
            self.message_erreur = QLabel("")
            self.message_erreur.setObjectName("message_erreur")

            self.message_valide = QLabel("")
            self.message_valide.setObjectName("message_valide")

            # --- champ et label associé aux actions utilisateur --- #
            # IP
            layout_Ip = QHBoxLayout()
            label_IP = QLabel("Entrer l'IP :")
            label_IP.setObjectName("label_action")
            self.champ_ip = QLineEdit()
            self.champ_ip.setObjectName("label_chemin")
            self.champ_ip.setFixedWidth(200)
            layout_Ip.addWidget(label_IP,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_Ip.addWidget(self.champ_ip)
            layout_Ip.addStretch()
            layout_Ip.setSpacing(53)
            # Masque
            layout_masque = QHBoxLayout()
            label_masque = QLabel("Entrer le masque :")
            label_masque.setObjectName("label_action")
            self.champ_masque_classfull = QLineEdit()
            self.champ_masque_classfull.setObjectName("label_chemin")
            self.champ_masque_classfull.setFixedWidth(200)
            layout_masque.addWidget(label_masque,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_masque.addWidget(self.champ_masque_classfull)
            layout_masque.addStretch()

            self.label_sous_reseau = QLabel("le sous-réseau est :")
            self.label_sous_reseau.setObjectName("label_action")

            self.label_reseau = QLabel("le réseau :")
            self.label_reseau.setObjectName("label_action")
            # --- label instruction action --- #
            label_input = QLabel("Entrer votre adresse IP au format 192.168.12.0 pour obtenir la classe du masque de l'IP")
            label_input.setObjectName("label_action")

            # --- composition du layout d'actions --- #
            layout_conteneur_input.addWidget(label_input, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addLayout(layout_Ip)      
            layout_conteneur_input.addLayout(layout_masque)  
            layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_valide, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.label_reseau, alignment=Qt.AlignmentFlag.AlignLeft)
            layout_conteneur_input.addWidget(self.label_sous_reseau, alignment=Qt.AlignmentFlag.AlignLeft)
           

            # --- layout bas (bouton retour, valider) --- #
            layout_bas = QHBoxLayout()
            bouton_retour = QPushButton("Retour")
            bouton_valider = QPushButton("Déterminer le réseau")

             # --- composition de la fenêtre --- #
            layout_bas.addWidget(bouton_retour,alignment=Qt.AlignmentFlag.AlignLeft)
            layout_bas.addWidget(bouton_valider,alignment=Qt.AlignmentFlag.AlignRight)

            layout_haut.addWidget(label_titre,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_haut.addWidget(Widget_input)
           
            layout_principal.addLayout(layout_haut)
            layout_principal.addLayout(layout_bas)

            # --- appel des fonctions et autres fenêtres --- # 
            bouton_valider.clicked.connect(self.demandeValidation_IP)
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

    def demandeValidation_IP(self):
        self.message_erreur.setText("")
        #récup champ de l'ip 
        ip_a_verifier = self.champ_ip.text()
        #récup champ du masque 
        masque_a_verifier = self.champ_masque_classfull.text()
        #vérif format de l'adresse ip
        tool.validIP(self, ip_a_verifier)
        if self.message_erreur.text() != "":
            return
        #vérif format du masque en classfull
        tool.validIP(self, masque_a_verifier)
        if self.message_erreur.text() != "":
            return
        #vérif du format logique du masque (pas possible d'avoir 255.0.255.0)
        tool.MasqueValide(self, masque_a_verifier)
        if self.message_erreur.text() != "":
            return
        # si tout est ok alors on peut calculer le RES et SR
        tool.calculerReseauClassfull(self, ip_a_verifier, masque_a_verifier)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Reseau_SousReseau_Window()
    fenetre.show()
    sys.exit(app.exec())

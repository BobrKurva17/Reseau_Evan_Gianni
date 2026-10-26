import tool
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit
import menuWindow as menuWindow

class ClasseIP_Window(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)

            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            self.menuW = None
            # 1. Layout principal de la fenêtre
            layout_principal = QVBoxLayout(self)

            layout_haut=QVBoxLayout()
            layout_haut.setContentsMargins(150, 100, 150, 200)
            # 2. Widget conteneur pour la saisie de l'IP
            Widget_input = QWidget()
            Widget_input.setObjectName("conteneur_action")

            # 3. Layout du widget de saisie
            layout_conteneur_input = QVBoxLayout(Widget_input)
            

            # 4. Éléments de saisie
            self.message_erreur = QLabel("")
            self.message_erreur.setObjectName("message_erreur")

            self.message_valide = QLabel("")
            self.message_valide.setObjectName("message_valide")
            
            self.champ_ip = QLineEdit()
            self.champ_ip.setObjectName("label_chemin")

            self.label_classe = QLabel("La classe de l'IP est:")
            self.label_classe.setObjectName("label_action")

            self.label_adresse_specifique=QLabel("l'adresse de L'IP est :")
            self.label_adresse_specifique.setObjectName("label_action")



            self.label_privee=QLabel("L'adresse IP est privée :")
            self.label_privee.setObjectName("label_action")

            self.label_reserver=QLabel("L'adresse IP est réservée :")
            self.label_reserver.setObjectName("label_action")

            label_titre=QLabel("Validation adresse IP")
            label_titre.setObjectName("label_titre")
            label_titre.setFixedSize(300,50)
            label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label_input = QLabel("Entrer votre adresse IP au format 192.168.12.0 pour obtenir la classe du masque de l'IP")
            label_input.setObjectName("label_action")

            layout_conteneur_input.addWidget(label_input, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.champ_ip, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_valide, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.label_classe, alignment=Qt.AlignmentFlag.AlignLeft)
            layout_conteneur_input.addWidget(self.label_adresse_specifique, alignment=Qt.AlignmentFlag.AlignLeft)
            layout_conteneur_input.addWidget(self.label_privee, alignment=Qt.AlignmentFlag.AlignLeft)
            layout_conteneur_input.addWidget(self.label_reserver, alignment=Qt.AlignmentFlag.AlignLeft)
            # 5. Layout des boutons
            layout_bas = QHBoxLayout()

            bouton_retour = QPushButton("Retour")
            bouton_valider = QPushButton("Valider l'IP")

            layout_bas.addWidget(bouton_retour,alignment=Qt.AlignmentFlag.AlignLeft)
            layout_bas.addWidget(bouton_valider,alignment=Qt.AlignmentFlag.AlignRight)

            # 6. Composition finale de la fenêtre
            layout_haut.addWidget(label_titre,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_haut.addWidget(Widget_input)
            layout_principal.addLayout(layout_haut)
            layout_principal.addLayout(layout_bas)

            #action 
            bouton_valider.clicked.connect(self.appel_determinerClasse)
            bouton_retour.clicked.connect(self.appel_menuWindow)
            
    def appel_menuWindow(self):
    #instanciation des autres fenêtres possibles 
            if self.menuW is None :
                self.menuW=menuWindow.Menu_Window()
                self.menuW.show() 
                self.close()
            else: 
                self.menuW.close()
                self.menuW = None
    def appel_determinerClasse(self):
        self.message_erreur.setText("")
        self.message_valide.setText("")
        ip_a_verifier = self.champ_ip.text()

        #première vérification l'entrée respecte le format IPv4
        tool.validIP(self, ip_a_verifier)
        if self.message_erreur.text() != "":
            return
        #si format ok alors on détermine la classe 
        masqueDecimal,classe_a_envoyer,type_adresse_a_envoyer, estPrivee,estReserver=tool.classIP(self,ip_a_verifier)
        self.label_classe.setText(f"La classe de l'IP est : {classe_a_envoyer}")
        self.label_adresse_specifique.setText(f"l'adresse de L'IP est : {type_adresse_a_envoyer}")
        self.label_privee.setText(f"L'adresse IP est privée : {estPrivee}")
        self.label_reserver.setText(f"L'adresse IP est réservée : {estReserver}")


            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = ClasseIP_Window()
    fenetre.show()
    sys.exit(app.exec())

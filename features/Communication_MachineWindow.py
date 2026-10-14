import tool 
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget
from PyQt6.QtWidgets import  QLineEdit
import features.menuWindow as menuWindow

class Communication_MachineWindow(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)

            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            self.menuW = None
            # 1. Layout principal de la fenêtre
            layout_principal = QVBoxLayout(self)

            layout_haut=QHBoxLayout()
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

            # Ligne pour l'IP de la machine 1 
            layout_ip_M1 = QHBoxLayout()
            label_ip_M1 = QLabel("Entrer l'IP de la machine 1:")
            label_ip_M1.setObjectName("label_action")

            self.champ_ip_M1 = QLineEdit()
            self.champ_ip_M1.setObjectName("label_chemin")
            self.champ_ip_M1.setFixedWidth(200)

            # ligne pour l'IP de la machine 2 
            layout_ip_M2 = QHBoxLayout()
            layout_ip_M2 = QLabel("Entrer l'IP de la machine 1:")
            layout_ip_M2.setObjectName("label_action")
            
            self.champ_ip_M2 = QLineEdit()
            self.champ_ip_M2.setObjectName("label_chemin")
            self.champ_ip_M2.setFixedWidth(200)

            #ajout des inputs au widget principale (machine1)
            layout_ip_M1.addWidget(layout_ip_M1,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_ip_M1.addWidget(self.champ_ip_M1)
            layout_ip_M1.addStretch()
            layout_ip_M1.setSpacing(53)

            #ajout des inputs au widget principale (machine2)
            layout_ip_M2.addWidget(layout_ip_M2,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_ip_M2.addWidget(self.champ_ip_M2)
            layout_ip_M2.addStretch()
            layout_ip_M2.setSpacing(53)

            
            #masque de la machine 1
            layout_masque_M1 = QHBoxLayout()
            layout_masque_M1 = QLabel("Entrer le masque :")
            layout_masque_M1.setObjectName("label_action")

            self.champ_masque_classfull_M1 = QLineEdit()
            self.champ_masque_classfull_M1.setObjectName("label_chemin")
            self.champ_masque_classfull_M1.setFixedWidth(200)

            layout_masque_M1.addWidget(layout_masque_M1,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_masque_M1.addWidget(self.champ_masque_classfull_M1)
            layout_masque_M1.addStretch()
            #masque de la machine 2 
            layout_masque_M2 = QHBoxLayout()
            layout_masque_M2 = QLabel("Entrer le masque :")
            layout_masque_M2.setObjectName("label_action")
            
            self.champ_masque_classfull_M2 = QLineEdit()
            self.champ_masque_classfull_M2.setObjectName("label_chemin")
            self.champ_masque_classfull_M2.setFixedWidth(200)
            
            layout_masque_M2.addWidget(layout_masque_M1,alignment=Qt.AlignmentFlag.AlignCenter)
            layout_masque_M2.addWidget(self.champ_masque_classfull_M1)
            layout_masque_M2.addStretch()

            self.label_sous_reseau = QLabel("le sous-réseau est :")
            self.label_sous_reseau.setObjectName("label_action")

            self.label_reseau = QLabel("le réseau :")
            self.label_reseau.setObjectName("label_action")

            label_input = QLabel("Entrer votre adresse IP au format 192.168.12.0 pour obtenir la classe du masque de l'IP")
            label_input.setObjectName("label_action")

            # Ajout des éléments dans le conteneur vertical principal (sans ajouter les inputs seuls)
            layout_conteneur_input.addWidget(label_input, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addLayout(layout_ip_M1)      
            layout_conteneur_input.addLayout(layout_masque)  
            layout_conteneur_input.addWidget(self.message_erreur, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.message_valide, alignment=Qt.AlignmentFlag.AlignCenter)
            layout_conteneur_input.addWidget(self.label_reseau, alignment=Qt.AlignmentFlag.AlignLeft)
            layout_conteneur_input.addWidget(self.label_sous_reseau, alignment=Qt.AlignmentFlag.AlignLeft)
           

            # 5. Layout des boutons
            layout_bas = QHBoxLayout()

            bouton_retour = QPushButton("Retour")
            bouton_valider = QPushButton("Déterminer le réseau")

            layout_bas.addWidget(bouton_retour,alignment=Qt.AlignmentFlag.AlignLeft)
            layout_bas.addWidget(bouton_valider,alignment=Qt.AlignmentFlag.AlignRight)

            # 6. Composition finale de la fenêtre
            layout_haut.addWidget(Widget_input)
           
            
            layout_principal.addLayout(layout_haut)
            layout_principal.addLayout(layout_bas)

            #action 
            bouton_valider.clicked.connect(self.demandeValidation_IP)
            bouton_retour.clicked.connect(self.appel_menuWindow)
            #self.champ_ip.textChanged.connect(lambda: tool.validIP(self))
            #self.champ_masque_classfull.textChanged.connect(lambda: tool.validIP(self))

    def appel_menuWindow(self):
    #instanciation des autres fenêtres possibles 
            if self.menuW is None :
                self.menuW=menuWindow.Menu_Window()
                self.menuW.show() 
                self.close()
            else: 
                self.menuW.close()
                self.menuW = None

  

            
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Reseau_SousReseau_Window()
    fenetre.show()
    sys.exit(app.exec())

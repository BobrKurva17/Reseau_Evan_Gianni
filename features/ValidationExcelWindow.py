from . import tool
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout
from PyQt6.QtWidgets import  QLineEdit
# --- import fenêtre --- # 
from . import CIDRWindow

class ValidationExcel_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(400, 250, 475, 300)
        self.setWindowTitle("IPPY")
        # --- instances des fenêtres appelées = null --- #
        self.CIDRW = None 

        # --- Layout principal de la fenêtre --- #
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 25)

        # --- Layout  action utilisateur --- #
        layout_input = QVBoxLayout()
        layout_input.setSpacing(10)

        label_chemin = QLabel(
            "Insérez le chemin absolu de votre dossier :"
        )
        #donner un nom au label pour le fichier css 
        label_chemin.setObjectName("label_chemin")
        label_chemin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entree_chemin = QLineEdit()

        
        self.entree_chemin.setFixedSize(350, 35)

        # aligner le label dans son layout 
        layout_input.addWidget(label_chemin,alignment=Qt.AlignmentFlag.AlignCenter)
        # aligner l'input dans son layout
        layout_input.addWidget(self.entree_chemin,alignment=Qt.AlignmentFlag.AlignCenter)
        # --- labels de validation --- #
        self.message_erreur = QLabel("")
        self.message_erreur.setObjectName("message_erreur")

        layout_input.addWidget(self.message_erreur)
       
        # --- layout bas (bouton retour, valider) --- #
        layout_bas = QHBoxLayout()
        bouton_retour = QPushButton("Retour")
        bouton_retour.setObjectName("bouton")
        bouton_valider = QPushButton("Valider")
        bouton_valider.setObjectName("bouton_valider")

        layout_bas.addWidget(bouton_retour)
        layout_bas.addStretch()
        layout_bas.addWidget(bouton_valider)

        # --- composition de la fenêtre --- #
        layout_principal.addLayout(layout_input)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_bas)
        # --- appel des fonctions et autres fenêtres --- #
        bouton_valider.clicked.connect(lambda: tool.exporterTableau(self))
        bouton_retour.clicked.connect(self.appel_CIDRWindow)

    def appel_CIDRWindow(self):
            # --- ouverture de la fenêtre appelée et fermeture la fenêtre actuelle --- # 
            if self.CIDRW is None :
                self.CIDRW=CIDRWindow.CIDR_Window()
                self.CIDRW.show() 
                self.close()
            else: 
                self.CIDRW.close()
                self.CIDRW = None       


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = ValidationExcel_Window()
    fenetre.show()
    sys.exit(app.exec())
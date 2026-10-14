import tool
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout

class Premiere_Connection_Windows(QDialog):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Premiere_Connection_Windows()
    fenetre.show()
    sys.exit(app.exec())
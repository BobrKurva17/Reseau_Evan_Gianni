import tool 
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QTableWidget,QTableWidgetItem
from PyQt6.QtWidgets import  QLineEdit
import menuWindow

class ValidationInput_Window(QDialog):
     def __init__(self, parent=None):
            super().__init__(parent)
            self.setGeometry(250, 100, 1000, 750)
            self.setWindowTitle("IPPY")
            menuW = None 

            layout_principal = QVBoxLayout()
            # Tableau contenant l'historique des ip entrées et validées 
            layout_Tableau_Ip_Historique = QHBoxLayout(layout_principal)
           # partie où l'utilisateur peut entrer l'ip dans l'input            
            layout_input_validations = QHBoxLayout(layout_principal)
            # layout bas contenant les boutons retour , valider , ect .. 
            layout_bas = QHBoxLayout(layout_principal)

            Table_Historique_inputs = QTableWidget(3,2)
            Table_Historique_inputs.setHorizontalHeaderLabels(
                        ["Numéro de l'input","Input"]
                    )
            Table_Historique_inputs.setFixedSize(520, 600)
            #var_tab_inputs = 
            for ligne, c in enumerate(var_tab_inputs):
                        #affecter l'indice de la valeur de sa ligne 
                        item0 = QTableWidgetItem(c[0])
                        item1 = QTableWidgetItem(c[1])
                       
                        # aligner les items 
                        item0.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        
                        # affecter la valeur à la bonne cellule du tableau (par ligne)
                        Table_Historique_inputs.setItem(ligne, 0, item0)
                        Table_Historique_inputs.setItem(ligne, 1, item1)
                        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = ValidationInput_Window()
    fenetre.show()
    sys.exit(app.exec())

from . import tool
from . import pwd
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget,QTableWidget,QHeaderView,QTableWidgetItem,QRadioButton
from PyQt6.QtWidgets import  QLineEdit,QMessageBox
from . import Menu_Admin_Window

class Liste_Utilisateur_Bloques_Windows(QDialog):

    def charger_utilisateurs(self):
            # Vide le tableau pour éviter de dupliquer les lignes
            self.tableUser.setRowCount(0)
            #remplissage de la table avec les utilisateurs
            cnx = tool.obtenir_connexion(self)
            for user in pwd.printUsersDisabled(cnx):
                rowPosition = self.tableUser.rowCount()
                self.tableUser.insertRow(rowPosition)
                self.tableUser.setItem(rowPosition, 0, QTableWidgetItem(str(user[0])))
                self.tableUser.setItem(rowPosition, 1, QTableWidgetItem(user[1]))
                self.tableUser.setItem(rowPosition, 2, QTableWidgetItem(user[2]))
                #ajout d'un bouton pour désactiver l'utilisateur
                btn_activer = QPushButton("Activer")
                btn_activer.clicked.connect(lambda checked, user_id=user[0]: self.activer_use(user_id))
                self.tableUser.setCellWidget(rowPosition, 3, btn_activer)

    def activer_use(self,id):
            reponse = QMessageBox.question(self,"Confirmer l'activation",
                                 "Souhaitez-vous rétablir cet utilisateur ?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                 QMessageBox.StandardButton.No)
            if(reponse == QMessageBox.StandardButton.Yes):
                cnx = tool.obtenir_connexion(self)
                cursor = cnx.cursor()
                cursor.execute("UPDATE user SET isActive = 1 WHERE id = %s", (id,))
                cnx.commit()
                self.charger_utilisateurs()
                return
            else:
                return
                        
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        self.menuW = None
        # 1. Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        layout_haut=QHBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        #affichage des utilisateurs
        self.tableUser = QTableWidget(0, 4)  # 0 lignes, 3 colonnes
        self.tableUser.setHorizontalHeaderLabels(["Id","Nom d'utilisateur", "Rôle", "Rétablir l'utilisateur"])
        self.tableUser.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # permet la redimension automatique des colonnes pour remplir l'espace disponible
        self.tableUser.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        #chargement des utilisateurs
        self.charger_utilisateurs()

        #bouton de retour
        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.appel_menuAdmin_window)

        layout_haut.addWidget(self.tableUser)
        
        layout_principal.addLayout(layout_haut)
        layout_principal.addWidget(btn_retour)

    def appel_menuAdmin_window(self):
        if self.menuW is None :
            self.menuW=Menu_Admin_Window.Menu_Admin_Window()
            self.menuW.show() 
            self.close()
        else: 
            self.menuW.close()
            self.menuW = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Liste_Utilisateur_Bloques_Windows()
    fenetre.show()
    sys.exit(app.exec())
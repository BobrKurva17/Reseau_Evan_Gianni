from . import tool
from . import pwd
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget,QTableWidget,QHeaderView,QTableWidgetItem,QRadioButton
from PyQt6.QtWidgets import  QLineEdit,QMessageBox
from . import Liste_Utilisateur_Bloques_Windows
from . import menuWindow
class Menu_Admin_Window(QDialog):

    def ajouter_utilisateur(self):
        # Créer une nouvelle fenêtre pour ajouter un utilisateur
        self.ajouter_utilisateur_window = QDialog(self)
        self.ajouter_utilisateur_window.setWindowTitle("Ajouter un utilisateur")
        self.ajouter_utilisateur_window.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(self.ajouter_utilisateur_window)

        # Champ pour le nom d'utilisateur
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.input_username)

        # Champ pour le mot de passe
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Minimum 8 caractères dont 1 chiffre, 1 majuscule et 1 caractère spécial (!@#$%&*?)")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        # Champ pour la confirmation du mot de passe
        self.input_password_confirm = QLineEdit()
        self.input_password_confirm.setPlaceholderText("Retapez votre mot de passe")
        self.input_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password_confirm)

        # Champ pour le rôle
        layout_role = QHBoxLayout()
        self.radio_admin = QRadioButton("Admin")
        self.radio_user = QRadioButton("Utilisateur")
        layout_role.addWidget(self.radio_admin)
        layout_role.addWidget(self.radio_user)
        layout.addLayout(layout_role)

        # Bouton pour valider l'ajout
        btn_valider = QPushButton("Ajouter")
        btn_valider.clicked.connect(self.verification_inscription)
        layout.addWidget(btn_valider)

        # Label pour les messages d'erreur
        self.label_erreur = QLabel()
        self.label_erreur.setStyleSheet("color: red;")

        layout.addWidget(self.label_erreur)

        self.ajouter_utilisateur_window.exec()  # Afficher la fenêtre modale

    def verification_inscription(self):
        self.label_erreur.setText("")  # Réinitialiser le message d'erreur
        mdp = self.input_password.text()
        mdpConfirm = self.input_password_confirm.text()
        utilisateur = self.input_username.text()
        
        #vérification données saisies
        if(not utilisateur):
            self.label_erreur.setText("Le nom d'utilisateur ne peut pas être vide")
            return False

        if(mdp != mdpConfirm):
            self.label_erreur.setText("Les mots de passe ne correspondent pas")
            return False

        if(not pwd.verifierMotDePasse(mdp, self)):
            return False

        if(not (self.radio_admin.isChecked() or self.radio_user.isChecked())):
            self.label_erreur.setText("Veuillez sélectionner un rôle pour l'utilisateur")
            return False

        self.enregistrement_utilisateur()

    def enregistrement_utilisateur(self):
        mdp = self.input_password.text()
        utilisateur = self.input_username.text()
        role = self.radio_admin.isChecked() and "admin" or "user"

        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        user = {
            "username": utilisateur,
            "pswd": pwd.hash_password(mdp),
            "roles": role
        }
        cursor.execute("INSERT INTO user (username, pswd, roles) VALUES (%s, %s, %s)", 
                                (user["username"], user["pswd"], user["roles"]))  
        cnx.commit()
        self.charger_utilisateurs()
        #retour à la fenêtre principale
        self.ajouter_utilisateur_window.close()

    def charger_utilisateurs(self):
        # Vide le tableau pour éviter de dupliquer les lignes
        self.tableUser.setRowCount(0)
        #remplissage de la table avec les utilisateurs
        cnx = tool.obtenir_connexion(self)
        for user in pwd.printUsers(cnx):
            rowPosition = self.tableUser.rowCount()
            self.tableUser.insertRow(rowPosition)
            self.tableUser.setItem(rowPosition, 0, QTableWidgetItem(str(user[0])))
            self.tableUser.setItem(rowPosition, 1, QTableWidgetItem(user[1]))
            self.tableUser.setItem(rowPosition, 2, QTableWidgetItem(user[2]))
            #ajout d'un bouton pour désactiver l'utilisateur
            btn_desactiver = QPushButton("Désactiver")
            btn_desactiver.clicked.connect(lambda checked, user_id=user[0]: self.desactiver_user(user_id))
            if(user[2] == "superadmin" or user[2] == "admin"):
                btn_desactiver.setEnabled(False)
            self.tableUser.setCellWidget(rowPosition, 3, btn_desactiver)
            #ajout d'un bouton pour générer un code secret
            btn_generer_code = QPushButton("Générer")
            btn_generer_code.clicked.connect(lambda checked, user_id=user[0]: self.generer_code(user_id))
            self.tableUser.setCellWidget(rowPosition, 4, btn_generer_code)

    def generer_code(self,id):
        codeSecret = pwd.genererCodeSecret()
        QMessageBox.warning(self, "Code secret généré", f"Le code secret généré est : {codeSecret}\nVeuillez le noter quelque part, il sera nécessaire pour la récupération du mot de passe.")
        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("UPDATE user SET codeSecret = %s WHERE id = %s", (pwd.hash_password(codeSecret),id))
        cnx.commit()
        self.charger_utilisateurs()

    def desactiver_user(self,id):
        reponse = QMessageBox.question(self,"Confirmer le blocage",
                             "Souhaitez-vous vraiment bloquer cet utilisateur ?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                             QMessageBox.StandardButton.No)
        if(reponse == QMessageBox.StandardButton.Yes):
            cnx = tool.obtenir_connexion(self)
            cursor = cnx.cursor()
            cursor.execute("UPDATE user SET isActive = 0 WHERE id = %s", (id,))
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
        self.tableUser = QTableWidget(0, 5)  # 0 lignes, 5 colonnes
        self.tableUser.setHorizontalHeaderLabels(["Id","Nom d'utilisateur", "Rôle", "Désactiver l'utilisateur","Générer un code secret"])
        self.tableUser.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # permet la redimension automatique des colonnes pour remplir l'espace disponible
        self.tableUser.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        #chargement des utilisateurs
        self.charger_utilisateurs()

        #bouton accès aux utilisateur désactivés
        btn_user_desactives = QPushButton("Accéder aux utilisateurs désactivés")
        btn_user_desactives.clicked.connect(self.appel_liste_bloque)

        #bouton d'ajout d'utilisateur
        btn_ajouter_user = QPushButton("Ajouter un utilisateur")
        btn_ajouter_user.clicked.connect(self.ajouter_utilisateur)

        #bouton de retour
        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.appel_menuWindow)

        layout_haut.addWidget(self.tableUser)
        
        layout_principal.addLayout(layout_haut)
        layout_principal.addWidget(btn_user_desactives)
        layout_principal.addWidget(btn_ajouter_user)
        layout_principal.addWidget(btn_retour)
        
    def appel_menuWindow(self):
    #instanciation des autres fenêtres possibles 
        if self.menuW is None :
            self.menuW=menuWindow.Menu_Window()
            self.menuW.show() 
            self.close()
        else: 
            self.menuW.close()
            self.menuW = None

    def appel_liste_bloque(self):
        if self.menuW is None :
            self.menuW=Liste_Utilisateur_Bloques_Windows.Liste_Utilisateur_Bloques_Windows()
            self.menuW.show() 
            self.close()
        else: 
            self.menuW.close()
            self.menuW = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Menu_Admin_Window()
    fenetre.show()
    sys.exit(app.exec())
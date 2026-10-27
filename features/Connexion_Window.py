import sys
from . import pwd
from . import tool
from . import session
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout,QFormLayout,QLineEdit,QMessageBox,QInputDialog
from . import menuWindow
from . import Menu_User_Window

class Connection_Windows(QDialog):

    nbErreurs = 0  # Compteur d'erreurs de connexion
    menuW= None

    def changer_mot_de_passe_window(self):
        # Créer une nouvelle fenêtre pour ajouter un utilisateur
        self.dialog_mdp = QDialog(self)
        self.dialog_mdp.setWindowTitle("Ajouter un utilisateur")
        self.dialog_mdp.setGeometry(300, 200, 400, 300)
        
        layout = QVBoxLayout(self.dialog_mdp)
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

        # Bouton pour valider la modification
        btn_valider = QPushButton("Modifier")
        btn_valider.clicked.connect(self.enregistrer_nouveau_mdp)
        layout.addWidget(btn_valider)

        # Label pour les messages d'erreur
        self.label_erreur = QLabel()
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.dialog_mdp.exec()

    def enregistrer_nouveau_mdp(self):
        self.label_erreur.setText("")  # Réinitialiser le message d'erreur

        nom = self.input_username.text()
        mdp = self.input_password.text()
        mdpConfirm = self.input_password_confirm.text()

        if(mdp != mdpConfirm):
            self.label_erreur.setText("Les mots de passe ne correspondent pas")
            return False

        if(not pwd.verifierMotDePasse(mdp, self)):
            return False

        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("UPDATE user SET pswd = %s WHERE username = %s", (pwd.hash_password(mdp),nom))
        cnx.commit()
        QMessageBox.warning(self, "Confirmation", "Mot de passe changé")
        self.dialog_mdp.close()
        
    def connexion(self):
        session.user_actuel=None
        self.label_erreur.setText("")  # Réinitialiser le message d'erreur
        mdp = self.input_mdp.text()
        utilisateur = self.input_username.text()

        if(not utilisateur):
            self.label_erreur.setText("Le nom d'utilisateur ne peut pas être vide")
            return False

        if(not pwd.verifierMotDePasse(mdp, self)):
            return False

        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (utilisateur,))
        result = cursor.fetchone()

        if result is None:
            self.label_erreur.setText("Nom d'utilisateur incorrect")
            return False
        
        if result[4] == 0:
                    QMessageBox.critical(self, "Erreur", "Votre compte est désactivé. Veuillez contacter l'administrateur.")
                    self.close()
                    return False
        
        if not pwd.verify_password(mdp, result[3]):
            self.label_erreur.setText("Mot de passe incorrect")
            self.nbErreurs += 1
            if self.nbErreurs == 3:
                self.nbErreurs = 0  # Réinitialiser le compteur d'erreurs
                while self.nbErreurs < 3:
                    code, ok = QInputDialog.getText(self, "Code secret", "Entrez le code secret pour réinitialiser le mot de passe :")
                    if not pwd.verify_password(code, result[5]):
                        QMessageBox.critical(self, "Erreur", "Code secret incorrect. Veuillez réessayer.")
                        self.nbErreurs += 1
                    else:
                        QMessageBox.information(self, "Réinitialisation du mot de passe", "Code secret correct. Vous pouvez maintenant réinitialiser votre mot de passe.")
                        self.changer_mot_de_passe_window()
                        break
                if self.nbErreurs == 3:
                    QMessageBox.critical(self, "Erreur", "Nombre maximum de tentatives dépassé. Veuillez contacter l'administrateur.")
                    cursor.execute("UPDATE user SET isActive = 0 WHERE username = %s", (utilisateur,))
                    cnx.commit()
                    self.close()  # Fermer la fenêtre de connexion
            return False
        session.user_actuel=result[0]
        self.appel_menuWindow()
        self.close()  # Fermer la fenêtre de connexion si tout est correct
        

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        self.menuW = None
        # 1. Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        layout_haut=QHBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        formulaireConnexion = QFormLayout()
        # Champ nom d'utilisateur
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Nom d'utilisateur")
        formulaireConnexion.addRow("Nom d'utilisateur:", self.input_username)
        # Champ mot de passe principal
        self.input_mdp = QLineEdit()
        self.input_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_mdp.setPlaceholderText("Minimum 8 caractères dont 1 chiffre, 1 majuscule et 1 caractère spécial (!@#$%&*?)")
        formulaireConnexion.addRow("Mot de passe:", self.input_mdp)
        
        layout_haut.addLayout(formulaireConnexion)
        layout_principal.addLayout(layout_haut)

        # Label pour les messages d'erreur
        self.label_erreur = QLabel()
        self.label_erreur.setStyleSheet("color: red;")

        layout_principal.addWidget(self.label_erreur)

        #Bouton de validation
        btn_valider = QPushButton("Connexion")
        btn_valider.clicked.connect(self.connexion)
        layout_principal.addWidget(btn_valider)


    def appel_menuWindow(self):
            #instanciation des autres fenêtres possibles 
                    if self.menuW is None :
                        self.menuW=menuWindow.Menu_Window()
                        self.menuW.show() 
                        
                    else: 
                        self.menuW.close()
                        self.menuW = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Connection_Windows()
    fenetre.show()
    sys.exit(app.exec())

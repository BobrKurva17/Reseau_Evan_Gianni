import sys
from pwd import verify_password,verifierMotDePasse
from tool import obtenir_connexion
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout,QFormLayout,QLineEdit,QMessageBox,QInputDialog

class Premiere_Connection_Windows(QDialog):

    nbErreurs = 0  # Compteur d'erreurs de connexion

    def connexion(self):
        self.label_erreur.setText("")  # Réinitialiser le message d'erreur
        mdp = self.input_mdp.text()
        utilisateur = self.input_username.text()

        if(not utilisateur):
            self.label_erreur.setText("Le nom d'utilisateur ne peut pas être vide")
            return False

        if(not verifierMotDePasse(mdp, self)):
            return False

        cnx = obtenir_connexion(self)
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
        
        if not verify_password(mdp, result[3]):
            self.label_erreur.setText("Mot de passe incorrect.")
            self.nbErreurs += 1
            if self.nbErreurs == 3:
                self.nbErreurs = 0  # Réinitialiser le compteur d'erreurs
                while self.nbErreurs < 3:
                    code, ok = QInputDialog.getText(self, "Code secret", "Entrez le code secret pour réinitialiser le mot de passe :")
                    if not verify_password(code, result[5]):
                        QMessageBox.critical(self, "Erreur", "Code secret incorrect. Veuillez réessayer.")
                        self.nbErreurs += 1
                    else:
                        QMessageBox.information(self, "Réinitialisation du mot de passe", "Code secret correct. Vous pouvez maintenant réinitialiser votre mot de passe.")
                        # Ici, vous pouvez ajouter la logique pour permettre à l'utilisateur de réinitialiser son mot de passe.
                        break
                if self.nbErreurs == 3:
                    QMessageBox.critical(self, "Erreur", "Nombre maximum de tentatives dépassé. Veuillez contacter l'administrateur.")
                    cursor.execute("UPDATE user SET isActive = 0 WHERE username = %s", (utilisateur,))
                    cnx.commit()
                    self.close()  # Fermer la fenêtre de connexion
            return False

        self.close()  # Fermer la fenêtre de connexion si tout est correct
        return result[0]

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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Premiere_Connection_Windows()
    fenetre.show()
    sys.exit(app.exec())
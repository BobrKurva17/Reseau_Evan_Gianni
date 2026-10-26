from . import tool
import sys
from . import pwd as p
from . import session as s
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QDialog, QVBoxLayout,QHBoxLayout,QWidget,QInputDialog,QMessageBox
from PyQt6.QtWidgets import  QLineEdit
from . import menuWindow

class Menu_User_Window(QDialog):
    s.id_user_actuel = 1

    def changer_nom_utilisateur_window(self):
        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("SELECT username FROM USER WHERE id = %s",(s.id_user_actuel,))
        nom = cursor.fetchone()
        # Créer une nouvelle fenêtre pour modifier le nom de l'utilisateur
        self.changer_nom_utilisateur_window = QDialog(self)
        self.changer_nom_utilisateur_window.setWindowTitle("Modifier nom de l'utilisateur")
        self.changer_nom_utilisateur_window.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(self.changer_nom_utilisateur_window)

        # Champ pour le nom d'utilisateur
        self.input_username = QLineEdit(nom[0])
        self.input_username.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.input_username)

        # Bouton pour valider la modification
        btn_valider = QPushButton("Modifier")
        btn_valider.clicked.connect(self.enregistrer_nouveau_nom)
        layout.addWidget(btn_valider)

        # Label pour les messages d'erreur
        self.label_erreur = QLabel()
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)
        
        self.changer_nom_utilisateur_window.exec()

    def enregistrer_nouveau_nom(self):
        nouveau_nom = self.input_username.text()

        if(not nouveau_nom):
            self.label_erreur.setText("Le nom d'utilisateur ne peut pas être vide")
            return False
        
        if(p.verify_name(self,nouveau_nom)):
            cnx = tool.obtenir_connexion(self)
            cursor = cnx.cursor()
            cursor.execute("UPDATE user SET username = %s WHERE id = %s",(nouveau_nom, s.id_user_actuel))
            cnx.commit()
            self.changer_nom_utilisateur_window.close()
        else:
            self.label_erreur.setText("Le nom d'utilisateur est déjà pris")
            return False

    def verifier_ancien_mot_de_passe(self):
        #Vérifier ancien mot de passe ou code secret
        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM USER WHERE id = %s",(s.id_user_actuel,))
        result = cursor.fetchone()

        self.nbErreurs = 0  # Réinitialiser le compteur d'erreurs
        while self.nbErreurs < 3:
            code, ok = QInputDialog.getText(self, "Code secret", "Entrez le code secret ou l'ancien mdp pour réinitialiser le mot de passe :",QLineEdit.EchoMode.Password)
            # Si l'utilisateur clique sur "Annuler"
            if not ok:
                return
            if (p.verify_password(code, result[5]) or p.verify_password(code, result[3])):
                break
            else:
                QMessageBox.critical(self, "Erreur", "Code secret ou ancien mot de passe incorrect. Veuillez réessayer.")
                self.nbErreurs += 1

        if self.nbErreurs == 3:
            QMessageBox.critical(self, "Erreur", "Nombre maximum de tentatives dépassé. Veuillez contacter l'administrateur pour obtenir un code secret.")
            return
        
        self.changer_mot_de_passe_window()
        
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
        mdp = self.input_password.text()
        mdpConfirm = self.input_password_confirm.text()

        if(mdp != mdpConfirm):
            self.label_erreur.setText("Les mots de passe ne correspondent pas")
            return False

        if(not p.verifierMotDePasse(mdp, self)):
            return False

        cnx = tool.obtenir_connexion(self)
        cursor = cnx.cursor()
        cursor.execute("UPDATE user SET pswd = %s WHERE id = %s", (p.hash_password(mdp),s.id_user_actuel))
        cnx.commit
        QMessageBox.warning(self, "Confirmation", "Mot de passe changé")
        self.dialog_mdp.close()
        
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")
        self.menuW = None
        # 1. Layout principal de la fenêtre
        layout_principal = QVBoxLayout(self)

        layout_haut=QHBoxLayout()
        layout_haut.setContentsMargins(150, 100, 150, 200)

        formulaireUser = QVBoxLayout()
        # Bouton changer de mot de passe
        btn_changer_mdp = QPushButton("Changer de mot de passe")
        btn_changer_mdp.clicked.connect(self.verifier_ancien_mot_de_passe)
        formulaireUser.addWidget(btn_changer_mdp)
        #Bouton changer de nom d'utilisateur
        btn_changer_username = QPushButton("Changer de nom d'utilisateur")
        btn_changer_username.clicked.connect(self.changer_nom_utilisateur_window)
        formulaireUser.addWidget(btn_changer_username)
        #bouton de retour
        btn_retour = QPushButton("Retour")
        btn_retour.clicked.connect(self.appel_menuWindow)
        formulaireUser.addWidget(btn_retour)

        layout_haut.addLayout(formulaireUser)     
        layout_principal.addLayout(layout_haut)


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

    fenetre = Menu_User_Window()
    fenetre.show()
    sys.exit(app.exec())
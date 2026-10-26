from . import tool
import sys
from . import session 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout
from . import CIDRWindow

from . import ValidationInput_Window
from . import ClasseIP_Window
from . import Reseau_SousReseau_Window
from . import Communication_MachineWindow
from . import Decoupe_SRWindow
from . import Masque_ClasseWindow
from . import Historique_ActionWindow
from . import Menu_Admin_Window
from . import Menu_User_Window
class Menu_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("Test")

        #initialisation de l'instance de la fenêtre CIDRWindows permet le retour en arriêre 
        self.CIDRW = None 
        self.VIW = None 
        self.CLIW = None
        self.RES_SRW = None
        self.COM_MW = None
        self.DECOUPE_SRW = None
        self.CLASS_IPW = None
        self.HAW = None
        self.MA = None 
        self.MU = None

        cnx = tool.obtenir_connexion(self)
        curseur = cnx.cursor()
        curseur.execute("SELECT * FROM USER WHERE id = %s", (session.user_actuel,))
        self.utilisateur_actuel = curseur.fetchone()
        # marges autour du panneau : laissent voir le fond
        layout_principal = QVBoxLayout(self)
        ##layout_principal.setContentsMargins(10, 20, 60, 40)

        # panneau central
        zone_boutons = QFrame()
        ##zone_boutons.setFixedWidth(600)
        zone_boutons.setObjectName("zone_boutons")

        # marges internes : le label et les boutons ne touchent pas les bords du panneau
        self.layout_boutons = QVBoxLayout(zone_boutons)
        self.layout_boutons.setContentsMargins(60, 30, 60, 30)
        self.layout_boutons.setSpacing(10)

        label_boutons = QLabel("Que souhaitez vous faire aujourd'hui ?")
        label_boutons.setObjectName("label_boutons")
        label_boutons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonCIDR = QPushButton("Tableau CIDR")
        self.buttonIP_Format_Valide = QPushButton("Vérifier votre IP")
        self.buttonClasse_IP = QPushButton("Déterminer la classe de votre IP")
        self.buttonMasque_IP = QPushButton("Déterminer le masque de classe de votre IP")
        self.buttonReseau_SR = QPushButton("Déterminer le réseau et sous-réseau")
        self.buttonMeme_reseau = QPushButton("Déterminer comment 2 machines communiquent")
        self.buttonDecoupe_SR = QPushButton("Découper un réseau en sous-réseaux")
        self.buttonHistorique = QPushButton("Historique des actions utilisateurs")
        self.buttonProfil = QPushButton("Profil")

        self.layout_boutons.addStretch()          # centre le contenu verticalement
        self.layout_boutons.addWidget(label_boutons)
        for bouton in (self.buttonCIDR, self.buttonIP_Format_Valide, self.buttonClasse_IP,
                       self.buttonMasque_IP, self.buttonReseau_SR, self.buttonMeme_reseau, self.buttonDecoupe_SR, self.buttonHistorique, self.buttonProfil):
            self.layout_boutons.addWidget(bouton)
        self.layout_boutons.addStretch()
        self.Acces_Admin()
        layout_principal.addWidget(zone_boutons, alignment=Qt.AlignmentFlag.AlignCenter)
        # ligne du bas : bouton retour à gauche
        layout_bas = QHBoxLayout()
        self.bouton_retour = QPushButton("Retour")
        self.bouton_retour.setObjectName("bouton_retour")
        layout_bas.addWidget(self.bouton_retour)
        layout_bas.addStretch()          # pousse le bouton vers la gauche
        layout_principal.addLayout(layout_bas)

        self.buttonCIDR.clicked.connect(self.appel_CIDRWindow)

        self.buttonIP_Format_Valide.clicked.connect(self.appel_IPWindow)

        self.buttonClasse_IP.clicked.connect(self.appel_ClasseIpWindow)
        self.buttonReseau_SR.clicked.connect(self.appel_Reseau_SousReseau_Window)
        self.buttonMeme_reseau.clicked.connect(self.appel_Communication_MachineWindow)
        self.buttonDecoupe_SR.clicked.connect(self.appel_DecoupeSRWindow)
        self.buttonMasque_IP.clicked.connect(self.appel_MasqueClasseWindow)
        self.buttonHistorique.clicked.connect(self.appel_HistoriqueWindow)
        self.buttonProfil.clicked.connect(self.appel_Menu_User)
        
    def Acces_Admin(self):
        
        #on vérifie si c'est un admin 
        if(self.utilisateur_actuel[2]=="admin" or self.utilisateur_actuel[2]=="superadmin" ):
            
            self.buttonAdmin = QPushButton("Menu Administrateur")
            self.layout_boutons.addWidget(self.buttonAdmin)
            self.buttonAdmin.clicked.connect(self.appel_Menu_Admin)
            
    def appel_Menu_User(self):
        if self.MU is None :
            self.MU = Menu_User_Window.Menu_User_Window()
            self.MU.show()
            self.close()
        else:
            self.MU.close()
            self.MU = None
    def appel_Menu_Admin(self):
        if self.MA is None :
            self.MA = Menu_Admin_Window.Menu_Admin_Window()
            self.MA.show()
            self.close()
        else:
            self.MA.close()
            self.MA = None  
    def appel_HistoriqueWindow(self):
        if self.HAW is None :
            self.HAW = Historique_ActionWindow.Historique_ActionWindow()
            self.HAW.show()
            self.close()
        else:
            self.HAW.close()
            self.HAW = None 
    def appel_DecoupeSRWindow(self):
        if self.DECOUPE_SRW is None:
            self.DECOUPE_SRW = Decoupe_SRWindow.Decoupe_SRWindow()
            self.DECOUPE_SRW.show()
            self.close()
        else:
            self.DECOUPE_SRW.close()
            self.DECOUPE_SRW = None
    def appel_MasqueClasseWindow(self):
        if self.CLASS_IPW is None:
            self.CLASS_IPW = Masque_ClasseWindow.Masque_Classe_Window()
            self.CLASS_IPW.show()
            self.close()
        else:
            self.CLASS_IPW.close()
            self.CLASS_IPW = None
    def appel_Communication_MachineWindow(self):
        if self.COM_MW is None:
            self.COM_MW = Communication_MachineWindow.Communication_MachineWindow()
            self.COM_MW.show()
            self.close()
        else:
            self.COM_MW.close()
            self.COM_MW = None
    def appel_CIDRWindow(self):
        #instanciation des autres fenêtres possibles 
        if self.CIDRW is None :
            self.CIDRW=CIDRWindow.CIDR_Window()
            self.CIDRW.show() 
            self.close()
        else: 
            self.CIDRW.close()
            self.CIDRW = None

    def appel_IPWindow(self):
        if self.VIW is None:
            self.VIW = ValidationInput_Window.ValidationInput_Window()
            self.VIW.show()
            self.close()
        else: 
            self.VIW.close()
            self.VIW = None 

    def appel_ClasseIpWindow(self):
        if self.CLIW is None:
            self.CLIW = ClasseIP_Window.ClasseIP_Window()
            self.CLIW.show()
            self.close()
        else: 
            self.CLIW.close()
            self.CLIW = None
    def appel_Reseau_SousReseau_Window(self):
        if self.RES_SRW is None :
            self.RES_SRW=Reseau_SousReseau_Window.Reseau_SousReseau_Window()
            self.RES_SRW.show()
            self.close()
        else:
            self.RES_SRW.close()
            self.RES_SRW = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = Menu_Window()
    fenetre.show()
    sys.exit(app.exec())
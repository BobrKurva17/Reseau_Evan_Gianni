from features.menu import *
from features.pwd import login, firstLaunch
import mysql.connector
from mysql.connector import errorcode
import sys
# --- import outils pyside --- # 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
# --- import fenêtre --- # 
from features.Premiere_Connection_Windows import Premiere_Connection_Windows
from features.Connexion_Window import Connection_Windows


# Configuration de la base de données
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'Ippy_DB',
    'raise_on_warnings': True
}

#essaye de la connection dans la base de donnée
try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erreur d'accès à la base de données : nom d'utilisateur ou mot de passe incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La base de données n'existe pas.")
    else:
        print(err)
    exit()

#firstLaunch(cnx)
##user = login(cnx)
##home(user,cnx)

# --- MAJ PHASE 2 --- #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # --- ouverture et manipulation CSS --- #
    with open("features/style.qss", "r", encoding="utf-8") as fichier:
        app.setStyleSheet(fichier.read())
    # --- manipulation dans la base de données --- #
    cursor = cnx.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    (count,) = cursor.fetchone()
    cursor.close()

    # accès à la fenêtre Premiere_Connection_Windows si pas de super admin
    if count == 0 : 
        fenetre = Premiere_Connection_Windows()
    else :
        fenetre = Connection_Windows()
    
    fenetre.show()
    sys.exit(app.exec())

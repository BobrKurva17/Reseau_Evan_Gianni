from features.menu import *
from features.pwd import login, firstLaunch
import mysql.connector
from mysql.connector import errorcode

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

print("""
 █████ ███████████  ███████████  █████ █████E
░░███ ░░███░░░░░███░░███░░░░░███░░███ ░░███ 
 ░███  ░███    ░███ ░███    ░███ ░░███ ███  
 ░███  ░██████████  ░██████████   ░░█████   
 ░███  ░███░░░░░░   ░███░░░░░░     ░░███    
 ░███  ░███         ░███            ░███    
 █████ █████        █████           █████   
░░░░░ ░░░░░        ░░░░░           ░░░░░     
──────────────────────────────────────────────────────────────                                     
""")

firstLaunch(cnx)
user = login(cnx)
home(user,cnx)
import tool
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QFrame,QHBoxLayout
from PyQt6.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView,QAbstractItemView
import ValidationExcelWindow

class CIDR_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        #instance de l'autre fenêtre 
        self.VEW = None
        self.setGeometry(250, 100, 1000, 750)
        self.setWindowTitle("IPPY")

        # Frame du tableau
        frame_table = QFrame()
        frame_table.setObjectName("frame_table")

        # Tableau
        var_tab_cidr = tool.printTable()

        tableCIDR = QTableWidget(len(var_tab_cidr), 3)
        tableCIDR.setHorizontalHeaderLabels(
            ["/ClassLess", "Binaire", "Décimal"]
        )

        tableCIDR.setFixedSize(520, 600)
       
       
        #Besoin de in enumerate pour obtenir le numéro de la ligne qui permet
        #de dire où l'écrire dans le tableau 
        #ligne = position où écrire , c = valeur
        for ligne, c in enumerate(var_tab_cidr):
            #affecter l'indice de la valeur de sa ligne 
            item0 = QTableWidgetItem(c[0])
            item1 = QTableWidgetItem(c[1])
            item2 = QTableWidgetItem(c[2])
            # aligner les items 
            item0.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # affecter la valeur à la bonne cellule du tableau (par ligne)
            tableCIDR.setItem(ligne, 0, item0)
            tableCIDR.setItem(ligne, 1, item1)
            tableCIDR.setItem(ligne, 2, item2)

        #modifie la largeur des colonnes 
        tableCIDR.setColumnWidth(0, 70) 
        tableCIDR.setColumnWidth(1, 300) 
        tableCIDR.setColumnWidth(2, 125)
        #Interdit la modification dans le tableau
        tableCIDR.setEditTriggers(
                QAbstractItemView.EditTrigger.NoEditTriggers
            )
        #enlève la colonne qui indique le numéro de la ligne 
        tableCIDR.verticalHeader().setVisible(False)

        tableCIDR.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        # Layout de la frame
        layout_table = QVBoxLayout(frame_table)
        layout_table.addWidget(tableCIDR)


        # Bouton
        bouton_retour = QPushButton("Retour")
        bouton_retour.setObjectName("bouton")
        bouton_toExcel = QPushButton("Vers Excel")
        bouton_toExcel.setObjectName("bouton")

        label_titre=QLabel("Tableau CIDR")
        label_titre.setObjectName("label_titre")
        
        label_titre.setFixedSize(500,50)
        #centre l'élément par rapport au label
        label_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Layout principal
        layout_principal = QVBoxLayout(self)
        #centrer l'élément dans son layaout 
        layout_principal.addWidget(label_titre,alignment=Qt.AlignmentFlag.AlignCenter)
        #layout_principal.move(200,40)
        # Tableau centré horizontalement
        layout_table_principal = QHBoxLayout()
        layout_table_principal.addStretch()
        layout_table_principal.addWidget(frame_table)
        layout_table_principal.addStretch()
        
        #pousse le conteneur vers le bas 
        layout_table_principal.setContentsMargins(0, 50, 0, 0)

        # Bouton en bas à gauche
        layout_bas = QHBoxLayout()
        layout_bas.addWidget(bouton_retour)
        layout_bas.addStretch()
        layout_bas.addWidget(bouton_toExcel,alignment=Qt.AlignmentFlag.AlignRight)
        

        # Assemblage
        layout_principal.addLayout(layout_table_principal)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_bas)

       
        

        bouton_toExcel.clicked.connect(self.appel_ValidationExcel)
    def appel_ValidationExcel(self):
        #instanciation des autres fenêtres possibles 
        if self.VEW is None :
            self.VEW=ValidationExcelWindow.ValidationExcel_Window()
            self.VEW.show() 
        else: 
            self.VEW.close()
            self.VEW = None
            




        
            

        
            
        
                    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("features/style.qss", "r") as fichier:
        app.setStyleSheet(fichier.read())

    fenetre = CIDR_Window()
    fenetre.show()
    sys.exit(app.exec())
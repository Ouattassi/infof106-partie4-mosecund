"""
Nom: Secundar
Prénom : Ismael
Matricule : 504107
Titre : Partie 4 projet d'année
Date : 07/04/2021
"""

import sys, os, pygame, time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QFileDialog,QVBoxLayout, QComboBox, QFormLayout, \
    QMessageBox, QStyleFactory, QDialog
from PyQt5.QtGui import QPalette, QPen, QColorConstants, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QPushButton,QSlider, QCheckBox
from PyQt5.QtCore import QSize, Qt, QRectF
from amazons import *
from players import *
from board import *
from action import *
from pygame import mixer



pygame.init()                                                   # Pour la musique
pygame.mixer.music.load("music.ogg")                            # on choisi la musique à jouer
mixer.music.play(-1)                                            # musique en boucle



class Window(QMainWindow):
    """
    Classe principale avec la fenetre principale
    """
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(850, 700))                    # taille de la fenetre, horizontal,vertical
        self.setWindowTitle("INFO F106 Game of the Amazons")    # Nom de la fenetre
        self.parametres = Parametres(self)                      # Pour utiliser les methodes de la classe parametre
        self.central = QWidget()
        self.qbox = QVBoxLayout()
        self.qbox.addWidget(self.parametres)                    # on ajoute dans la boite les widgets

        self.central.setLayout(self.qbox)                       # on ajoute à la deuxieme boite

        self.setCentralWidget(self.central)

        self.commencer = QFormLayout()
        self.btn_commencer = QPushButton("Commencer", self)     # on ajoute un bouton commencer
        self.btn_commencer.setFont(QFont("Arial",15, QFont.Bold)) # on défini la police de ce bouton

        self.btn_commencer.clicked.connect(self.start)            # on connecte ce bouton à la methode start dans le cas
                                                                  # où ce bouton est lancé
        self.commencer.addRow(self.btn_commencer)                 # on ajoute le bouton commencer au bon endroit
        self.qbox.addLayout(self.commencer)
        self.qbox.addItem(self.commencer)

        self.current_player = None                                # on initialise le joueur courant à None


    def create_board(self,filename):
        """
        Permet de créer le board avec le fichier donné
        :param filename:
        :return:
        """

        self.size = read_file(filename)[0]                         # sur la premiere ligne du fichier
                                                                   # il récupère la taille

        self.pos_black = [Pos2D.from_string(i) for i in read_file(filename)[1]]     # on récupere la positions des
                                                                                    # reines et des fleches
        self.pos_white = [Pos2D.from_string(i) for i in read_file(filename)[2]]
        self.pos_arrows = [Pos2D.from_string(i) for i in read_file(filename)[3]]
        self.gameboard = Chess(self.size,self.pos_black,self.pos_white,self.pos_arrows) # on dessine le board

        self.qbox.addWidget(self.gameboard)                                         # on ajoute le board à la fenetre

    def recommencer(self):
        """
        Permet de changer le bouton commencer en recommencer mais aussi d'ouvrir une fenetre pour savoir si le joueur
        veut réellement recommencer sa partie ou pas
        :return:
        """

        boite = QMessageBox()                       # on défini une boite
        boite.setText("Voulez-vous recommencer?")   # une question est demandée
        boite.setStandardButtons(QMessageBox.No)    # le bouton de base est non ( il ne fait rien)
        boite.addButton(QMessageBox.Yes)            # on ajoute un bouton oui qui va exécuter certaines actions
        reponse = boite.exec_()                     # on lance la boite

        if reponse == QMessageBox.Yes:              # si oui
            self.btn_commencer.setText("Commencer") # on définit le bouton commencer comme étant commencer
            self.btn_commencer.setFont(QFont("Arial",15, QFont.Bold))   # on définit sa police
            self.btn_commencer.disconnect()                             # on déconnecte le bouton commencer
            self.qbox.removeWidget(self.gameboard)                      # on enleve le board
            self.gameboard.setParent(None)
            self.parametres.charger_label.setText("Aucun plateau")      # on mets aussi qu'il n'y plus de plateau chargé
            self.btn_commencer.clicked.connect(self.start)              # on connecte le bouton commencer à la méthode
                                                                        # start
            self.statusBar().setVisible(False)                          # on masque le joueur courant

    def update_board(self,size,pos_black,pos_white,pos_arrow):
        """
        Méthode pour afficher un board et effacer le board courant,
        Cette méthode n'a pas été utilisée ici parce que je change uniquement la position de chaque Qpixmap
        :param size:
        :param pos_black:
        :param pos_white:
        :param pos_arrow:
        :return:
        """

        self.qbox.removeWidget(self.gameboard)                          # enleve le board courant
        self.gameboard.setParent(None)

        self.gameboard = Chess(size,pos_black,pos_white,pos_arrow)      # permet de créer un board avec les nouveaux
                                                                        # parametres
        self.qbox.addWidget(self.gameboard)                             # on ajoute ce board à la fenetre

    def start(self):
        """
        Methode qui est connectée au bouton commencer
        elle permet de changer le bouton commencer à recommencer et elle défini les joueurs qui ont été choisi par
        l'utilisateur
        :return:
        """
        self.board = Board(self.size,read_file(self.parametres.path_data)[1],read_file(self.parametres.path_data)[2],read_file(self.parametres.path_data)[3])
        self.amazone = Amazons(self.board)

        # on appelle la classe board et la classe amazone

        self.btn_commencer.setText("Recommencer")                       # on change le bouton commencer à recommencer
        self.btn_commencer.setFont(QFont("Arial",15, QFont.Bold))
        self.btn_commencer.disconnect()                                 # on déconnecte le bouton commencer à start
        self.btn_commencer.clicked.connect(self.recommencer)            # on le connecte à recommencer
        self.player_1 = mainWin.make_player(self.parametres.btn_joueur_1.currentText(), 1, self.gameboard)
        self.player_2 = mainWin.make_player(self.parametres.btn_joueur_2.currentText(), 0, self.gameboard)

        # permet de créer deux joueurs en fonction des choix de l'utilisateur
        self.players = [self.player_1,self.player_2]
        self.current_player_num = 0                                     # on initialise le joueur courant à 0 comme
        self.change_player()
        self.statusBar().setVisible(True)                               # on affiche le joueur courant

    def change_player(self,game_is_over=False):
        """
        Méthode qui permet de changer de joueur et de jouer tour à tour
        :param game_is_over: Si le jeu est terminé
        :return:
        """
        if game_is_over:
            """
            Si le jeu est terminé une fenetre s'exécute en affichant le gagnant
            """
            Pop = WinnerPopup(self.board.status.winner,self)
            Pop.exec_()
            return


        self.current_player_num = 1 - self.current_player_num
        self.current_player = self.players[self.current_player_num]
        # change de joueur courant et affiche le joueur courant
        self.statusBar().showMessage("Tour du joueur :{}".format("Blanc" if self.current_player == self.player_1 else "Noir"))
        self.statusBar().setFont(QFont("Arial",15, QFont.Bold))



    def make_player(self,text, player_id, board):
        '''
        Permet de creer un joueur en fonction des parametres données
        :param text: soit Humain soit IA
        :param player_id: donne un identifiant au joueur qu'on va créer
        :param board: une instance de la classe board
        :return: une instante de la classe player
        '''
        if text == 'Minimax':
            return AIPlayer(player_id, board)
        elif text == 'Humain':
            return HumanPlayer(player_id, board)

class Parametres(QWidget):
    """

    Classe qui permet de gérer tous les paramètres que l'utilisateur a choisi

    """
    def __init__(self,delegate):
        super().__init__()

        self.delegate = delegate

        param = QFormLayout()

        param.setContentsMargins(0,0,500,0)                         # place sur un certain endroit de la fenetre

        self.btn_joueur_1 = QComboBox(self)                         # liste déroulante avec le choix entre IA ou HUMAIN
        self.btn_joueur_1.setFont(QFont("Arial",15, QFont.Bold))
        self.btn_joueur_1.addItem("Minimax")
        self.btn_joueur_1.addItem("Humain")
        self.btn_joueur_2 = QComboBox(self)
        self.btn_joueur_2.setFont(QFont("Arial",15, QFont.Bold))
        self.btn_joueur_2.addItem("Minimax")
        self.btn_joueur_2.addItem("Humain")

        self.time_label = QLabel('Timer interval:', self)           # Défini un temps interval

        self.save_label = QLabel('Enregistrement',self)             # Demande à l'utilisateur s'il veut que sa partie
                                                                    # soit enregistrée
        self.save_label.setFont(QFont("Arial",15, QFont.Bold))
        self.save = QCheckBox("Oui", self)
        self.save.setFont(QFont("Arial",15, QFont.Bold))

        self.musique_label = QLabel('Musique', self)                # Permet de désactiver la musique en cas de gene
        self.musique_label.setFont(QFont("Arial",15, QFont.Bold))
        self.musique = QCheckBox("Mute", self)
        self.musique.setFont(QFont("Arial",15, QFont.Bold))
        self.musique.stateChanged.connect(self.mute_musique)

        self.bt_charger = QPushButton('Charger',self)               # Permet à l'utilisateur de charger un plateau
        self.bt_charger.setFont(QFont("Arial",15, QFont.Bold))
        self.charger_label = QLabel("Aucun plateau",self)
        self.charger_label.setFont(QFont("Arial",15, QFont.Bold))

        self.bt_charger.clicked.connect(self.btnstate)              # si le bouton chargé est clické la méthode bntstate
                                                                    # est appelée
        self.bt_charger.setCheckable(True)
        self.bt_charger.toggle()
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setTickPosition(QSlider.TicksBelow)
        self.time_slider.sliderReleased.connect(self.release_slider)
        self.time_slider.setTickInterval(10)
        self.time_slider.setValue(1)
        self.time_label.setFont(QFont("Arial",15, QFont.Bold))

        self.joueur_1_label = QLabel("Joueur 1",self)
        self.joueur_1_label.setFont(QFont("Arial",15, QFont.Bold))

        self.joueur_2_label = QLabel("Joueur 2",self)
        self.joueur_2_label.setFont(QFont("Arial", 15, QFont.Bold))

        param.addRow(self.joueur_1_label,self.btn_joueur_1)             # on ajoute dans l'endroit réservée aux
                                                                        # paramatres ce dont l'on a besoin
        param.addRow(self.joueur_2_label,self.btn_joueur_2)
        param.addRow(self.time_label,self.time_slider)
        param.addRow(self.save_label,self.save)
        param.addRow(self.musique_label,self.musique)
        param.addRow(self.bt_charger,self.charger_label)                # on commence par le boutton ensuite le label

        qp = QPalette()
        qp.setColor(QPalette.ButtonText, Qt.black)                      # pour changer la couleur des boutons et de la
                                                                        # fenetre
        qp.setColor(QPalette.Window, QColorConstants.Svg.burlywood)
        qp.setColor(QPalette.Button,QColorConstants.Svg.blanchedalmond)
        qp.setColor(QPalette.Background, QColorConstants.Svg.burlywood)
        app.setPalette(qp)

        self.setLayout(param)

        self.show()

    def mute_musique(self):
        """
        Methode qui permet de mute la musique si l'utilisateur n'en a pas envie. Si l'envie lui prend il peut de nouveau
        écouter la musique en décochant le mute
        :return:
        """
        if self.musique.isChecked():
            pygame.mixer.music.stop()

        else:
            pygame.mixer.music.load("music.ogg")
            pygame.mixer.music.play(-1)

    def release_slider(self):
        '''
        Fonction pour le time interval
        :return: None
        '''
        self.time_interval = self.time_slider.value() * 10

    def btnstate(self):
        """
        Méthode qui est appelée si le bouton chargé est clické
        :return:
        """

        if self.bt_charger.isChecked():
            self.delegate.create_board(self.get_file_name())            # si c'est le cas on appelle la méthode
                                                                        # qui permet d'ouvrir un fichier
    def get_file_name(self):
        """
        Méthode qui permet de choisir un fichier à partir de l'ordinateur
        :return:
        """

        response = QFileDialog.getOpenFileName(self,caption="select a file",directory=os.getcwd(),filter='(*.txt)')
        self.charger_label.setText('Plateau OK!')                       # on signal que le plateau a bien
                                                                        # été selectionné
        self.path = str(response[0])                                    # on sauvegarde le chemin dans une variable

        return self.path                                                # on renvoie le chemin

    @property
    def path_data(self):
        """
        Méthode qui permet de nous donner le chemin du fichier selectionné
        :return: le chemin du fichier
        """
        return self.path

class Scene(QtWidgets.QGraphicsScene):
    """
    Classe qui permet l'affichage du jeu, tout ce qui est graphique et aussi sur le plateau
    """
    def __init__(self,size,pos_black,pos_white,pos_arrows):
        super().__init__()

        self.TILE_SIZE = 100 - (size*6.5)                     # on défini la taille d'une case sur le plateau
        self.click_depart = None                              # on initialise les clicks de départ,arrivée et
                                                              # de la fleche tirée à 0
        self.click_arrivee = None
        self.click_fleche = None
        self.size = size                                      # on stock la taille dans une variable ainsi que les
                                                              # autres données nécéssaires
        self.pos_black = pos_black
        self.pos_white = pos_white
        self.pos_arrow = pos_arrows

        self.cases = []
        self.black = []
        self.white = []
        self.arrow = []

        pen = QPen(QColorConstants.Transparent)                 # on définit le pen
        brush_peru = QBrush(QColorConstants.Svg.peru)           # on défini la couleur de la brosse
        brush_wheat = QBrush(QColorConstants.Svg.wheat)         # on défini la couleur de la seconde brosse

        for row in range(size):
            """
            Permet de créer un board
            """
            self.cases.append([])
            for column in range(size):
                if (row + column) % 2 == 0:                     # permet d'alterner les couleurs
                    brush = brush_peru
                else:
                    brush = brush_wheat
                rect = QRectF(self.TILE_SIZE * column, self.TILE_SIZE * row, self.TILE_SIZE, self.TILE_SIZE)
                self.cases[row].append(self.addRect(rect, pen=pen, brush=brush))

        for black in pos_black:
            """
            Permet de rajouter les reines noires sur le plateau en fonction du plateau selectionné
            """

            row = black.y
            column = black.x

            icon = QPixmap('black.svg')                          # on choisi l'icon qu'on veut rajouter sur le board
            icon = icon.scaled(self.TILE_SIZE, self.TILE_SIZE)   # on défini sa taille

            black_queen = self.addPixmap(icon)
            black_queen.setPos(self.TILE_SIZE * column, self.TILE_SIZE *row)    # on défini sa position sur le board

            self.black.append(((row,column), black_queen))       # on stock les coordonnées de chaque reines ajoutées

        for white in pos_white:

            row = white.y
            column = white.x

            icon = QPixmap('white.svg')
            icon = icon.scaled(self.TILE_SIZE, self.TILE_SIZE)

            white_queen = self.addPixmap(icon)
            white_queen.setPos(self.TILE_SIZE * column, self.TILE_SIZE * row)

            self.white.append(((row,column), white_queen))

        for arrow in pos_arrows:
            row = arrow.y
            column = arrow.x

            icon = QPixmap('arrow.svg')
            icon = icon.scaled(self.TILE_SIZE, self.TILE_SIZE)

            arrow_img = self.addPixmap(icon)
            arrow_img.setPos(self.TILE_SIZE * column, self.TILE_SIZE * row)
            self.arrow.append(((row,column),arrow_img))

    def add_arrow(self,pos):
        """
        Fonction qui permet d'ajouter une fleche sur le board (partie graphique)
        :param pos: la position où la fleche sera tirée
        :return:
        """

        icon = QPixmap('arrow.svg')
        icon = icon.scaled(self.TILE_SIZE, self.TILE_SIZE)

        arrow_img = self.addPixmap(icon)
        arrow_img.setPos(self.TILE_SIZE * pos[1], self.TILE_SIZE * pos[0])
        self.arrow.append(pos)


    def add_queen(self,item_to_remove,item_to_add,pos_new,player):
        """
        Fonction qui permet d'ajouter une reine sur le board (partie graphique)
        :param item_to_remove: element qui va etre enlevé
        :param item_to_add: element qui va etre ajouté
        :param pos_new: l'endroit où la reine va se déplacer
        :param player: 0 pour les blancs, 1 pour les noires
        :return:
        """

        if player == 0:
            self.white.remove(item_to_remove)
            self.white.append((pos_new, item_to_add[1]))
            item_to_add[1].setPos(pos_new[1] * self.TILE_SIZE, pos_new[0] * self.TILE_SIZE)

        elif player == 1:
            self.black.remove(item_to_remove)
            self.black.append((pos_new, item_to_add[1]))
            item_to_add[1].setPos(pos_new[1] * self.TILE_SIZE, pos_new[0] * self.TILE_SIZE)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        Fonction qui permet de récuperer les clicks
        :param event:
        :return:
        """
        self.click_total = []

        for i, row_cases in enumerate(self.cases):
            for j, case in enumerate(row_cases):
                if case.rect().contains(event.scenePos()):

                    if self.click_depart == None:               # permet de récuperer le click de départ
                        self.click_depart = (i,j)

                        self.click_depart_fenetre = (i,j)

                    elif self.click_arrivee == None :
                        self.click_arrivee = (i,j)              # permet de récuperer le click d'arrivée

                        self.click_arrivee_fenetre = (i,j)

                    elif self.click_fleche == None and self.click_arrivee != self.click_depart:
                        # permet de récuperer le click de la fleche
                        self.click_fleche = (i,j)
                        self.click_fleche_fenetre = (i,j)

                    if self.click_arrivee == self.click_depart :
                        # si les déplacement ne sont pas correctes on initialise tous les click à None

                        self.click_arrivee = None
                        self.click_depart = None
                        self.click_fleche = None

                    if self.click_depart != None and self.click_arrivee != None and self.click_fleche != None:
                        # dans le cas où on a bien 3 click

                        if mainWin.current_player == mainWin.player_1:
                            # si c'est le joueur blanc en cours
                            for white_queen in self.white:

                                if self.click_depart in white_queen:
                                    # si le click est bien une reine blanche
                                    click_depart_pos2d = Pos2D(self.click_depart[0], self.click_depart[1])
                                    click_arivee_pos2d = Pos2D(self.click_arrivee[0], self.click_arrivee[1])
                                    click_fleche_pos2d = Pos2D(self.click_fleche[0], self.click_fleche[1])
                                    # on converti les click en pos2d

                                    if mainWin.board.is_accessible(click_depart_pos2d,click_arivee_pos2d) and \
                                            mainWin.board.is_accessible(click_arivee_pos2d,click_fleche_pos2d,ignore=click_arivee_pos2d):
                                        # on vérifie s'il est accessible

                                        self.add_queen(white_queen,white_queen,self.click_arrivee,0)
                                        # on ajoute la reine sur le board
                                        self.add_arrow(self.click_fleche)
                                        # on ajoute la fleche sur le board

                                        mainWin.board._move(click_depart_pos2d,click_arivee_pos2d)
                                        mainWin.board._shoot_arrow(click_fleche_pos2d)


                        elif mainWin.current_player == mainWin.player_2:
                            # on fait de même si c'est le cas où le joueur noir joue

                            for black_queen in self.black:

                                if self.click_depart in black_queen:
                                    click_depart_pos2d = Pos2D(self.click_depart[0], self.click_depart[1])
                                    click_arivee_pos2d = Pos2D(self.click_arrivee[0], self.click_arrivee[1])
                                    click_fleche_pos2d = Pos2D(self.click_fleche[0], self.click_fleche[1])

                                    if mainWin.board.is_accessible(click_depart_pos2d, click_arivee_pos2d) and \
                                            mainWin.board.is_accessible(click_arivee_pos2d, click_fleche_pos2d,
                                                                        ignore=click_arivee_pos2d):

                                        self.add_queen(black_queen,black_queen,self.click_arrivee,1)
                                        self.add_arrow(self.click_fleche)

                                        mainWin.board._move(click_depart_pos2d, click_arivee_pos2d)
                                        mainWin.board._shoot_arrow(click_fleche_pos2d)

                        if mainWin.amazone.is_over():                       # si le jeu est terminé
                            mainWin.change_player(game_is_over=True)        # on fait appelle à change_player
                                                                            # qui va ouvrir un pop up
                                                                            # dans lequel le gagnant est mentionné

                        mainWin.change_player()                             # on change de joueur à chaque fois
                        mainWin.statusBar().showMessage(
                            "Joueur :{}".format("Blanc" if mainWin.current_player == mainWin.player_1 else "Noir"))
                                                                            # on indique le joueur courant

                        self.click_depart = None                            # sinon on remets tous les clicks à None
                        self.click_arrivee = None
                        self.click_fleche = None


    def GetClicked(self, tuple_click):
        """
        Convertis les coordonnées d'un click en un coup
        par exemple (0,0) --> a1
        """
        x = tuple_click[0]
        y = tuple_click[1]
        x = x+1
        y = chr(y+97)
        res = str(y) + str(x)
        return res


class Plateau(QtWidgets.QGraphicsView):
    def __init__(self,size,pos_black,pos_white,pos_arrows):
        super().__init__()
        scene = Scene(size,pos_black,pos_white,pos_arrows)
        self.setScene(scene)
        self.setAlignment(QtCore.Qt.AlignCenter)
        # désactive la bordure qui est par défaut
        self.setFrameShape(0)
        # le fait devenir transparant
        self.setStyleSheet('QGraphicsView {background: transparent;}')

class Chess(QtWidgets.QWidget):
    """
    Permet de créer le plateau
    """
    def __init__(self,size,pos_black,pos_white,pos_arrows):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        self.plateau = Plateau(size,pos_black,pos_white,pos_arrows)
        layout.addWidget(self.plateau, 1, 1)

        leftLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(leftLayout, 1, 0)
        rightLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(rightLayout, 1, 2)


class WinnerPopup(QDialog):
    '''
    Popup qui affiche le gagnant du jeu
    '''
    def __init__(self, winners, parent):
        '''
        Constructeur de la classe gagnant
        :param winners: le gagnant
        :param parent:
        '''
        super().__init__(parent)

        if winners == PLAYER_1:
            text = 'White queens won!'

        else:
            text = 'Black queens won!'

        self.setFixedSize(QSize(500, 100))
        self.label = QLabel(text, self)
        self.label.setFont(QFont("Arial", 20, QFont.Bold))
        label_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        label_height = self.label.fontMetrics().boundingRect(self.label.text()).height()
        self.label.move((self.width()-label_width)/2, (self.height()-label_height)/2)



class MinimaxPlayer(AIPlayer):
    """
    Amélioration de l'IA
    """
    def __init__(self, board, player_id):
        super().__init__(board, player_id)

    def minimax(self, depth=2, maximizing=True, alpha = -INF, beta = INF):
        """
        Une durée de 2 secondes maximal a été rajoutée dans le cas où la durée es
        """

        if depth == 0:                                  # si la prochondeur est de 0
            return (None,self.objective_function())     # on fait appel à l'autre fonction

        if maximizing:                                  # si on veut maximiser
            best_score = -INF
            player = self.player_id

        else:
            best_score = +INF
            player = self.other_player_id

        best_actions = []                                # on stocks les meilleures actions
        assert self.board.has_moves(player)              # si le joueur a encore des déplacements

        for action in self.board.possible_actions(player):      # on va parcourir tous ses actions possibles
            self.board.act(action)

            winner = self.board.status.winner                   # on regarde le status du gagnant
            if winner is not None:                              # s'il n'y a pas de gagnant
                score = INF+depth
                if winner == self.other_player_id:
                    score *= -1
            else:
                score = self.minimax(depth-1, not maximizing)[1]
            self.board.undo()

            if (score > best_score and maximizing) or (score < best_score and not maximizing):
                best_score = score
                best_actions = [action]
            self.fin = time.time()                              # on termine le calcul du temps
            self.temps_final = self.fin - self.debut
            if self.temps_final < 1.999999999999:               # on renvoie un coup tant qu'il est inférieur à 1.99...
                return random.choice(best_actions), best_score  # on prend une des meilleures actions au hasard
            elif score == best_score:
                best_actions.append(action)

            if maximizing:                                      # on utilise alpha et beta
                if alpha <= score:
                    alpha = score
                if beta <= alpha:
                    break

            elif not maximizing:
                if beta >= score:
                    beta = score
                if beta <= alpha:
                    break

        return random.choice(best_actions), best_score

    def objective_function(self):
        count = 0
        for action in self.board.possible_actions(self.player_id):

            count += 1

        return count


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    app.setStyle(QStyleFactory.create('Fusion'))

    sys.exit(app.exec_())
# -*- coding: utf-8 -*-
"""

@author: melkarmo
"""

from tkinter import *
from tkinter.messagebox import *
from random import randint



# Ceci est la classe des boutons associés aux lettres de l'alphabet
# elle hérite de la classe Button
class MonBouton(Button):
    
    """ Attributs """
    
    def __init__(self, parent, letter, window):
        Button.__init__(self, parent, text=letter, command=self.cliquer)
        # parent désigne la zone (fenêtre ou frame ...) où va être affiché le bouton
        
        # lorsqu'on clique sur le bouton, c'est la méthode cliquer qui est appelée
        self.__lettre = letter # lettre associée au bouton
        self.__fenetre = window # fenêtre dans laquelle est affichée le bouton
    
    """ Méthodes """
    
    def cliquer(self):
        self.config(state=DISABLED) # on désactive la touche
        
        # on traite le clic du joueur sur le bouton associée à la lettre
        # la méthode traitement est dans la classe FenPrincipale
        self.__fenetre.traitement(self.__lettre)



# Ceci est la classe de la zone d'affichage du pendu
# elle hérite de la classe Canvas
class ZoneAffichage(Canvas):
    
    """ Attributs """
    
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, parent, width = w, height = h, bg = c)
        # width = largeur, height = hauteur, bg = couleur de fond



# Ceci est la classe de la fenêtre principale de l'application
# elle hérite de la classe Tk
class FenPrincipale(Tk):
    
    """ Attributs """
    
    def __init__(self):
        
        Tk.__init__(self)
        self.title('Jeu du Pendu') # titre de la fenêtre
        
        # une instance de la classe Frame correspond à une zone (ou cadre) de la fenêtre
        # ici, le frameMenu est la zone où on met les boutons pour amorcer une nouvelle partie et pour quitter la partie
        frameMenu = Frame(self)
        frameMenu.pack(side=TOP, padx=5, pady=5)
        self.__boutonNew = Button(frameMenu, text='Nouvelle partie', width=15, command=self.nouvellePartie).pack(side=LEFT, padx = 10, pady = 10) # bouton pour amorcer une nouvelle partie
        self.__boutonEnd = Button(frameMenu, text='Quitter', width=15, command=self.destroy).pack(side=RIGHT, padx = 10, pady = 10) # bouton pour quitter le jeu
     
        # on définit la zone d'affichage du Pendu
        self.__zoneAffichage = ZoneAffichage(self,400,400,'light grey')
        self.__zoneAffichage.pack(padx=5, pady=5)
        
        # ici, le frameLetters est la zone où on met le clavier virtuel
        frameLetters = Frame(self)
        frameLetters.pack(side=BOTTOM, padx=10, pady=15)
        
        # on crée la liste des caractères des 26 lettres de l'alphabet
        lettres = []
        for i in range(26):
            lettres.append(chr(ord('A')+i))
            
        # on crée la liste des boutons, instances de la classe MonBouton,
        # de notre clavier virtuel dans le frameLetters grâce à la liste des lettres de l'alphabet
        self.__boutons = [MonBouton(frameLetters,l,self) for l in lettres]
        
        # ce qui suit permet d'éviter d'avoir les boutons des lettres sur une même ligne
        for i in range(26):
            bouton = self.__boutons[i]
            bouton.config(width=4) # on augmente la largeur des bouton pour améliorer la lisibilité
            bouton.grid(row=1 + i//10,column=i%10 +1)
            
        self.__nbManques = 0 # nombre de coups manqués par le joueur
        self.__motMystere = '' # mot à deviner
        self.__motAffiche = '' # mot affiché au joueur
        self.__lmot = Label(self) # objet permettant d'afficher motAffiche au joueur
        
        self.nouvellePartie() # on lance notre première partie


    """ Méthodes """
    
    # Cette méthode est appelée au démarrage de l'application, mais également lorsque
    # le joueur désire refaire une partie
    def nouvellePartie(self):
        
        self.__zoneAffichage.delete("all") # on nettoie la zone d'affichage d'éventuels éléments du pendu d'une partie précédente
        
        self.__nbManques = 0 # on réinitialise le nombre de coups manqués
        self.__motMystere = self.nouveauMot() # on génère un mot à deviner
        self.__motAffiche = self.nouveauMotCache(self.__motMystere) # on initialise le mot à afficher au joueur, caché bien sûr

        # on affiche motAffiche au joueur dans la fenêtre
        self.__lmot.pack(padx = 5, pady = 5)
        self.__lmot.config(text='Mot : '+self.__motAffiche) 

        # on réactive tout les boutons du clavier virtuel
        for bouton in self.__boutons:
            bouton.config(state=NORMAL)
            
    
    # Cette méthode génère un mot à deviner parmi des mots dans un fichier 'mots.txt'
    def nouveauMot(self):
        
        # on ouvre le fichier mots, et on extrait les mots du fichiers dans une liste 'mots', puis on ferme le fichier
        fichier = open('mots.txt','r')
        contenu_fichier = fichier.read()
        mots = contenu_fichier.split('\n')
        fichier.close()
        
        # on renvoie un mot aléatoire dans la liste mots
        n = randint(0,len(mots)-1) 
        return mots[n]
        
        
    # Cette méthode renvoie, pour un mot donné en argument, la chaine de caractère de longueur identique,
    # mais composée uniquement d' étoiles, ce qui permet de cacher le mot à afficher au joueur
    def nouveauMotCache(self, mot):
        res = ''
        for i in range (len(mot)):
            res = res + '*'
        return res
            
        
    # Cette méthode effectue le traitement du choix du joueur 
    # elle prend en argument une lettre, correspondant au choix du joueur
    def traitement(self, lettre):
        
        rate = 1 
        # rate est la variable qui vaut 1 si le coup du joueur est manqué
        # et 0 si le joueur réussit son coup, on l'initialise ici à 1
        
        # à l'aide d'une boucle for, on cherche les occurences de la lettre dans le mot à deviner
        for j in range(len(self.__motMystere)):
            if self.__motMystere[j] == lettre:
                # si la lettre est dans le mot, on l'affiche dans le mot à afficher
                self.__motAffiche = self.__motAffiche[:j] + lettre + self.__motAffiche[j+1:]
                # la variable rate vaut alors 0
                rate = 0
        
        # on met à jour le nombre de coups manqués, ce qui revient à y ajouté la valeur de la variable rate        
        self.__nbManques += rate
        
        # on met à jour le texte à afficher au joueur
        self.__lmot.config(text='Mot : '+self.__motAffiche)

        # si le joueur a raté son coup, on affiche un élément du pendu        
        if rate == 1 :
            self.affichePendu()
            
        # on vérifie enfin si la partie est bien finie    
        self.finPartie()
        
        
    # Cette méthode, lorsqu'elle est appelée, affiche l'élement du pendu correspondant 
    # au nombre de coups manqués au moment de l'appel
    def affichePendu(self):
        
        n = self.__nbManques
        
        # dimensions du pendu
        rayon_tete = 20
        longueur_torse = 8
        longueur_bras = 40
        longueur_jambe = 50
        
        # chaque nombre de coups manqués correspond à un élément et un seul du pendu, 
        # d'où l'utilisation des conditions
        # les éléments du pendu sont affichés sous forme géométrique, plus précisement 
        # sous forme de rectangles, et d'un disque pour la tête du pendu
        if n == 1:
            self.__zoneAffichage.create_rectangle(50, 350, 150, 354, outline='black', fill='black')
        elif n == 2:
            self.__zoneAffichage.create_rectangle(98, 75, 102, 354, outline='black', fill='black')
        elif n == 3:
            self.__zoneAffichage.create_rectangle(98, 75, 250, 79, outline='black', fill='black')
        elif n == 4:
            self.__zoneAffichage.create_rectangle(246, 75, 250, 150, outline='black', fill='black')
        elif n == 5:
            self.__zoneAffichage.create_oval(248-rayon_tete,140-rayon_tete,248+rayon_tete,140+rayon_tete, outline='black', fill='black')
        elif n == 6:
            self.__zoneAffichage.create_rectangle(248-longueur_torse, 140, 248+longueur_torse, 225, outline='black', fill='black')
        elif n == 7:
            self.__zoneAffichage.create_rectangle(248-longueur_bras, 180, 248, 186, outline='black', fill='black')
        elif n == 8:
            self.__zoneAffichage.create_rectangle(248, 180, 248+longueur_bras, 186, outline='black', fill='black')
        elif n == 9:
            self.__zoneAffichage.create_rectangle(240, 225, 246, 225+longueur_jambe, outline='black', fill='black')
        elif n == 10:
            self.__zoneAffichage.create_rectangle(250, 225, 256, 225+longueur_jambe, outline='black', fill='black')
    
    
    # Cette méthode met fin à la partie si la partie doit être finie, càd on vérifiant les conditions (voir corps de la méthode)
    def finPartie(self):
        
        # on finit la partie si le joueur a manqué 10 coups
        if self.__nbManques == 10:
            
            # on dit au joueur qu'il a gagné
            self.__lmot.config(text='Vous avez perdu, le mot était : '+self.__motMystere)
            
            # on désactive les boutons du clavier virtuel
            for bouton in self.__boutons:
                bouton.config(state=DISABLED)
                
        # on finit la partie si le mot a été deviné par le joueur
        elif self.__motAffiche == self.__motMystere:
            
            # on dit au joueur qu'il a gagné
            self.__lmot.config(text= self.__motMystere + ' - Bravo, vous avez gagné')
            
            # on désactive les boutons du clavier virtuel
            for bouton in self.__boutons:
                bouton.config(state=DISABLED)
                
        
        
fen = FenPrincipale()
fen.mainloop()

        
        
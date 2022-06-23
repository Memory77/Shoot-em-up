#import de la librairie pygame
import pygame

import random

#pour avoir les constantes de Pygame 
from pygame import *

#taille de notre écran
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600


#classe définissant le vaisseau du héro
#hérite de Sprite
class Vaisseau(pygame.sprite.Sprite):
    #construct
    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("img/vaisseau.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    #Màj quand le joueur appuie sur une touche
    def update(self, pressed_keys):
        #déplacement vers le haut
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        #déplacement vers le bas
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        #vers la gauche
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        #vers la droite
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Appui sur espace => ajout d'un missile
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)
                tous_sprites.add(missile)
                le_missile.add(missile)
        #pour ne pas sortir de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN

# Classe qui va définir un missile de notre vaisseau 
# Va hériter de Sprite
class Missile(pygame.sprite.Sprite):
    # Construct, avec en argumant le point d'apparition du missile
    def __init__(self, center_missile):
        global player
        super(Missile, self).__init__()
        self.surf = pygame.image.load("img/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=center_missile
        )
        
    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()

# Classe définissant un vaisseau ennemi
# Hérite de Sprite
class Enemmi(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemmi, self).__init__()
        self.surf = pygame.image.load("img/ennemi.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # Les ennemis apparaissent sur la droite de l'écran, a une hauteur random
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 50,
                random.randint(0, HAUTEUR_ECRAN),
            )
        )
        # chaque ennemi à une vitesse random, entre 5 et 20
        self.speed = random.randint(5, 20)

    # Mise à jour du vaisseau ennemi
    def update(self):
        #Déplacement du vaisseau vers la gauche
        self.rect.move_ip(-self.speed, 0)
        # Si le vaisseau sort de l'écran, on l'efface
        if self.rect.right < 0:
            self.kill()

# Classe définissant une explosion
# Hérite de Sprite
class Explosion(pygame.sprite.Sprite):
    # Constructeur, avec le centre initial
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        # On affiche l'explosion pendant 10 cycles
        self._compteur = 10
        self.surf = pygame.image.load("img/explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=center_vaisseau
        )
        
    #màj de l'explosion
    def update(self):
        # On décrémente le compteur
        self._compteur = self._compteur - 1
        # Une fois à 0, on efface l'explosion
        if self._compteur == 0:
            self.kill()

# Classe définissant une étoile
class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("img/etoile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # position de départ aléatoire, à droite de l'écran
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 20,
                random.randint(0, HAUTEUR_ECRAN),
            )
        )

    # màj de l'étoile
    def update(self):
        # chaque étoile se déplace vers la gauche
        self.rect.move_ip(-5, 0)
        # Quand elle sort de l'écran, on l'efface
        if self.rect.right < 0:
            self.kill()

# Classe affichant le score courant
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self._scoreCourant = 0
        self._setText()
    
    def _setText(self):
        self.surf = police_score.render(
            'Score : ' + str(self._scoreCourant), False, (255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN / 2, 15)
        )
    
    def update(self):
        self._setText()
    
    # Pour incrémenter le score quand on touche l'ennemi
    def incremente(self, valeur):
        self._scoreCourant = self._scoreCourant + valeur

pygame.font.init()

police_score = pygame.font.SysFont('Comic Sans MS', 30)

# réglage de l'horloge
clock = pygame.time.Clock()

#initialisation de la librairie
pygame.init()
pygame.display.set_caption("The Shoot'em up 1.0")

AJOUTE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(AJOUTE_ENEMY, 500)
AJOUTE_ETOILE = pygame.USEREVENT + 2
pygame.time.set_timer(AJOUTE_ETOILE, 100)

#création de la surface principale
ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])

# groupe de Sprites
# tous les sprites (pour faire le blit)
tous_sprites = pygame.sprite.Group()
# le missile
le_missile = pygame.sprite.Group()
# les ennemis
les_ennemies = pygame.sprite.Group()
# les explosions
les_explosions = pygame.sprite.Group()
# les étoiles
les_etoiles = pygame.sprite.Group()

# création des éléments
vaisseau = Vaisseau()
tous_sprites.add(vaisseau)
score = Score()
tous_sprites.add(score)

# game loop
continuer = True
while continuer:

    #si le joueur veut fermer la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == AJOUTE_ENEMY:
            # creation d'un nouvel ennemi et ajout dans le groupe de sprites
            nouvel_enemmi = Enemmi()
            # ajout aux groupes
            les_ennemies.add(nouvel_enemmi)
            tous_sprites.add(nouvel_enemmi)
        elif event.type == AJOUTE_ETOILE:
            # Create the new start and add it to sprite groups
            nouvel_etoile = Etoile()
            les_etoiles.add(nouvel_etoile)
            tous_sprites.add(nouvel_etoile)

    # On remplit notre écran en noir (rvb)
    ecran.fill((0,0,0))

    # détection des collisions héro / ennemi
    if pygame.sprite.spritecollideany(vaisseau, les_ennemies):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        continuer = False

    # détection des collisions missile/ennemi
    for missile in le_missile: 
        liste_ennemis_touches = pygame.sprite.spritecollide(
            missile, les_ennemies, True)
        if len(liste_ennemis_touches) > 0:
            missile.kill()
            score.incremente(len(liste_ennemis_touches))
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)

    #pile des touches appuyées
    touche_appuyee = pygame.key.get_pressed()

    #màj des éléments
    vaisseau.update(touche_appuyee)
    le_missile.update()
    les_ennemies.update()
    les_explosions.update()
    les_etoiles.update()
    score.update()

    #mise à jour du vaisseau
    #ecran.blit(vaisseau.surf, vaisseau.rect)
    #recopie des objets sur la surface ecran
    for mon_sprite in tous_sprites: 
        ecran.blit(mon_sprite.surf, mon_sprite.rect)

    pygame.display.flip()

    # indique à pyg de e pas faire plus de 30 fois par seconde la gameloop
    clock.tick(30)

pygame.time.delay(3000)

pygame.quit()
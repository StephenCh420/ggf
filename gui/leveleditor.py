import pygame
import sys
from game.background import *
from gui.button import Button


class LevelEditor:

    def __init__(self, level, game_handler, mode, level_selector):

        self.level = level
        self.game_handler = game_handler
        self.level_selector = level_selector
        self.mode = mode
        self.bg = None
        self.p_type = 1
        self.p1_button = None
        self.p2_button = None
        self.p3_button = None
        self.banderole = pygame.image.load("images/banderole plateforme.png")
        self.decalage = 0
        self.left_click = pygame.image.load("images/left_click.png")
        self.right_click = pygame.image.load("images/right_click.png")
        self.delete = pygame.image.load("images/delete.png").convert_alpha()
        self.exit_button = None

    """
    :desc - Processing 
    """
    def process(self):
        print("Editing levels")
        count = 0  # Pour le décalage du background
        pro = True  # Condition d'arrêt de la boucle
        self.game_handler.register_platform_by_file(
            self.level.location)  # Chargement des plateformes à partir du fichier du niveau
        self.render_background()  # Affiche le background
        click = False  # Si le joueur clique sur sa souris

        while pro:
            self.bg.draw(self.mode)

            if self.p_type == 1:
                self.p1_button = Button("Type 1", 160, 36, (50, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 1 yellow.png", (160, 36))
                self.p2_button = Button("Type 2", 250, 36, (230, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 2 white.png", (250, 36))
                self.p3_button = Button("Type 3", 500, 36, (500, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 3 white.png", (500, 36))
            elif self.p_type == 2:
                self.p1_button = Button("Type 1", 160, 36, (50, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 1 white.png", (160, 36))
                self.p2_button = Button("Type 2", 250, 36, (230, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 2 yellow.png", (250, 36))
                self.p3_button = Button("Type 3", 500, 36, (500, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 3 white.png", (500, 36))
            elif self.p_type == 3:
                self.p1_button = Button("Type 1", 160, 36, (50, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 1 white.png", (160, 36))
                self.p2_button = Button("Type 2", 250, 36, (230, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 2 white.png", (250, 36))
                self.p3_button = Button("Type 3", 500, 36, (500, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 3 yellow.png", (500, 36))

            self.exit_button = Button("Quitter", 10, 10, (10, 10),
                                      self.game_handler.ggf).custom_image("images/getback.png", (75, 75))

            place = True  # Si on peut placer une plateforme
            highlight = "None"
            plat_del = None  # La plateforme à supprimer
            i = 0  # Compteur
            index = 0  # Index de la plateforme à supprimer

            if self.p1_button.collides():
                place = False
                self.p1_button = Button("Type 1", 160, 36, (50, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 1 white.png", (160, 36))
                if click: self.p_type = 1
            elif self.p2_button.collides():
                place = False
                self.p2_button = Button("Type 2", 250, 36, (230, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 2 white.png", (250, 36))
                if click: self.p_type = 2
            elif self.p3_button.collides():
                place = False
                self.p3_button = Button("Type 3", 500, 36, (500, 655 + self.decalage),
                                        self.game_handler.ggf).custom_image("images/plateforme 3 white.png", (500, 36))
                if click:
                    self.p_type = 3
            elif self.exit_button.collides():
                highlight = self.exit_button.title
                place = False
                if click: pro = False

            click = False

            for plat in self.game_handler.platforms:  # Intéractions avec les plateformes
                if plat.is_mobile():
                    plat.move()
                if plat.collides():
                    plat_del = plat
                    index = i
                    print(index)
                i += 1
                plat.draw(self.mode)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        click = True

                        if place and mouse_pos[1] < 630:
                            level_hs = open("high scores/" + self.level.name + ".txt", "w+")
                            for i in range(0, 3):
                                level_hs.write("999.99\n")
                            level_hs.close()
                            self.game_handler.register_platform(self.level.name + ".txt", mouse_pos, False,
                                                                self.bg.decalage,
                                                                self.p_type)
                    elif event.button == 3:
                        click = True
                        if place:
                            self.game_handler.register_platform(self.level.name + ".txt", mouse_pos, True,
                                                                self.bg.decalage,
                                                                self.p_type)
                if event.type == pygame.QUIT:
                    pro = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:

                        if plat_del is not None:
                            self.game_handler.rewrite_file(self.level, plat_del)
                            self.game_handler.platforms.pop(index)

                    if event.key == pygame.K_UP:
                        count += 1
                        self.bg.defil("up")
                        if self.bg.count < self.bg.n_screen:
                            for plat in self.game_handler.platforms:
                                plat.move_y(self.bg.delta_y)
                    if event.key == pygame.K_DOWN and count > 0:
                        count -= 1
                        self.bg.defil("down")
                        if self.bg.count < self.bg.n_screen:
                            for plat in self.game_handler.platforms:
                                plat.move_y(-self.bg.delta_y)

            self.mode.blit(self.banderole, (0, 600 + self.decalage))
            self.mode.blit(self.left_click, (1030, 645 + self.decalage))
            self.mode.blit(self.right_click, (1100, 645 + self.decalage))
            self.mode.blit(self.delete, (1170, 670 + self.decalage))
            self.p1_button.render("")
            self.p2_button.render("")
            self.p3_button.render("")

            if pygame.mouse.get_pos()[1] >= 620 + self.decalage / 2:
                if self.decalage > 0:
                    self.decalage -= 20

            else:
                if self.decalage < 100:
                    self.decalage += 10
            self.exit_button.render(highlight)
            pygame.display.update()

        self.level_selector.selected_level = None
        self.game_handler.level = None
        self.game_handler.platforms = []

    """
    :desc - Créé un background qui bouge 
    """
    def render_background(self):
        self.bg = Background()
        self.bg.surface = self.mode

    
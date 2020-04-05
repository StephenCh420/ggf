import pygame
import sys
from game.Game import Game
from entities.player import Player
from entities.platform import Platform
from utils import Utils


class GGf:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gotta go fast")
        self.mode = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.SysFont(None, 100)
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("images/back.png").convert_alpha()
        self.play = Game(self)
        self.menu()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def menu(self):
        # pygame.mixer.music.load('pioneer-to-the-falls.mp3')
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)

        while True:
            self.mode.blit(self.bg, [0, 0])
            self.draw_text("Gotta go fast", self.font, (109, 7, 26), self.mode, 430, 10)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            play = pygame.Rect(430, 300, 450, 70)
            rules = pygame.Rect(430, 400, 450, 70)
            highlight = "None"
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if play.collidepoint((mouse_x, mouse_y)):
                highlight = "play"
                if click:
                    self.game()

            if rules.collidepoint((mouse_x, mouse_y)):
                highlight = "rules"
                if click:
                    self.rules()

            if highlight == "play":
                pygame.draw.rect(self.mode, (109, 7, 26), play)
                pygame.draw.rect(self.mode, (255, 0, 0), rules)

            elif highlight == "rules":
                pygame.draw.rect(self.mode, (255, 0, 0), play)
                pygame.draw.rect(self.mode, (109, 7, 26), rules)

            elif highlight == "None":
                pygame.draw.rect(self.mode, (255, 0, 0), play)
                pygame.draw.rect(self.mode, (255, 0, 0), rules)

            self.draw_text("Jouer", self.font, (200, 7, 26), self.mode, 550, 300)
            self.draw_text("Options", self.font, (200, 7, 26), self.mode, 530, 400)

            pygame.display.update()
            self.clock.tick(25)

    def rules(self):

        running = True

        while running:
            self.mode.blit(self.bg, [0, 0])
            self.draw_text("Options", self.font, (255, 255, 255), self.mode, 500, 10)

            quit = pygame.Rect(430, 300, 450, 70)
            click = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            highlight = "None"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if quit.collidepoint((mouse_x, mouse_y)):
                highlight = "quit"
                if click:
                    running = False

            if highlight == "quit":
                pygame.draw.rect(self.mode, (109, 7, 26), quit)
            elif highlight == "None":
                pygame.draw.rect(self.mode, (255, 0, 0), quit)

            pygame.display.update()
            self.clock.tick(25)

    def game(self):

        self.play.register_platform(Platform((500, 100), True, "images/plateforme 1 V2.png"))
        self.play.register_platform(Platform((600, 300), False, "images/plateforme 1 V2.png"))
        self.play.register_player(Player([100, 300]))

        while True:
            self.mode.blit(self.bg, [0, 0])
            self.draw_text('Level 1', self.font, (255, 255, 255), self.mode, 20, 20)

            self.play.process()

            for event in pygame.event.get():
                if event.type == pygame.K_KP_ENTER:
                    break
                if event.type == pygame.QUIT:
                    sys.exit(0)

            pygame.display.update()
            self.clock.tick(25)

ggf = GGf()

import pygame
import random
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-jeu Pygame")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Joueur
player = pygame.Rect(WIDTH//2, HEIGHT-40, 40, 40)
player_speed = 5

# Objets
bonus_list = []
obstacle_list = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)

# Score et vies
score = 0
lives = 3



pygame.quit()
sys.exit()

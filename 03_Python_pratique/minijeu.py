import pygame
import random
import sys
import time

# Initialisation
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Charger image joueur
try:
    player_img = pygame.image.load("assets/travel.png")
    player_img = pygame.transform.scale(player_img, (50, 80))
except:
    player_img = None

player = pygame.Rect(WIDTH//2 - 25, HEIGHT-100, 50, 80)
player_speed = 5

# Charger images des voitures obstacles
obstacle_images = []
for i in range(5):
    if i == 0:
        path = "assets/car.png"
    else:
        path = f"assets/car{i}.png"
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (50, 80))
    obstacle_images.append(img)

# Charger image essence
try:
    fuel_img = pygame.image.load("assets/gasoline.png")
    fuel_img = pygame.transform.scale(fuel_img, (40, 40))
except:
    fuel_img = None

# Obstacles et bonus
obstacle_list = []
fuel_list = []

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)  # toutes les 1.2 sec

# Score, vies et chrono
score = 0
lives = 3
start_time = time.time()

running = True
while running:
    screen.fill((40, 40, 40))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            # Spawn obstacle voiture
            img = random.choice(obstacle_images)
            w, h = img.get_size()
            obstacle_list.append([pygame.Rect(random.randint(0, WIDTH-w), -h, w, h), img])

            # Spawn bonus essence (1 chance sur 3)
            if random.randint(1, 3) == 1:
                fuel_list.append(pygame.Rect(random.randint(0, WIDTH-30), -30, 30, 30))

    # Contrôles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed

    # Déplacement obstacles
    for o, img in obstacle_list[:]:
        o.y += 5
        if o.colliderect(player):
            lives -= 1
            obstacle_list.remove([o, img])
        elif o.top > HEIGHT:
            obstacle_list.remove([o, img])

    # Déplacement essence
    for f in fuel_list[:]:
        f.y += 4
        if f.colliderect(player):
            score += 10
            fuel_list.remove(f)
        elif f.top > HEIGHT:
            fuel_list.remove(f)

    # Affichage joueur
    if player_img:
        screen.blit(player_img, player)
    else:
        pygame.draw.rect(screen, (0, 100, 255), player)

    # Affichage obstacles
    for o, img in obstacle_list:
        screen.blit(img, o)

    # Affichage essence
    for f in fuel_list:
        if fuel_img:
            screen.blit(fuel_img, f)
        else:
            pygame.draw.rect(screen, (0, 255, 0), f)

    # Texte score, vies, temps
    elapsed_time = int(time.time() - start_time)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Vies: {lives}", True, (255, 255, 255))
    time_text = font.render(f"Temps: {elapsed_time}s", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(time_text, (10, 70))

    # Fin du jeu
    if lives <= 0:
        game_over_text = font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

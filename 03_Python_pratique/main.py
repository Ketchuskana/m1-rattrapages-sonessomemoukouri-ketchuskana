import pygame, sys, random, time
from player import Player
from background import draw_background
from obstacles import Obstacle
from fuel import Fuel

# --- Initialisation ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Joueur
player = Player(WIDTH//2 - 25, HEIGHT-100, 5, "assets/travel.png")

# Obstacles et bonus
obstacle_list = []
fuel_list = []

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

# Charger images obstacles et fuel
obstacle_images = []
for i in range(5):
    path = f"assets/car{i}.png" if i > 0 else "assets/car.png"
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (60, 90))
    obstacle_images.append(img)

fuel_img = pygame.image.load("assets/gasoline.png")
fuel_img = pygame.transform.scale(fuel_img, (40, 40))

# Score et vies
score = 0
lives = 3
start_time = time.time()

# --- Boucle principale ---
running = True
while running:
    screen.fill((0,0,0))
    draw_background(screen, WIDTH, HEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            # Spawn obstacle
            obstacle_list.append(Obstacle(120, WIDTH-120, 5, obstacle_images))
            # Spawn fuel (1 chance sur 3)
            if random.randint(1,3) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, fuel_img))

    keys = pygame.key.get_pressed()
    player.move(keys, 120, WIDTH-120, 0, HEIGHT)
    player.draw(screen)

    # Déplacement obstacles
    for obs in obstacle_list[:]:
        obs.update()
        if obs.rect.colliderect(player.rect):
            lives -= 1
            obstacle_list.remove(obs)
        elif obs.rect.top > HEIGHT:
            obstacle_list.remove(obs)
        else:
            obs.draw(screen)

    # Déplacement fuel
    for f in fuel_list[:]:
        f.update()
        if f.rect.colliderect(player.rect):
            score += 10
            fuel_list.remove(f)
        elif f.rect.top > HEIGHT:
            fuel_list.remove(f)
        else:
            f.draw(screen)

    # Texte
    elapsed_time = int(time.time() - start_time)
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Vies: {lives}", True, (255,255,255)), (10,40))
    screen.blit(font.render(f"Temps: {elapsed_time}s", True, (255,255,255)), (10,70))

    if lives <= 0:
        screen.blit(font.render("GAME OVER", True, (255,50,50)), (WIDTH//2-80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

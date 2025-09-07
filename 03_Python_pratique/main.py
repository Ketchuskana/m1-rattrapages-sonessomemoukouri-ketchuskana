import pygame, sys, random, time
from player import Player
from background import draw_background
from obstacle import Obstacle
from fuel import Fuel

# --- Initialisation ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de survie routier")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

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
level = 1
last_speed_increase = start_time
obstacle_speed = 5

# Boutons fin de jeu
def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, (255,255,255))
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))
    return False

# --- Boucle principale ---
running = True
while running:
    screen.fill((0,0,0))
    draw_background(screen, WIDTH, HEIGHT)

    current_time = time.time()
    elapsed_time = int(current_time - start_time)

    # --- Augmentation de vitesse tous les 30s ---
    if current_time - last_speed_increase >= 30:
        obstacle_speed += 1
        level += 1
        last_speed_increase = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            # Spawn obstacle
            obstacle_list.append(Obstacle(120, WIDTH-120, obstacle_speed, obstacle_images))
            # Spawn fuel (1 chance sur 3)
            if random.randint(1,3) == 1:
                fuel_list.append(Fuel(120, WIDTH-120, 4, fuel_img))

    keys = pygame.key.get_pressed()
    player.move(keys, 120, WIDTH-120, 0, HEIGHT)
    player.draw(screen)

    # Déplacement obstacles
    for obs in obstacle_list[:]:
        obs.update()
        if obs.rect.colliderect(player.hitbox):
            lives -= 1
            obstacle_list.remove(obs)
        elif obs.rect.top > HEIGHT:
            obstacle_list.remove(obs)
        else:
            obs.draw(screen)

    # Déplacement fuel
    for f in fuel_list[:]:
        f.update()
        if f.rect.colliderect(player.hitbox):
            score += 10
            fuel_list.remove(f)
        elif f.rect.top > HEIGHT:
            fuel_list.remove(f)
        else:
            f.draw(screen)

    # Texte score, vies, temps et niveau
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Vies: {lives}", True, (255,255,255)), (10,40))
    screen.blit(font.render(f"Temps: {elapsed_time}s", True, (255,255,255)), (10,70))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (WIDTH-120,10))

    # --- Fin du jeu ---
    if lives <= 0:
        screen.blit(big_font.render("GAME OVER", True, (255,50,50)), (WIDTH//2-130, HEIGHT//2-50))
        replay = draw_button("Rejouer", WIDTH//2-100, HEIGHT//2+10, 90, 40, (0,100,200), (0,150,255))
        quit_game = draw_button("Quitter", WIDTH//2+10, HEIGHT//2+10, 90, 40, (200,0,0), (255,50,50))
        pygame.display.flip()
        if replay:
            # Reset du jeu
            score = 0
            lives = 3
            level = 1
            obstacle_speed = 5
            obstacle_list.clear()
            fuel_list.clear()
            start_time = time.time()
            last_speed_increase = start_time
        elif quit_game:
            running = False
        continue  # skip le reste pour ne pas bouger les obstacles

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

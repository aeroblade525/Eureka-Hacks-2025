import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1000, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Touch Nature")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (2, 43, 1)
BLACK = (0, 0, 0)

# Game variables
score = 100000000
click_power = 1
click_multiplier = 1
click_multiplier_cost = 30

# Auto-clicker types
auto_clickers = [
    {"name": "Plant Grass", "base_cost": 10, "cost": 10, "count": 0, "rate": 1},
    {"name": "Plant Bush", "base_cost": 50, "cost": 50, "count": 0, "rate": 5},
    {"name": "Plant Flower", "base_cost": 100, "cost": 100, "count": 0, "rate": 10},
    {"name": "Plant Tree", "base_cost": 500, "cost": 500, "count": 0, "rate": 20}
]

# Load images
grass_image = pygame.image.load("Grass.png").convert_alpha()
grass_image = pygame.transform.scale(grass_image, (30, 30))

bush_image = pygame.image.load("bush.png").convert_alpha()
bush_image = pygame.transform.scale(bush_image, (50, 50))

flower_image = pygame.image.load("Wilted Rose.png").convert_alpha()
flower_image = pygame.transform.scale(flower_image, (40, 40))

tree_image = pygame.image.load("Tree.png").convert_alpha()
tree_image = pygame.transform.scale(tree_image, (40, 50))

touch_nature_image = pygame.image.load("touch_Nature.png").convert_alpha()
touch_nature_image = pygame.transform.scale(touch_nature_image, (180, 75))

# Lists to store planted items
grass_positions = []
bush_positions = []
flower_positions = []
tree_positions = []

# Fonts
main_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 20)

# Main loop
clock = pygame.time.Clock()
running = True

# Center image properties
image_width = 180
image_height = 75
image_x = WIDTH // 2 - image_width // 2
image_y = HEIGHT // 2 - image_height // 2
image_rect = pygame.Rect(image_x, image_y, image_width, image_height)

# Button layout
button_width = 300
button_height = 45
button_spacing = 15
button_start_y = 20

def create_button_rect(index):
    return pygame.Rect(
        WIDTH - button_width - 20,
        button_start_y + (button_height + button_spacing) * index,
        button_width,
        button_height
    )

def draw_button(screen, rect, color, text):
    # Draw black border first
    pygame.draw.rect(screen, BLACK, rect.inflate(4, 4), border_radius=8)
    # Then draw actual button on top (slightly smaller)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def random_position_away_from_center():
    while True:
        x = random.randint(0, WIDTH - 50)
        y = random.randint(0, HEIGHT - 50)
        item_rect = pygame.Rect(x, y, 50, 50)
        if not item_rect.colliderect(image_rect.inflate(100, 100)):  # Keep distance from center
            return (x, y)

while running:
    screen.fill(DARK_GREEN)  # <-- Changed background color

    # Draw all planted items
    for pos in grass_positions:
        screen.blit(grass_image, pos)

    for pos in bush_positions:
        screen.blit(bush_image, pos)

    for pos in flower_positions:
        screen.blit(flower_image, pos)

    for pos in tree_positions:
        screen.blit(tree_image, pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Click on center image
            if image_rect.collidepoint(mouse_pos):
                score += click_power * click_multiplier

            # Auto-clicker buttons
            for i, ac in enumerate(auto_clickers):
                button_rect = create_button_rect(i)
                if button_rect.collidepoint(mouse_pos):
                    if score >= ac["cost"]:
                        score -= ac["cost"]
                        ac["count"] += 1
                        ac["cost"] = int(ac["base_cost"] * (1.2 ** ac["count"]))

                        x, y = random_position_away_from_center()

                        if i == 0:  # Plant Grass
                            grass_positions.append((x, y))
                        elif i == 1:  # Plant Bush
                            bush_positions.append((x, y))
                        elif i == 2:  # Plant Flower
                            flower_positions.append((x, y))
                        elif i == 3:  # Plant Tree
                            tree_positions.append((x, y))

            # Click multiplier button
            multiplier_rect = pygame.Rect(20, HEIGHT - 70, 300, 50)
            if multiplier_rect.collidepoint(mouse_pos):
                if score >= click_multiplier_cost:
                    score -= click_multiplier_cost
                    click_multiplier *= 2
                    click_multiplier_cost *= 3

    # Add auto income
    for ac in auto_clickers:
        score += ac["count"] * ac["rate"] / 60

    # Draw center clickable image
    screen.blit(touch_nature_image, (image_x, image_y))

    # Draw buttons
    for i, ac in enumerate(auto_clickers):
        button_text = f"{ac['name']}: {ac['cost']} pts - Owned: {ac['count']} (+{ac['rate']}/s)"
        button_color = GREEN
        draw_button(screen, create_button_rect(i), button_color, button_text)

    # Click multiplier
    multiplier_text = f"Click Multiplier (x{click_multiplier}) - Cost: {click_multiplier_cost}"
    draw_button(screen, pygame.Rect(20, HEIGHT - 70, 350, 60), RED, multiplier_text)

    # Score and stats
    score_text = main_font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (20, 20))

    click_text = main_font.render(f"Click Power: {click_power * click_multiplier}/click", True, WHITE)
    screen.blit(click_text, (20, 60))

    total_income = sum(ac["count"] * ac["rate"] for ac in auto_clickers)
    income_text = main_font.render(f"Income: {total_income}/second", True, WHITE)
    screen.blit(income_text, (20, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

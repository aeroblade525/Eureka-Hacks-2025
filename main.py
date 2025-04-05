import pygame
import sys
import random
import time

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
GRAY = (150, 150, 150)
FACT_BG = (50, 50, 50, 200)  # Semi-transparent dark background

# Game variables
score = 0
click_power = 1
click_multiplier = 1
click_multiplier_cost = 30
last_fact_time = time.time()  # Track when last fact was shown

# Random facts
FACTS = [
    "Trees communicate through underground fungal networks!",
    "A single tree can absorb 48 pounds of CO2 per year.",
    "Bamboo is the fastest growing plant on Earth (up to 35 inches per day!).",
    "The Amazon rainforest produces 20% of Earth's oxygen.",
    "Over 80% of the world's forests have been destroyed.",
    "An acre of trees absorbs the CO2 equivalent of driving 26,000 miles.",
    "The oldest living tree is a bristlecone pine named Methuselah (over 5,000 years old!).",
    "Plants can detect water sources through vibrations and grow toward them.",
    "Some plants recognize and favor their siblings when growing nearby.",
    "The smell of freshly cut grass is actually a plant distress signal.",
    "One large tree can provide a day's oxygen for four people.",
    "The tallest tree in the world is Hyperion, a 380-foot redwood.",
    "The world's smallest tree is the dwarf willow, barely 2 inches tall.",
    "Trees reduce noise pollution by absorbing sound waves.",
    "A tree's leaves can be 10°F cooler than the surrounding air temperature.",
    "The rings of a tree can reveal past climate conditions.",
    "Some trees can live for over 5,000 years.",
    "The baobab tree can store up to 32,000 gallons of water in its trunk.",
    "The rainbow eucalyptus has naturally multicolored bark.",
    "The dragon's blood tree gets its name from its red sap.",
    "The corpse flower smells like rotting flesh when it blooms.",
    "The sensitive plant (Mimosa pudica) folds its leaves when touched.",
    "Some plants can grow in complete darkness underground.",
    "The world's largest flower (Rafflesia) can weigh up to 24 pounds.",
    "The Venus flytrap can count - it only closes after two touches.",
    "Some cacti can survive for over a year without rain.",
    "The oldest known plant is a 9,500-year-old spruce in Sweden.",
    "A sunflower is actually thousands of tiny flowers in one head.",
    "The seeds of the coco de mer palm can weigh up to 66 pounds.",
    "The leaves of the titan arum can grow over 15 feet tall.",
    "Some plants can grow in temperatures as low as -40°F.",
    "The leaves of the giant water lily can support a small child's weight.",
    "The wolffia plant is the smallest flowering plant (size of a grain of rice).",
    "The fastest-growing plant is bamboo (up to 35 inches per day).",
    "The seeds of some lotus plants remain viable for over 1,000 years.",
    "The leaves of the telegraph plant move in jerky motions throughout the day.",
    "Some plants can survive being frozen solid and revive when thawed.",
    "The leaves of the sensitive plant fold within seconds of being touched.",
    "The leaves of the compass plant align north-south to minimize sun exposure.",
    "The resurrection plant can survive years without water and revive in minutes.",
    "The leaves of the silver dollar plant are completely waterproof.",
    "Some plants can grow in highly acidic soil with pH levels below 3.",
    "The leaves of the rubber tree contain latex used to make natural rubber.",
    "The bark of the cork oak regenerates after being harvested.",
    "The leaves of the neem tree have natural insect-repelling properties.",
    "The roots of the mesquite tree can reach depths of 175 feet.",
    "The leaves of the eucalyptus tree contain oil that repels insects.",
    "The bark of the paper birch peels off in thin, paper-like layers.",
    "The leaves of the Joshua tree were used by Native Americans for baskets.",
    "The wood of the balsa tree is lighter than cork.",
    "The leaves of the pitcher plant form a deadly trap for insects.",
    "The flowers of the corpse plant generate heat to spread their smell.",
    "The leaves of the sundew plant are covered in sticky, digestive hairs.",
    "The roots of the strangler fig eventually kill their host tree.",
    "The leaves of the sensitive brier fold up when touched.",
    "The flowers of the chocolate cosmos smell like chocolate.",
    "The leaves of the telegraph plant move in response to light changes.",
    "The seeds of the squirting cucumber explode when ripe.",
    "The leaves of the touch-me-not plant fold when touched.",
    "The flowers of the moonflower only open at night.",
    "The leaves of the sensitive fern are extremely delicate.",
    "The roots of the mangrove tree can filter salt from seawater.",
    "The leaves of the silver vine are more attractive to cats than catnip.",
    "The flowers of the titan arum can reach 10 feet tall.",
    "The leaves of the sensitive partridge pea fold when touched.",
    "The seeds of the sandbox tree explode with enough force to injure people.",
    "The leaves of the shameplant fold inward when touched.",
    "The flowers of the night-blooming cereus only open for one night.",
    "The leaves of the telegraph weed move in response to touch.",
    "The seeds of the jewelweed explode when touched (hence 'touch-me-not').",
    "The leaves of the sensitive joint-vetch fold when disturbed.",
    "The flowers of the chocolate flower smell like cocoa.",
    "The leaves of the sensitive pea plant fold when touched.",
    "The roots of the aspen tree can live for thousands of years.",
    "The leaves of the sensitive briar fold when touched.",
    "The flowers of the evening primrose only open at dusk.",
    "The leaves of the sensitive tree fold when touched.",
    "The roots of the giant sequoia rarely exceed 6 feet in depth.",
    "The leaves of the sensitive plant (Mimosa pudica) have rapid movement.",
    "The flowers of the night phlox smell like vanilla and almonds.",
    "The leaves of the telegraph plant move in response to light.",
    "The seeds of the Himalayan balsam explode when touched."
]

# Fact display system
active_facts = []  # List of dictionaries: {text: str, spawn_time: float, y_offset: int}

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
small_font = pygame.font.Font(None, 24)
fact_font = pygame.font.Font(None, 20)  # Smaller font for facts

def create_button_rect(index):
    return pygame.Rect(
        WIDTH - button_width - 20,
        button_start_y + (button_height + button_spacing) * index,
        button_width,
        button_height
    )

def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, BLACK, rect.inflate(4, 4), border_radius=8)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def random_position_away_from_center():
    while True:
        x = random.randint(0, WIDTH - 50)
        y = random.randint(0, HEIGHT - 50)
        item_rect = pygame.Rect(x, y, 50, 50)
        if not item_rect.colliderect(image_rect.inflate(100, 100)):
            return (x, y)

def draw_fact(screen, text, y_offset):
    """Draw a fact bubble in the bottom right corner"""
    text_surface = fact_font.render(text, True, WHITE)
    
    # Calculate background size with padding
    padding = 10
    bg_width = text_surface.get_width() + padding * 2
    bg_height = text_surface.get_height() + padding * 2
    
    # Position in bottom right with offset
    bg_rect = pygame.Rect(
        WIDTH - bg_width - 20,
        HEIGHT - bg_height - 20 - y_offset,
        bg_width,
        bg_height
    )
    
    # Draw background with rounded corners
    pygame.draw.rect(screen, FACT_BG, bg_rect, border_radius=8)
    # Draw text centered in background
    screen.blit(text_surface, (bg_rect.x + padding, bg_rect.y + padding))

def update_facts():
    """Update and clean up facts"""
    current_time = time.time()
    
    # Remove facts older than 3 seconds
    active_facts[:] = [f for f in active_facts if current_time - f['spawn_time'] < 3]
    
    # Update y offsets based on position in list (newer facts go at bottom)
    for i, fact in enumerate(active_facts):
        fact['y_offset'] = i * 40  # 40px per fact

# Main game loop
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

while running:
    screen.fill(DARK_GREEN)

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

            if image_rect.collidepoint(mouse_pos):
                score += click_power * click_multiplier

            for i, ac in enumerate(auto_clickers):
                button_rect = create_button_rect(i)
                if button_rect.collidepoint(mouse_pos):
                    if score >= ac["cost"]:
                        score -= ac["cost"]
                        ac["count"] += 1
                        ac["cost"] = int(ac["base_cost"] * (1.2 ** ac["count"]))

                        x, y = random_position_away_from_center()

                        if i == 0:
                            grass_positions.append((x, y))
                        elif i == 1:
                            bush_positions.append((x, y))
                        elif i == 2:
                            flower_positions.append((x, y))
                        elif i == 3:
                            tree_positions.append((x, y))

            multiplier_rect = pygame.Rect(20, HEIGHT - 70, 300, 50)
            if multiplier_rect.collidepoint(mouse_pos):
                if score >= click_multiplier_cost:
                    score -= click_multiplier_cost
                    click_multiplier *= 2
                    click_multiplier_cost *= 3

    # Add auto income
    for ac in auto_clickers:
        score += ac["count"] * ac["rate"] / 60

    # Check if 20 seconds have passed since last fact
    current_time = time.time()
    if current_time - last_fact_time >= 20:
        last_fact_time = current_time
        fact_text = random.choice(FACTS)
        active_facts.append({
            'text': fact_text,
            'spawn_time': current_time,
            'y_offset': 0
        })

    # Update facts
    update_facts()

    # Draw center clickable image
    screen.blit(touch_nature_image, (image_x, image_y))

    # Draw score under the center image
    score_text = small_font.render(f"Score: {int(score)}", True, GRAY)
    score_rect = score_text.get_rect(center=(WIDTH//2, image_y + image_height + 30))
    screen.blit(score_text, score_rect)

    # Draw power and income at the top center
    click_text = small_font.render(f"{click_power * click_multiplier} seeds / click", True, GRAY)
    click_rect = click_text.get_rect(center=(WIDTH//2, 30))
    screen.blit(click_text, click_rect)

    total_income = sum(ac["count"] * ac["rate"] for ac in auto_clickers)
    income_text = small_font.render(f"{total_income} seeds / second", True, GRAY)
    income_rect = income_text.get_rect(center=(WIDTH//2, 60))
    screen.blit(income_text, income_rect)

    # Draw buttons
    for i, ac in enumerate(auto_clickers):
        button_text = f"{ac['name']}: {ac['cost']} pts - Owned: {ac['count']} (+{ac['rate']}/s)"
        button_color = GREEN
        draw_button(screen, create_button_rect(i), button_color, button_text)

    # Click multiplier
    multiplier_text = f"Seed Multiplier (x{click_multiplier}) - Seed Cost: {click_multiplier_cost}"
    draw_button(screen, pygame.Rect(20, HEIGHT - 70, 350, 60), RED, multiplier_text)

    # Draw active facts
    for fact in active_facts:
        draw_fact(screen, fact['text'], fact['y_offset'])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
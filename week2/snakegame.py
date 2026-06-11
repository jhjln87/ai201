import pygame
import random
import sys
import math

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
GRID_SIZE = 10
GRID_COUNT = 40  # 40px per grid cell = 400x400 window
WINDOW_SIZE = GRID_SIZE * GRID_COUNT
INFO_BAR_HEIGHT = 150
SCREEN_WIDTH = WINDOW_SIZE
SCREEN_HEIGHT = WINDOW_SIZE + INFO_BAR_HEIGHT

FPS = 8  # Speed of the game (comfortable for AI and viewing)

# Colors (Whimsical Palette)
COLOR_BG = (28, 28, 30)
COLOR_GRID = (44, 44, 46)
COLOR_SNAKE_HEAD = (50, 215, 75)
COLOR_SNAKE_BODY = (40, 168, 60)
COLOR_HEALTH_BAR = (255, 69, 58)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_MUTED = (142, 142, 147)

# Mario Kart Items Definition
ITEMS_CONFIG = {
    "Green Shell": {
        "color": (100, 255, 100),
        "shape": "circle",
        "flavor": [
            "You crunched a Green Shell! Your conscience bounces off the walls.",
            "Green Shell consumed. Somewhere, a plumber just lost his lead.",
            "Sniper elite! That Green Shell tasted like fiberglass and victory."
        ]
    },
    "Banana Peel": {
        "color": (255, 214, 10),
        "shape": "triangle",
        "flavor": [
            "You ate a Banana Peel. You slipped internally, but gained mass!",
            "Potassium level UP. Watch your step, or don't. I'm a sign, not a cop.",
            "Slipped it right down the gullet. A classic traction hazard turned snack."
        ]
    },
    "Super Mushroom": {
        "color": (255, 55, 95),
        "shape": "mushroom",
        "flavor": [
            "Mushroom power! You feel slightly faster, though functionally identical.",
            "A fungal delicacy! The fabric of space-time wobbles rhythmically.",
            "You ate the Super Mushroom. Your ego expands exponentially!"
        ]
    }
}

# ==========================================
# GAME CLASS
# ==========================================
class MarioKartSnake:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐍 Whimsical Auto-Snake: Kart Edition 🏎️")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 14, bold=True)
        
        self.reset_game()

    def reset_game(self):
        # Snake State
        # Start in the middle of our 10x10 grid
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.direction = (0, -1) # Moving UP initially
        self.health = 100
        self.score = 0
        
        # Item State
        self.item_pos = None
        self.item_type = None
        self.spawn_item()
        
        # Text Flavor Ticker
        self.current_flavor = "Welcome to the track. The AI is driving. Relax."

    def spawn_item(self):
        while True:
            self.item_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if self.item_pos not in self.snake:
                break
        self.item_type = random.choice(list(ITEMS_CONFIG.keys()))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Manual reset key just in case
                    self.reset_game()

    # ==========================================
    # SUBTASK LAST: AI AUTOPLAY BRAIN
    # ==========================================
    def ai_choose_direction(self):
        head_x, head_y = self.snake[0]
        target_x, target_y = self.item_pos

        # All possible 90-degree moves
        possible_moves = [
            ((0, -1), "UP"),
            ((0, 1), "DOWN"),
            ((-1, 0), "LEFT"),
            ((1, 0), "RIGHT")
        ]

        valid_moves = []

        for move, name in possible_moves:
            # Rule: Never directly reverse into yourself
            if move[0] == -self.direction[0] and move[1] == -self.direction[1]:
                continue
            
            # Predict next position with screen-wrapping taken into account
            next_x = (head_x + move[0]) % GRID_SIZE
            next_y = (head_y + move[1]) % GRID_SIZE
            next_pos = (next_x, next_y)

            # Score the move based on Manhattan distance to target via wrapping
            # Calculates standard distance vs wrapped distance to find quickest path
            dx = abs(next_x - target_x)
            dy = abs(next_y - target_y)
            dist_x = min(dx, GRID_SIZE - dx)
            dist_y = min(dy, GRID_SIZE - dy)
            distance = dist_x + dist_y

            # Weight self-collision as dangerous, but passable if necessary
            penalty = 0
            if next_pos in self.snake:
                penalty = 1000  # High penalty, but not infinitely impossible if cornered

            total_cost = distance + penalty
            valid_moves.append((total_cost, move))

        # Sort moves by lowest cost (closest to item + safest)
        valid_moves.sort(key=lambda x: x[0])
        
        if valid_moves:
            self.direction = valid_moves[0][1]

    # ==========================================
    # GAME LOGIC & SUBTASKS 2 & 4
    # ==========================================
    def update(self):
        # 1. Let the AI pick the best move
        self.ai_choose_direction()

        # 2. Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        
        # Subtask 2 & Last: Screen wrapping calculation
        new_head = ((head_x + dir_x) % GRID_SIZE, (head_y + dir_y) % GRID_SIZE)

        # Subtask 2: Check self-intersection (Lose health instead of instant death)
        if new_head in self.snake:
            self.health -= 25
            self.current_flavor = f" OUCH! Passed through yourself. Health down to {self.health}%!"
            if self.health <= 0:
                self.current_flavor = "💀 Absolute structural collapse! Game Over. Restarting..."
                self.draw() # Render the death text briefly
                pygame.display.flip()
                pygame.time.wait(2000)
                self.reset_game()
                return

        # Move snake
        self.snake.insert(0, new_head)

        # 3. Check for item consumption
        if new_head == self.item_pos:
            self.score += 1
            # Replenish some health upon eating, capped at 100
            self.health = min(100, self.health + 10)
            
            # Subtask 4: Update Flavor Text
            self.current_flavor = random.choice(ITEMS_CONFIG[self.item_type]["flavor"])
            
            # Respawn item
            self.spawn_item()
        else:
            # Remove tail if didn't eat
            self.snake.pop()

    # ==========================================
    # GRAPHICS & SUBTASK 3 (MARIO KART RENDER)
    # ==========================================
    def draw_item(self, x, y, conf):
        color = conf["color"]
        shape = conf["shape"]
        
        # Center of the specific grid cell
        center_x = x * GRID_COUNT + GRID_COUNT // 2
        center_y = y * GRID_COUNT + GRID_COUNT // 2
        radius = GRID_COUNT // 3

        if shape == "circle": # Green Shell
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
            # Shell texture lines
            pygame.draw.circle(self.screen, COLOR_BG, (center_x, center_y), radius // 2, 2)
            
        elif shape == "triangle": # Banana Peel
            pt1 = (center_x, center_y - radius)
            pt2 = (center_x - radius, center_y + radius)
            pt3 = (center_x + radius, center_y + radius)
            pygame.draw.polygon(self.screen, color, [pt1, pt2, pt3])
            
        elif shape == "mushroom": # Super Mushroom
            # Cap
            pygame.draw.circle(self.screen, color, (center_x, center_y - 2), radius)
            # Stem
            stem_rect = pygame.Rect(center_x - radius//2, center_y, radius, radius)
            pygame.draw.rect(self.screen, (240, 240, 240), stem_rect)
            # Eyes/Dots details roughly rendered
            pygame.draw.circle(self.screen, COLOR_BG, (center_x - 4, center_y - 2), 2)
            pygame.draw.circle(self.screen, COLOR_BG, (center_x + 4, center_y - 2), 2)

    def draw(self):
        self.screen.fill(COLOR_BG)

        # Draw Grid Board (10x10)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * GRID_COUNT, y * GRID_COUNT, GRID_COUNT, GRID_COUNT)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)

        # Draw Mario Kart Item (Subtask 3)
        if self.item_pos:
            self.draw_item(self.item_pos[0], self.item_pos[1], ITEMS_CONFIG[self.item_type])

        # Draw Snake
        for i, segment in enumerate(self.snake):
            rect = pygame.Rect(segment[0] * GRID_COUNT + 2, segment[1] * GRID_COUNT + 2, GRID_COUNT - 4, GRID_COUNT - 4)
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

        # --- Draw Info UI Dashboard ---
        ui_top = WINDOW_SIZE
        # Background splitter
        pygame.draw.rect(self.screen, (18, 18, 18), (0, ui_top, SCREEN_WIDTH, INFO_BAR_HEIGHT))
        pygame.draw.line(self.screen, COLOR_TEXT_MUTED, (0, ui_top), (SCREEN_WIDTH, ui_top), 2)

        # Stats Strings
        score_text = self.font.render(f"ITEMS COLLECTED: {self.score}", True, COLOR_TEXT)
        health_label = self.font.render(f"HP: {self.health}%", True, COLOR_HEALTH_BAR)
        
        self.screen.blit(score_text, (20, ui_top + 15))
        self.screen.blit(health_label, (280, ui_top + 15))

        # Health Bar Drawing
        pygame.draw.rect(self.screen, (60, 0, 0), (20, ui_top + 35, SCREEN_WIDTH - 40, 12))
        current_health_width = int((SCREEN_WIDTH - 40) * (self.health / 100))
        pygame.draw.rect(self.screen, COLOR_HEALTH_BAR, (20, ui_top + 35, current_health_width, 12))

        # Subtask 4: Text Ticker Display (Handles wrapping text elegantly)
        words = self.current_flavor.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < SCREEN_WIDTH - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        # Print flavor text lines
        y_offset = ui_top + 65
        for line in lines[:3]: # Cap out at 3 lines to fit UI bounding space safely
            flavor_text = self.font.render(line.strip(), True, COLOR_TEXT_MUTED)
            self.screen.blit(flavor_text, (20, y_offset))
            y_offset += 18

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = MarioKartSnake()
    game.run()
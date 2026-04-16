import pygame
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FPS = 60

# Gameplay Settings
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_SPEED = 3.5
PIPE_GAP = 180
PIPE_WIDTH = 90
PIPE_FREQUENCY = 1500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Game Assets/hind.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 35))
        except pygame.error:
            self.image = pygame.Surface((50, 35), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, YELLOW, [0, 0, 50, 35])

        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.movement = 0
        self.rotated_image = self.image

    def update(self):
        self.movement += GRAVITY
        self.rect.centery += int(self.movement)

        angle = -self.movement * 3
        angle = max(min(angle, 30), -90)

        self.rotated_image = pygame.transform.rotate(self.image, angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.rotated_image)

    def flap(self):
        self.movement = FLAP_STRENGTH

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.position = position
        self.passed = False

        try:
            if position == 1:
                self.image = pygame.image.load("Game Assets/pipe.tap.png").convert_alpha()
            else:
                self.image = pygame.image.load("Game Assets/pipe_bottom.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, 600))
        except pygame.error:
            self.image = pygame.Surface((PIPE_WIDTH, 600))
            self.image.fill(GREEN)

        if position == 1:
            self.rect = self.image.get_rect(midbottom=(x, y - PIPE_GAP // 2))
        else:
            self.rect = self.image.get_rect(midtop=(x, y + PIPE_GAP // 2))

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < -50:
            self.kill()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Hill Climbing AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 60, bold=True)

        try:
            self.bg_image = pygame.image.load("Game Assets/background.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((135, 206, 235))

        self.bg_x = 0
        self.score = 0
        self.high_score = 0
        self.game_active = True
        self.autopilot = False

        self.modes = ["Manual", "Hill Climbing"]
        self.mode_index = 0

        self.bird = pygame.sprite.GroupSingle(Bird())
        self.pipes = pygame.sprite.Group()

        self.pipe_timer = pygame.USEREVENT
        pygame.time.set_timer(self.pipe_timer, PIPE_FREQUENCY)

    def create_pipes(self):
        y = random.randint(250, SCREEN_HEIGHT - 250)
        return Pipe(SCREEN_WIDTH + 100, y, 1), Pipe(SCREEN_WIDTH + 100, y, -1)

    def check_collision(self):
        if pygame.sprite.spritecollide(self.bird.sprite, self.pipes, False, pygame.sprite.collide_mask):
            return False
        if self.bird.sprite.rect.top <= 0 or self.bird.sprite.rect.bottom >= SCREEN_HEIGHT:
            return False
        return True

    def update_score(self):
        bird_x = self.bird.sprite.rect.centerx
        for pipe in self.pipes:
            if pipe.position == 1 and not pipe.passed and bird_x > pipe.rect.right:
                self.score += 1
                pipe.passed = True
        self.high_score = max(self.high_score, self.score)

    def get_next_pipe(self):
        bird_x = self.bird.sprite.rect.centerx
        pipes = [p for p in self.pipes if p.rect.right > bird_x]
        return min(pipes, key=lambda p: p.rect.x) if pipes else None

    def get_target_y(self, pipe):
        if not pipe:
            return SCREEN_HEIGHT // 2
        return pipe.rect.bottom + PIPE_GAP // 2 if pipe.position == 1 else pipe.rect.top - PIPE_GAP // 2

    # --- Hill Climbing AI ---
    def ai_hill_climbing(self):
        pipe = self.get_next_pipe()
        target_y = self.get_target_y(pipe)

        if self.bird.sprite.rect.centery > target_y + 10 and self.bird.sprite.movement > 0:
            self.bird.sprite.flap()

    def display_ui(self):
        ui = pygame.Surface((260, 120), pygame.SRCALPHA)
        ui.fill((0, 0, 0, 150))
        self.screen.blit(ui, (10, 10))

        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (20, 20))
        self.screen.blit(self.font.render(f"Best: {self.high_score}", True, WHITE), (20, 45))

        auto = "ON" if self.autopilot else "OFF"
        color = GREEN if self.autopilot else RED
        self.screen.blit(self.font.render(f"Autopilot (A): {auto}", True, color), (20, 70))

        self.screen.blit(self.font.render(f"Mode (M): {self.modes[self.mode_index]}", True, CYAN), (20, 95))

    def reset_game(self):
        self.game_active = True
        self.pipes.empty()
        self.bird.sprite.rect.center = (100, SCREEN_HEIGHT // 2)
        self.bird.sprite.movement = 0
        self.score = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active and not self.autopilot:
                        self.bird.sprite.flap()
                    if event.key == pygame.K_a:
                        self.autopilot = not self.autopilot
                    if event.key == pygame.K_m:
                        self.mode_index = (self.mode_index + 1) % len(self.modes)
                    if event.key == pygame.K_r and not self.game_active:
                        self.reset_game()

                if event.type == self.pipe_timer and self.game_active:
                    self.pipes.add(self.create_pipes())

            self.bg_x = (self.bg_x - 1.5) % SCREEN_WIDTH
            self.screen.blit(self.bg_image, (self.bg_x, 0))
            self.screen.blit(self.bg_image, (self.bg_x - SCREEN_WIDTH, 0))

            if self.game_active:
                if self.autopilot and self.modes[self.mode_index] == "Hill Climbing":
                    self.ai_hill_climbing()

                self.pipes.update()
                self.pipes.draw(self.screen)
                self.bird.update()
                self.bird.draw(self.screen)

                self.game_active = self.check_collision()
                self.update_score()
                self.display_ui()
            else:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))

                self.screen.blit(self.large_font.render("GAME OVER", True, WHITE),
                                 (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
                self.screen.blit(self.font.render("Press R to Restart", True, YELLOW),
                                 (SCREEN_WIDTH//2 - 90, SCREEN_HEIGHT//2 + 40))

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()

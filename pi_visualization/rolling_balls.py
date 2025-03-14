import pygame
import random
import colorsys
import math
from typing import List, Tuple

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Ball:
    """Ball representing a Pi digit with physics and collision properties."""

    def __init__(self, digit: int, x: float, y: float, radius: int, color: Tuple[int, int, int]):
        self.digit = digit
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.mass = radius * 0.5

        # Generate text surface once for better performance
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(str(digit), True, (255, 255, 255))
        self.text_rect = self.text.get_rect()  # Fixed: store rectangle for centering text

    def move(self):
        """Update ball position based on its velocity."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off the walls with friction
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -0.95
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.speed_x *= -0.95

        if self.y - self.radius < 0:
            self.y = self.radius
            self.speed_y *= -0.95
        elif self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.speed_y *= -0.95

        # Apply gravity and air resistance
        self.speed_y += 0.1  # Gravity
        self.speed_x *= 0.995  # Horizontal friction
        self.speed_y *= 0.995  # Vertical friction

    def draw(self, screen):
        """Draw the ball and its digit."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Center the text on the ball
        self.text_rect.center = (int(self.x), int(self.y))
        screen.blit(self.text, self.text_rect)

    def check_collision(self, other_ball):
        """Check and resolve collision with another ball."""
        dx = other_ball.x - self.x
        dy = other_ball.y - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance < self.radius + other_ball.radius:
            # Calculate collision response
            angle = math.atan2(dy, dx)
            total_mass = self.mass + other_ball.mass

            # Calculate velocities after collision
            v1x = ((self.mass - other_ball.mass) * self.speed_x +
                  2 * other_ball.mass * other_ball.speed_x) / total_mass
            v1y = ((self.mass - other_ball.mass) * self.speed_y +
                  2 * other_ball.mass * other_ball.speed_y) / total_mass
            v2x = ((other_ball.mass - self.mass) * other_ball.speed_x +
                  2 * self.mass * self.speed_x) / total_mass
            v2y = ((other_ball.mass - self.mass) * other_ball.speed_y +
                  2 * self.mass * self.speed_y) / total_mass

            # Apply new velocities
            self.speed_x = v1x
            self.speed_y = v1y
            other_ball.speed_x = v2x
            other_ball.speed_y = v2y

            # Move balls apart to prevent sticking
            overlap = 0.5 * (self.radius + other_ball.radius - distance + 1)
            self.x -= overlap * dx / distance
            self.y -= overlap * dy / distance
            other_ball.x += overlap * dx / distance
            other_ball.y += overlap * dy / distance


def get_color_for_digit(digit: int) -> Tuple[int, int, int]:
    """Generate a visually appealing color based on the digit."""
    # Use the HSV color space for better visual distribution
    hue = digit / 10.0
    saturation = 0.7 + (digit % 3) * 0.1  # Varying saturation
    value = 0.9

    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))


def run_rolling_balls(pi_digits: List[int], max_balls: int = 100):
    """Run the rolling balls visualization.

    Args:
        pi_digits: List of Pi digits to visualize
        max_balls: Maximum number of balls to display
    """
    import math  # Import needed for collision physics

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rolling Pi Balls")

    balls = []
    digit_counts = {}

    # Use only a portion of digits for better performance
    digits_to_show = min(max_balls, len(pi_digits))

    # Create balls for each digit of Pi
    for i, digit in enumerate(pi_digits[:digits_to_show]):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)

        # Adjust radius based on digit frequency
        if digit not in digit_counts:
            digit_counts[digit] = 0
        digit_counts[digit] += 1

        base_radius = 20
        radius = base_radius + digit_counts[digit] // 3
        radius = min(radius, 40)  # Cap the maximum radius

        color = get_color_for_digit(digit)
        balls.append(Ball(digit, x, y, radius, color))

    # Information display
    info_font = pygame.font.Font(None, 24)

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not paused:
            # Update ball positions
            for i, ball in enumerate(balls):
                ball.move()

                # Check for collisions with other balls
                for j in range(i + 1, len(balls)):
                    ball.check_collision(balls[j])

        # Drawing
        screen.fill((0, 0, 0))

        # Draw balls
        for ball in balls:
            ball.draw(screen)

        # Display information
        info_text = f"Pi Visualization - {len(balls)} digits shown - {'PAUSED' if paused else 'RUNNING'}"
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
import pygame
import numpy as np
import time
import sys
from typing import List, Tuple, Optional


class PiMusicPlayer:
    """Converts Pi digits to musical notes and provides visualization."""

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize the music player.

        Args:
            screen_width: Width of the visualization window
            screen_height: Height of the visualization window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

        # Create display window
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pi Symphony")

        # Define musical scales (frequencies in Hz)
        self.pentatonic_scale = [261.63, 293.66, 329.63, 392.00, 440.00]  # C, D, E, G, A
        self.major_scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major
        self.chromatic_scale = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23,
                               369.99, 392.00, 415.30, 440.00, 466.16, 493.88]  # Chromatic C4-B4

        # Font for display
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Visual elements
        self.note_history = []  # Track played notes for visualization

    def get_frequency(self, digit: int, scale: List[float]) -> float:
        """Map a digit (0-9) to a frequency in the given scale.

        Args:
            digit: A digit from 0-9
            scale: List of frequencies representing a musical scale

        Returns:
            The frequency for the given digit
        """
        index = digit % len(scale)
        octave_adjust = digit // len(scale)
        base_freq = scale[index]
        # Adjust octave if needed
        return base_freq * (2 ** octave_adjust)

    def generate_sound(self, frequency: float, duration: float = 0.3) -> pygame.mixer.Sound:
        """Generate a sound with the given frequency.

        Args:
            frequency: Frequency in Hz
            duration: Duration of the sound in seconds

        Returns:
            PyGame sound object
        """
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))

        # Generate a sine wave
        buf = np.sin(2 * np.pi * np.arange(n_samples) * frequency / sample_rate)

        # Apply amplitude envelope
        envelope = np.ones(n_samples)
        attack = int(0.1 * n_samples)  # 10% attack
        decay = int(0.8 * n_samples)   # 80% decay

        # Apply attack (fade in)
        envelope[:attack] = np.linspace(0, 1, attack)
        # Apply decay (fade out)
        envelope[decay:] = np.linspace(1, 0, n_samples - decay)

        # Apply envelope
        buf = buf * envelope

        # Convert to 16-bit signed integers
        buf = (buf * 32767).astype(np.int16)

        # Create PyGame Sound object
        return pygame.mixer.Sound(buffer=buf)

    def draw_visualization(self, current_digit: int, position: int, digits: List[int]):
        """Draw the visualization for the current note and digit.

        Args:
            current_digit: The current digit being played
            position: Position in the Pi sequence
            digits: List of all digits
        """
        # Clear the screen
        self.screen.fill((0, 0, 30))  # Dark blue background

        # Add the new note to history
        note_y = self.screen_height - 100 - current_digit * 30
        self.note_history.append((position, note_y, current_digit))

        # Keep only the last 100 notes
        if len(self.note_history) > 100:
            self.note_history.pop(0)

        # Draw the piano keyboard at the bottom
        key_width = self.screen_width / 10
        for i in range(10):
            # White keys
            key_rect = pygame.Rect(i * key_width, self.screen_height - 80, key_width - 2, 70)
            key_color = (220, 220, 220)  # Default white key

            # Highlight the current digit
            if i == current_digit:
                key_color = (255, 200, 100)

            pygame.draw.rect(self.screen, key_color, key_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), key_rect, 1)  # Black outline

            # Draw digit on key
            digit_text = self.font.render(str(i), True, (0, 0, 0))
            self.screen.blit(digit_text, (i * key_width + key_width/2 - 10, self.screen_height - 50))

        # Draw note history as a connected line
        if len(self.note_history) > 1:
            for i in range(1, len(self.note_history)):
                prev_x = self.screen_width - (len(self.note_history) - self.note_history[i-1][0] + position) * 8
                prev_y = self.note_history[i-1][1]
                current_x = self.screen_width - (len(self.note_history) - self.note_history[i][0] + position) * 8
                current_y = self.note_history[i][1]

                # Only draw if on screen
                if 0 <= prev_x < self.screen_width and 0 <= current_x < self.screen_width:
                    pygame.draw.line(self.screen, (100, 255, 100), (prev_x, prev_y),
                                    (current_x, current_y), 2)

                    # Draw circle at each point
                    pygame.draw.circle(self.screen, (255, 255, 100),
                                      (current_x, current_y), 5)

        # Display the current position and digit
        position_text = self.font.render(f"Position: {position}", True, (255, 255, 255))
        digit_text = self.font.render(f"Digit: {current_digit}", True, (255, 255, 255))
        self.screen.blit(position_text, (20, 20))
        self.screen.blit(digit_text, (20, 60))

        # Display instructions
        instructions = "Space: Pause | Esc: Quit | 1-3: Change Scale | Up/Down: Speed"
        instr_text = self.small_font.render(instructions, True, (200, 200, 200))
        self.screen.blit(instr_text, (20, self.screen_height - 100))

        # Update the display
        pygame.display.flip()

    def play_pi_music(self, pi_digits: List[int], start_index: int = 0, max_notes: Optional[int] = None):
        """Play music based on Pi digits with visualization.

        Args:
            pi_digits: List of Pi digits
            start_index: Starting position in the digit sequence
            max_notes: Maximum number of notes to play (None for unlimited)
        """
        current_scale = self.major_scale
        note_duration = 0.3  # seconds
        pause_between_notes = 0.1  # seconds

        running = True
        paused = False
        position = start_index

        scale_options = {
            1: ("Pentatonic", self.pentatonic_scale),
            2: ("Major", self.major_scale),
            3: ("Chromatic", self.chromatic_scale)
        }
        current_scale_name = "Major"

        while running:
            if position >= len(pi_digits) or (max_notes is not None and position >= start_index + max_notes):
                # We've reached the end
                time.sleep(1)
                running = False
                break

            # Check for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        # Change scale
                        scale_num = event.key - pygame.K_0
                        current_scale_name, current_scale = scale_options[scale_num]
                    elif event.key == pygame.K_UP:
                        note_duration = max(0.1, note_duration - 0.05)
                    elif event.key == pygame.K_DOWN:
                        note_duration = min(1.0, note_duration + 0.05)

            if not paused:
                digit = pi_digits[position]
                frequency = self.get_frequency(digit, current_scale)

                # Generate and play sound
                sound = self.generate_sound(frequency, note_duration)
                sound.play()

                # Visualize
                self.draw_visualization(digit, position, pi_digits)

                # Wait for sound to finish
                time.sleep(note_duration + pause_between_notes)

                position += 1
            else:
                # When paused, just update the visualization and check for input
                self.draw_visualization(pi_digits[position], position, pi_digits)
                time.sleep(0.1)

        # Clean up
        pygame.quit()


def pi_symphony(pi_digits: List[int], max_notes: int = 100):
    """Play the Pi Symphony visualization.

    Args:
        pi_digits: List of Pi digits
        max_notes: Maximum number of notes to play
    """
    player = PiMusicPlayer()
    player.play_pi_music(pi_digits, max_notes=max_notes)


if __name__ == "__main__":
    from mpmath import mp
    mp.dps = 1000
    pi_digits = [int(d) for d in str(mp.pi)[2:]]
    pi_symphony(pi_digits)

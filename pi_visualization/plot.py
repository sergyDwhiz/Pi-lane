import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def plot_pi_digits(pi_digits: List[int], interactive: bool = True):
    """Plot the digits of Pi as points on a graph with improved visuals.

    Args:
        pi_digits: List of Pi digits to visualize
        interactive: Enable interactive features if True
    """
    # Create figure and axis with a dark background
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})

    # Limit to 1000 points for better performance
    display_digits = pi_digits[:1000]
    positions = np.arange(len(display_digits))

    # Main scatter plot
    scatter = ax1.scatter(positions, display_digits,
                         c=display_digits,
                         cmap='plasma',
                         s=50,
                         alpha=0.8,
                         edgecolors='white')

    # Add connecting lines for better visualization of pattern
    ax1.plot(positions, display_digits, 'white', alpha=0.2, linewidth=0.5)

    # Configure axes and titles
    ax1.set_title("Digits of π (Pi)", fontsize=16, color='white')
    ax1.set_xlabel("Position", fontsize=12)
    ax1.set_ylabel("Digit Value", fontsize=12)
    ax1.set_yticks(range(10))
    ax1.grid(True, linestyle='--', alpha=0.3)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label("Digit Value")

    # Add digit frequency histogram
    digit_counts = np.bincount(display_digits, minlength=10)
    digit_percentages = digit_counts / len(display_digits) * 100

    bars = ax2.bar(range(10), digit_percentages, color='turquoise')
    ax2.set_title("Digit Distribution", fontsize=14)
    ax2.set_xlabel("Digit")
    ax2.set_ylabel("Percentage (%)")
    ax2.set_xticks(range(10))

    # Add percentage labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{digit_percentages[i]:.1f}%',
                ha='center', va='bottom', rotation=0)

    # Add statistics as text
    stats_text = (
        f"Number of digits shown: {len(display_digits)}\n"
        f"Expected frequency per digit: 10.0%\n"
        f"Most common: {np.argmax(digit_counts)} ({digit_percentages[np.argmax(digit_counts)]:.1f}%)\n"
        f"Least common: {np.argmin(digit_counts)} ({digit_percentages[np.argmin(digit_counts)]:.1f}%)"
    )
    plt.figtext(0.02, 0.02, stats_text, fontsize=10)

    plt.tight_layout()
    plt.show()


def plot_pi_digit_heatmap(pi_digits: List[int], width: int = 40):
    """Plot the digits of Pi as a 2D heatmap.

    Args:
        pi_digits: List of Pi digits to visualize
        width: Width of the heatmap
    """
    # Limit to a reasonable number for display
    display_digits = pi_digits[:10000]

    # Reshape into a 2D array
    height = len(display_digits) // width
    display_digits = display_digits[:width * height]
    pi_array = np.array(display_digits).reshape(height, width)

    plt.figure(figsize=(12, 8))
    plt.imshow(pi_array, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Digit Value')
    plt.title('Pi Digits Heatmap')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from mpmath import mp
    mp.dps = 1000
    pi_digits = [int(d) for d in str(mp.pi)[2:]]
    plot_pi_digits(pi_digits)

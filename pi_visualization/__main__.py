"""Main entry point for Pi-lane visualizations."""

import argparse
from mpmath import mp
from typing import List

from pi_visualization.plot import plot_pi_digits
from pi_visualization.music import pi_symphony
from pi_visualization.animate import animate_pi_spiral
from pi_visualization.rolling_balls import run_rolling_balls


def get_pi_digits(precision: int = 1000) -> List[int]:
    """Get digits of Pi as a list of integers.

    Args:
        precision: Number of digits to calculate

    Returns:
        List of Pi digits
    """
    mp.dps = precision  # Set precision
    pi_str = str(mp.pi)[2:]  # Get digits after the decimal point
    return [int(digit) for digit in pi_str]


def main():
    """Run the selected Pi visualization."""
    parser = argparse.ArgumentParser(description='Visualize the digits of Pi.')
    parser.add_argument('--viz', type=str, default='rolling_balls',
                      choices=['rolling_balls', 'plot', 'music', 'spiral'],
                      help='Visualization to run')
    parser.add_argument('--precision', type=int, default=1000,
                      help='Number of Pi digits to calculate')

    args = parser.parse_args()

    digits = get_pi_digits(args.precision)

    if args.viz == 'rolling_balls':
        run_rolling_balls(digits)
    elif args.viz == 'plot':
        plot_pi_digits(digits)
    elif args.viz == 'music':
        pi_symphony(digits)
    elif args.viz == 'spiral':
        animate_pi_spiral(digits)


if __name__ == "__main__":
    main()

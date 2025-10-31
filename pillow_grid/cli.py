#!/usr/bin/env python3
"""
Command-line interface for pillow-grid
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from pillow_grid import Grid


def parse_labels(label_string: Optional[str]) -> Optional[List[str]]:
    """Parse comma-separated label string into list."""
    if not label_string:
        return None
    return [label.strip() for label in label_string.split(',')]


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='pillow-grid',
        description='Create image grids from command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a 2x3 grid from images
  pillow-grid img1.jpg img2.jpg img3.jpg img4.jpg img5.jpg img6.jpg -o grid.png --rows 2 --cols 3

  # Auto-sized grid with labels
  pillow-grid *.jpg -o output.png --labels "Cat,Dog,Bird,Fish"

  # Grid with row and column labels
  pillow-grid *.png -o grid.png --rows 2 --cols 2 \\
    --x-labels "Col 1,Col 2" --y-labels "Row 1,Row 2"

  # Custom spacing and font size
  pillow-grid img*.jpg -o grid.png --spacing 20 --font-size 16
        """
    )
    
    # Required arguments
    parser.add_argument(
        'images',
        nargs='+',
        help='Input image files (supports wildcards)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file path'
    )
    
    # Grid layout
    parser.add_argument(
        '--rows',
        type=int,
        default=None,
        help='Number of rows (auto-calculated if not specified)'
    )
    
    parser.add_argument(
        '--cols',
        type=int,
        default=None,
        help='Number of columns (auto-calculated if not specified)'
    )
    
    # Labels
    parser.add_argument(
        '--labels',
        type=str,
        default=None,
        help='Comma-separated labels for each image (e.g., "Cat,Dog,Bird")'
    )
    
    parser.add_argument(
        '--x-labels',
        type=str,
        default=None,
        dest='x_labels',
        help='Comma-separated column labels (e.g., "Col 1,Col 2")'
    )
    
    parser.add_argument(
        '--y-labels',
        type=str,
        default=None,
        dest='y_labels',
        help='Comma-separated row labels (e.g., "Row 1,Row 2")'
    )
    
    # Label styling
    parser.add_argument(
        '--labels-align',
        choices=['left', 'center', 'right'],
        default='center',
        dest='labels_align',
        help='Alignment for image labels (default: center)'
    )
    
    parser.add_argument(
        '--x-labels-align',
        choices=['left', 'center', 'right'],
        default='left',
        dest='x_labels_align',
        help='Alignment for column labels (default: left)'
    )
    
    parser.add_argument(
        '--y-labels-align',
        choices=['left', 'center', 'right'],
        default='left',
        dest='y_labels_align',
        help='Alignment for row labels (default: left)'
    )
    
    parser.add_argument(
        '--labels-max-lines',
        type=int,
        default=1,
        dest='labels_max_lines',
        help='Maximum lines for image labels (default: 1)'
    )
    
    parser.add_argument(
        '--x-labels-max-lines',
        type=int,
        default=2,
        dest='x_labels_max_lines',
        help='Maximum lines for column labels (default: 2)'
    )
    
    parser.add_argument(
        '--y-labels-max-lines',
        type=int,
        default=2,
        dest='y_labels_max_lines',
        help='Maximum lines for row labels (default: 2)'
    )
    
    # Styling
    parser.add_argument(
        '--spacing',
        type=int,
        default=5,
        help='Spacing between images in pixels (default: 5)'
    )
    
    parser.add_argument(
        '--font-size',
        type=int,
        default=12,
        dest='font_size',
        help='Font size for labels (default: 12)'
    )
    
    parser.add_argument(
        '--background-color',
        type=str,
        default='white',
        dest='background_color',
        help='Background color (default: white)'
    )
    
    parser.add_argument(
        '--font-path',
        type=str,
        default=None,
        dest='font_path',
        help='Path to custom font file'
    )
    
    # Options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.images:
        parser.error("At least one image file is required")
    
    # Check if image files exist
    missing_files = []
    for img_path in args.images:
        if not Path(img_path).exists():
            missing_files.append(img_path)
    
    if missing_files:
        print(f"Error: The following image files were not found:", file=sys.stderr)
        for f in missing_files:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)
    
    # Parse labels
    labels = parse_labels(args.labels)
    x_labels = parse_labels(args.x_labels)
    y_labels = parse_labels(args.y_labels)
    
    if args.verbose:
        print(f"Creating grid from {len(args.images)} images...")
        if args.rows or args.cols:
            print(f"Grid size: {args.rows or 'auto'}x{args.cols or 'auto'}")
        else:
            print("Grid size: auto")
        if labels:
            print(f"Image labels: {len(labels)}")
        if x_labels:
            print(f"Column labels: {len(x_labels)}")
        if y_labels:
            print(f"Row labels: {len(y_labels)}")
    
    try:
        # Create the grid
        grid = Grid(
            images=args.images,
            labels=labels,
            rows=args.rows,
            cols=args.cols,
            x_labels=x_labels,
            y_labels=y_labels,
            spacing=args.spacing,
            x_labels_max_lines=args.x_labels_max_lines,
            y_labels_max_lines=args.y_labels_max_lines,
            labels_max_lines=args.labels_max_lines,
            x_labels_align=args.x_labels_align,
            y_labels_align=args.y_labels_align,
            labels_align=args.labels_align,
            font_size=args.font_size,
            font_path=args.font_path,
            background_color=args.background_color
        )
        
        # Save the grid
        grid.save(args.output)
        
        if args.verbose:
            print(f"Grid saved to: {args.output}")
            print(f"Grid size: {grid.width}x{grid.height} pixels")
        else:
            print(f"Grid saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()


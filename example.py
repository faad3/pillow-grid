#!/usr/bin/env python3
"""
Example usage of the pillow-grid package
"""

from PIL import Image
import os
import sys

# Add the package to the path for testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pillow_grid import Grid


def create_sample_images():
    """Create some sample images for demonstration."""
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    images = []
    
    for i, color in enumerate(colors):
        # Create a colored rectangle with some text
        img = Image.new('RGB', (200, 150), color)
        images.append(img)
    
    return images


def create_different_sized_images():
    """Create images with different sizes for testing grid normalization."""
    images = []
    
    # Different sizes and colors
    configs = [
        (100, 100, 'red'),      # Square small
        (300, 150, 'green'),    # Wide rectangle
        (150, 300, 'blue'),     # Tall rectangle  
        (250, 200, 'yellow'),   # Medium rectangle
        (80, 120, 'purple'),    # Small portrait
        (400, 100, 'orange'),   # Very wide
    ]
    
    for width, height, color in configs:
        img = Image.new('RGB', (width, height), color)
        images.append(img)
    
    return images


def main():
    os.makedirs('output', exist_ok=True)

    print("Creating sample images...")
    images = create_sample_images()
    
    # Example 1: Basic 2x3 grid
    print("Creating basic 2x3 grid...")
    grid1 = Grid(images, rows=2, cols=3)
    grid1.save('output/example_basic_grid.png')
    print(f"Saved basic grid: {grid1.size}")
    
    # Example 2: Grid with only images and labels (no row/col labels)
    print("Creating grid with only image labels...")
    grid2 = Grid(
        images[:4],
        labels=['Image A', 'Image B', 'Image C', 'Image D'],
        rows=2,
        cols=2,
        spacing=10,
        font_size=14,
        labels_align='center',
    )
    grid2.save('output/example_only_labels_grid.png')
    print(f"Saved grid with only image labels: {grid2.size}")
    
    # Example 3: Grid with all types of labels
    print("Creating grid with all label types...")
    grid3 = Grid(
        images[:4], 
        labels=['Image A', 'Image B', 'Image C', 'Image D'],
        rows=2, 
        cols=2,
        x_labels=['Left Column' * 1, 'Right Column'],
        y_labels=['Top Row', 'Bottom Row'],
        spacing=5,
        font_size=12,
        x_labels_max_lines=2,
        y_labels_max_lines=2,
        labels_max_lines=1,
        labels_align='center',
    )
    grid3.save('output/example_all_labels_grid.png')
    print(f"Saved grid with all labels: {grid3.size}")
    
    # Example 4: Auto-sized grid
    print("Creating auto-sized grid...")
    grid4 = Grid(images, spacing=15)
    grid4.save('output/example_auto_grid.png')
    print(f"Saved auto grid: {grid4.size}")
    
    # Example 5: Custom background and styling
    print("Creating custom styled grid...")
    grid5 = Grid(
        images[:3],
        rows=1,
        cols=3,
        x_labels=['Image A', 'Image B', 'Image C'],
        spacing=25,
        background_color='lightgray',
        x_labels_max_lines=2,
        font_size=18
    )
    grid5.save('output/example_custom_grid.png')
    print(f"Saved custom grid: {grid5.size}")

    # Example 6: Grid with long text and different alignments
    print("Creating grid with long text and different alignments...")
    grid6 = Grid(
        images[:3],
        rows=2,
        cols=2,
        x_labels=['Its a very long text which we are going to use to test the grid', 'Image B '],
        y_labels=['Top Row ', 'Its a very long text which we are going to use to test the grid'],
        spacing=5,
        x_labels_max_lines=2,
        y_labels_max_lines=1,
        x_labels_align='left',    
        y_labels_align='left',
        font_size=18
    )
    grid6.save('output/example_long_text_grid.png')
    print(f"Saved long text grid: {grid6.size}")

    # Example 7: Different sized images with all label types
    print("Creating grid with different sized images and all label types...")
    different_images = create_different_sized_images()
    grid7 = Grid(
        different_images,
        labels=[
            'Small 100x100',
            'Wide 300x150', 
            'Tall 150x300',
            'Medium 250x200',
            'Portrait 80x120',
            'Very Wide 400x100'
        ],
        rows=2,
        cols=3,
        x_labels=['Small Square', 'Wide Rect', 'Tall Rect'],
        y_labels=['Row 1', 'Row 2'],
        spacing=5,  # Small spacing - will be automatically increased to fit labels
        x_labels_max_lines=2,
        y_labels_max_lines=1,
        labels_max_lines=1,
        x_labels_align='center',
        y_labels_align='center',
        labels_align='center',
        font_size=20,
        background_color='lightblue'
    )
    grid7.save('output/example_different_sizes_grid.png')
    print(f"Saved different sizes grid: {grid7.size}")
    print("Original image sizes:")
    for i, img in enumerate(different_images):
        print(f"  Image {i+1}: {img.size}")
    print(f"Note: Spacing was automatically adjusted from 5px to accommodate individual labels")
    
    print("\nAll examples created successfully!")
    print("Generated files:")
    print("- example_basic_grid.png")
    print("- example_only_labels_grid.png")
    print("- example_all_labels_grid.png") 
    print("- example_auto_grid.png")
    print("- example_custom_grid.png")
    print("- example_long_text_grid.png")
    print("- example_different_sizes_grid.png")


if __name__ == "__main__":
    main() 
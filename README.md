# Pillow Grid

A simple Python package for creating image grids with PIL (Pillow).

## Installation

```bash
pip install -e .
```

Or install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from pillow_grid import grid
from PIL import Image

# Create some example images or load from files
images = [
    Image.new('RGB', (100, 100), 'red'),
    Image.new('RGB', (100, 100), 'green'),
    Image.new('RGB', (100, 100), 'blue'),
    Image.new('RGB', (100, 100), 'yellow'),
]

# Create a 2x2 grid
my_grid = grid(images, rows=2, cols=2)

# Save the grid
my_grid.save('my_grid.png')

# Show the grid
my_grid.show()
```

### With Labels

```python
from pillow_grid import grid

# Create grid with labels
my_grid = grid(
    images=['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg'],
    rows=2, 
    cols=2,
    x_labels=['Column 1', 'Column 2'],
    y_labels=['Row 1', 'Row 2'],
    spacing=15,
    font_size=14,
    x_labels_max_lines=1,  # Allow up to 1 line for column labels
    y_labels_max_lines=2   # Allow up to 2 lines for row labels
)

my_grid.save('labeled_grid.png')
```

### With Custom Alignment

```python
from pillow_grid import grid

# Create grid with left-aligned x-labels and right-aligned y-labels
my_grid = grid(
    images=['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg'],
    rows=2, 
    cols=2,
    x_labels=['Long Column Label 1', 'Long Column Label 2'],
    y_labels=['Long Row Label 1', 'Long Row Label 2'],
    x_align='left',      # Left-align column labels
    y_align='right',     # Right-align row labels
    x_labels_max_lines=2,
    y_labels_max_lines=1
)

my_grid.save('aligned_grid.png')
```

### With Individual Image Labels

```python
from pillow_grid import grid

# Create grid with labels under each individual image
my_grid = grid(
    images=['cat.jpg', 'dog.jpg', 'bird.jpg', 'fish.jpg'],
    rows=2, 
    cols=2,
    all_labels=['Fluffy Cat', 'Golden Retriever', 'Blue Jay', 'Goldfish'],
    all_labels_max_lines=2,
    all_labels_align='center',
    spacing=5,  # Will be auto-adjusted to fit labels if needed
    font_size=12
)

my_grid.save('individual_labels_grid.png')
```

**Note:** When using `all_labels`, the spacing between rows is automatically adjusted to be at least `line_height * all_labels_max_lines` to ensure labels don't overlap with images below them.

### Auto-sizing

```python
from pillow_grid import grid

# Auto-calculate grid dimensions (roughly square)
images = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg']
my_grid = grid(images)  # Will create a 3x2 grid automatically

my_grid.save('auto_grid.png')
```

## Features

- **Automatic resizing**: Images are automatically resized to fit uniformly in the grid
- **Flexible layouts**: Specify rows and columns or let the package auto-calculate
- **Labels**: Add column and row labels
- **Customizable spacing**: Control spacing between images
- **PIL-like interface**: Familiar methods like `save()`, `show()`, `copy()`, etc.
- **Multiple input formats**: Accept PIL Images or file paths

## API Reference

### `grid(images, rows=None, cols=None, **kwargs)`

Create a Grid object from a list of images.

**Parameters:**
- `images`: List of PIL Image objects or file paths
- `rows`: Number of rows (auto-calculated if not provided)
- `cols`: Number of columns (auto-calculated if not provided)
- `x_labels`: Optional list of labels for columns
- `y_labels`: Optional list of labels for rows
- `all_labels`: Optional list of labels for each individual image (positioned under each image)
- `spacing`: Spacing between images in pixels (default: 5)
- `x_labels_max_lines`: Maximum number of lines for x-labels (default: 1)
- `y_labels_max_lines`: Maximum number of lines for y-labels (default: 1)
- `all_labels_max_lines`: Maximum number of lines for all_labels (default: 1)
- `x_labels_align`: Horizontal alignment for x-labels - 'left', 'center', 'right' (default: 'center')
- `y_labels_align`: Horizontal alignment for y-labels - 'left', 'center', 'right' (default: 'center')
- `all_labels_align`: Horizontal alignment for all_labels - 'left', 'center', 'right' (default: 'center')
- `font_size`: Size of label font (default: 12)
- `background_color`: Background color for the grid (default: "white")

### Grid Methods

- `save(filename, **kwargs)`: Save the grid image to a file
- `show()`: Display the grid image
- `copy()`: Return a copy of the grid image
- `resize(size, resample)`: Resize the grid image

### Grid Properties

- `size`: Size of the grid image as (width, height)
- `width`: Width of the grid image
- `height`: Height of the grid image
- `mode`: Color mode of the grid image

## License

MIT License 
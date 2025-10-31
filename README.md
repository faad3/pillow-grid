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

You can use `pillow-grid` either as a Python library or as a command-line tool.

### Command-Line Usage

After installation, you can use the `pillow-grid` command:

```bash
# Create a 2x3 grid from images
pillow-grid img1.jpg img2.jpg img3.jpg img4.jpg img5.jpg img6.jpg -o grid.png --rows 2 --cols 3

# Auto-sized grid with labels
pillow-grid *.jpg -o output.png --labels "Cat,Dog,Bird,Fish"

# Grid with row and column labels
pillow-grid *.png -o grid.png --rows 2 --cols 2 \
  --x-labels "Col 1,Col 2" --y-labels "Row 1,Row 2"

# Custom spacing and font size
pillow-grid img*.jpg -o grid.png --spacing 20 --font-size 16

# See all options
pillow-grid --help
```

### Python Library Usage

#### Basic Usage

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

### With Row and Column Labels

```python
from pillow_grid import grid

# Create grid with row and column labels
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

# Create grid with left-aligned x_labels and right-aligned y_labels
my_grid = grid(
    images=['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg'],
    rows=2, 
    cols=2,
    x_labels=['Long Column Label 1', 'Long Column Label 2'],
    y_labels=['Long Row Label 1', 'Long Row Label 2'],
    x_labels_align='left',      # Left-align column labels
    y_labels_align='right',     # Right-align row labels
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
    labels=['Fluffy Cat', 'Golden Retriever', 'Blue Jay', 'Goldfish'],
    rows=2, 
    cols=2,
    labels_max_lines=2,
    labels_align='center',
    spacing=5,  # Will be auto-adjusted to fit labels if needed
    font_size=12
)

my_grid.save('individual_labels_grid.png')
```

**Note:** When using `labels`, the spacing between rows is automatically adjusted to be at least `line_height * labels_max_lines` to ensure labels don't overlap with images below them. Note how `labels` is the second parameter after `images` for convenient use!

### Auto-sizing

```python
from pillow_grid import grid

# Auto-calculate grid dimensions (roughly square)
images = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg']
my_grid = grid(images)  # Will create a 3x2 grid automatically

my_grid.save('auto_grid.png')
```

## Features

- **Command-line tool**: Create grids directly from the terminal
- **Automatic resizing**: Images are automatically resized to fit uniformly in the grid
- **Flexible layouts**: Specify rows and columns or let the package auto-calculate
- **Labels**: Add column labels, row labels, and individual image labels
- **Customizable spacing**: Control spacing between images
- **PIL-like interface**: Familiar methods like `save()`, `show()`, `copy()`, etc.
- **Multiple input formats**: Accept PIL Images or file paths

## API Reference

### Command-Line Interface

```bash
pillow-grid [images...] -o OUTPUT [options]
```

**Required Arguments:**
- `images`: Input image files (supports multiple files)
- `-o, --output`: Output file path

**Grid Layout:**
- `--rows`: Number of rows (auto-calculated if not specified)
- `--cols`: Number of columns (auto-calculated if not specified)

**Labels:**
- `--labels`: Comma-separated labels for each image
- `--x-labels`: Comma-separated column labels
- `--y-labels`: Comma-separated row labels

**Label Styling:**
- `--labels-align {left,center,right}`: Image label alignment (default: center)
- `--x-labels-align {left,center,right}`: Column label alignment (default: left)
- `--y-labels-align {left,center,right}`: Row label alignment (default: left)
- `--labels-max-lines`: Maximum lines for image labels (default: 1)
- `--x-labels-max-lines`: Maximum lines for column labels (default: 2)
- `--y-labels-max-lines`: Maximum lines for row labels (default: 2)

**Styling:**
- `--spacing`: Spacing between images in pixels (default: 5)
- `--font-size`: Font size for labels (default: 12)
- `--background-color`: Background color (default: white)
- `--font-path`: Path to custom font file

**Other:**
- `-v, --verbose`: Verbose output
- `-h, --help`: Show help message

### Python API

#### `Grid(images, labels=None, rows=None, cols=None, **kwargs)`

Create a Grid object from a list of images.

**Parameters:**
- `images`: List of PIL Image objects or file paths
- `labels`: Optional list of labels for each individual image (positioned under each image)
- `rows`: Number of rows (auto-calculated if not provided)
- `cols`: Number of columns (auto-calculated if not provided)
- `x_labels`: Optional list of labels for columns
- `y_labels`: Optional list of labels for rows
- `spacing`: Spacing between images in pixels (default: 5)
- `x_labels_max_lines`: Maximum number of lines for x_labels (default: 2)
- `y_labels_max_lines`: Maximum number of lines for y_labels (default: 2)
- `labels_max_lines`: Maximum number of lines for labels (default: 1)
- `x_labels_align`: Horizontal alignment for x_labels - 'left', 'center', 'right' (default: 'left')
- `y_labels_align`: Horizontal alignment for y_labels - 'left', 'center', 'right' (default: 'left')
- `labels_align`: Horizontal alignment for labels - 'left', 'center', 'right' (default: 'center')
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
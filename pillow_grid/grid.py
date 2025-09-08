"""
Grid class for creating image grids with PIL
"""

from PIL import Image, ImageDraw, ImageFont
from typing import List, Union, Optional, Tuple
import os
import textwrap


class Grid:
    """
    A class for creating and managing image grids.
    
    Attributes:
        images: List of PIL Images
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        x_labels: Labels for columns
        y_labels: Labels for rows
        spacing: Spacing between images in pixels
        x_labels_max_lines: Maximum number of lines for x-labels
        y_labels_max_lines: Maximum number of lines for y-labels
        x_labels_align: Horizontal alignment for x-labels
        y_labels_align: Horizontal alignment for y-labels
        font_size: Size of label font
    """
    
    def __init__(self, images: List[Image.Image], rows: int, cols: int, 
                 x_labels: Optional[List[str]] = None, 
                 y_labels: Optional[List[str]] = None,
                 spacing: int = 5,
                 x_labels_max_lines: int = 2,
                 y_labels_max_lines: int = 2,
                 x_labels_align: str = 'left',
                 y_labels_align: str = 'left',
                 font_size: int = 12,
                 font_path: Optional[str] = None,
                 background_color: Union[str, Tuple[int, int, int]] = "white"):
        """
        Initialize a Grid object.
        
        Args:
            images: List of PIL Image objects
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            x_labels: Optional list of labels for columns
            y_labels: Optional list of labels for rows
            spacing: Spacing between images in pixels
            x_labels_max_lines: Maximum number of lines for x-labels (default: 1)
            y_labels_max_lines: Maximum number of lines for y-labels (default: 1)
            x_labels_align: Horizontal alignment for x-labels ('left', 'center', 'right')
            y_labels_align: Horizontal alignment for y-labels ('left', 'center', 'right')
            font_size: Size of label font
            font_path: Optional path to a specific font file
            background_color: Background color for the grid
        """
        self.images = images
        self.rows = rows
        self.cols = cols
        self.x_labels = x_labels or []
        self.y_labels = y_labels or []
        self.spacing = spacing
        self.x_labels_max_lines = x_labels_max_lines
        self.y_labels_max_lines = y_labels_max_lines
        self.x_labels_align = x_labels_align
        self.y_labels_align = y_labels_align
        self.font_size = font_size
        self.font_path = font_path
        self.background_color = background_color
        
        # Validate inputs
        if len(images) > rows * cols:
            raise ValueError(f"Too many images ({len(images)}) for grid size {rows}x{cols}")
        
        if self.x_labels and len(self.x_labels) > cols:
            raise ValueError(f"Too many x_labels ({len(self.x_labels)}) for {cols} columns")
            
        if self.y_labels and len(self.y_labels) > rows:
            raise ValueError(f"Too many y_labels ({len(self.y_labels)}) for {rows} rows")
        
        if x_labels_align not in ['left', 'center', 'right']:
            raise ValueError(f"x_labels_align must be 'left', 'center', or 'right', got '{x_labels_align}'")
            
        if y_labels_align not in ['left', 'center', 'right']:
            raise ValueError(f"y_labels_align must be 'left', 'center', or 'right', got '{y_labels_align}'")
        
        self._grid_image = None
        self._create_grid()
    
    def _get_uniform_size(self) -> Tuple[int, int]:
        """Calculate uniform size for all images based on the largest dimensions."""
        if not self.images:
            return (100, 100)
        
        max_width = max(img.width for img in self.images)
        max_height = max(img.height for img in self.images)
        return (max_width, max_height)
    
    def _resize_images(self, target_size: Tuple[int, int]) -> List[Image.Image]:
        """Resize all images to target size while maintaining aspect ratio."""
        resized_images = []
        for img in self.images:
            # Calculate scaling to fit within target size while maintaining aspect ratio
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]
            
            if img_ratio > target_ratio:
                # Image is wider, scale by width
                new_width = target_size[0]
                new_height = int(target_size[0] / img_ratio)
            else:
                # Image is taller, scale by height
                new_height = target_size[1]
                new_width = int(target_size[1] * img_ratio)
            
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a new image with target size and paste the resized image centered
            final_img = Image.new('RGB', target_size, self.background_color)
            paste_x = (target_size[0] - new_width) // 2
            paste_y = (target_size[1] - new_height) // 2
            final_img.paste(resized_img, (paste_x, paste_y))
            
            resized_images.append(final_img)
        
        return resized_images
    
    def _create_grid(self):
        """Create the grid image."""
        if not self.images:
            self._grid_image = Image.new('RGB', (100, 100), self.background_color)
            return
        
        # Get uniform size and resize images
        uniform_size = self._get_uniform_size()
        resized_images = self._resize_images(uniform_size)
        
        # Calculate dimensions
        img_width, img_height = uniform_size
        
        # Create temporary canvas and font to calculate label space needed
        temp_img = Image.new('RGB', (1, 1), self.background_color)
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Try to load a better font with fallbacks
        font = self._load_font(self.font_size)
        
        # Get font metrics
        ascent, descent = font.getmetrics()
        font_height = ascent + descent
        line_height = int(font_height * 1.05)  # Add 5% spacing between lines
        
        # Calculate actual space needed for x-labels
        x_label_space = 0
        if self.x_labels:
            # Use max_lines multiplied by font height
            x_label_space = self.x_labels_max_lines * line_height
        
        # Calculate actual space needed for y-labels
        y_label_space = 0
        if self.y_labels:
            # For rotated text, we need space equal to max_lines * font_height
            # This becomes the width after rotation
            y_label_space = self.y_labels_max_lines * line_height
        
        grid_width = (self.cols * img_width + (self.cols - 1) * self.spacing + 
                     y_label_space)
        grid_height = (self.rows * img_height + (self.rows - 1) * self.spacing + 
                      x_label_space)
        
        # Create the grid canvas
        self._grid_image = Image.new('RGB', (grid_width, grid_height), self.background_color)
        draw = ImageDraw.Draw(self._grid_image)
        
        # Place images
        for i, img in enumerate(resized_images):
            if i >= self.rows * self.cols:
                break
                
            row = i // self.cols
            col = i % self.cols
            
            x = col * (img_width + self.spacing) + y_label_space
            y = row * (img_height + self.spacing) + x_label_space
            
            self._grid_image.paste(img, (x, y))
        
        # Add x labels (column labels) - wrapped to fit in specified lines
        if self.x_labels:
            for i, label in enumerate(self.x_labels):
                if i < self.cols:
                    # Wrap text to fit within max_lines
                    wrapped_lines = self._wrap_text_to_lines(label, font, img_width, self.x_labels_max_lines, draw)
                    
                    if wrapped_lines:  # Only draw if we have text
                        # Calculate the column bounds (offset by y_label_space)
                        col_start_x = i * (img_width + self.spacing) + y_label_space
                        
                        # Calculate starting y position to center the text block
                        total_text_height = len(wrapped_lines) * line_height
                        y_start = (x_label_space - total_text_height) // 2
                        
                        # Draw each line with specified alignment
                        for line_idx, line in enumerate(wrapped_lines):
                            if line:  # Only draw non-empty lines
                                text_width = draw.textlength(line, font=font)
                                x_offset = self._get_text_x_position(text_width, img_width, self.x_labels_align)
                                x = col_start_x + x_offset
                                y = y_start + line_idx * line_height
                                draw.text((x, y), line, fill="black", font=font)
        
        # Add y labels (row labels) - rotated 90 degrees, wrapped to fit in specified lines
        if self.y_labels:
            for i, label in enumerate(self.y_labels):
                if i < self.rows:
                    # Calculate dimensions for text rendering (before rotation)
                    text_width = img_height  # Will become height after rotation
                    text_height = self.y_labels_max_lines * line_height  # Will become width after rotation
                    
                    # Create temporary image for text rendering
                    temp_img = Image.new("RGB", (text_width, text_height), color=self.background_color)
                    temp_draw = ImageDraw.Draw(temp_img)
                    
                    # Wrap text to fit within max_lines
                    wrapped_lines = self._wrap_text_to_lines(label, font, text_width, self.y_labels_max_lines, temp_draw)
                    
                    if wrapped_lines:  # Only draw if we have text
                        # Calculate starting position to center the text block
                        total_text_height = len(wrapped_lines) * line_height
                        y_start = (text_height - total_text_height) // 2
                        
                        # Draw each line with specified alignment on temporary image
                        for line_idx, line in enumerate(wrapped_lines):
                            if line:  # Only draw non-empty lines
                                line_width = temp_draw.textlength(line, font=font)
                                x_offset = self._get_text_x_position(line_width, text_width, self.y_labels_align)
                                y = y_start + line_idx * line_height
                                temp_draw.text((x_offset, y), line, fill="black", font=font)
                        
                        # Rotate 90 degrees counterclockwise
                        rotated_temp = temp_img.rotate(90, expand=True)
                        
                        # Calculate the center y position for this row
                        row_start_y = i * (img_height + self.spacing) + x_label_space
                        
                        # Calculate paste position to center with row
                        paste_x = max(0, (y_label_space - rotated_temp.width) // 2)
                        paste_y = row_start_y + (img_height - rotated_temp.height) // 2
                        
                        # Ensure within bounds
                        paste_y = max(x_label_space, min(paste_y, 
                                      self._grid_image.height - rotated_temp.height))
                        
                        # Paste the rotated text
                        self._grid_image.paste(rotated_temp, (paste_x, paste_y))
    
    def _wrap_text_to_lines(self, text: str, font, max_width: int, max_lines: int, draw) -> List[str]:
        """
        Wrap text to fit within the specified number of lines and width.
        Text is first wrapped by words, then by characters if needed.
        
        Args:
            text: Text to wrap
            font: Font object
            max_width: Maximum width in pixels per line
            max_lines: Maximum number of lines allowed
            draw: ImageDraw object for text measurement
            
        Returns:
            List of text lines that fit within the constraints
        """
        def text_length(text_line):
            return draw.textlength(text_line, font=font)
        
        def fit_text_in_width(text_to_fit, available_width, add_ellipsis=False):
            """Fit text in available width, cutting by characters if needed."""
            if text_length(text_to_fit) <= available_width:
                return text_to_fit
            
            ellipsis = "..." if add_ellipsis else ""
            ellipsis_width = text_length(ellipsis) if add_ellipsis else 0
            
            if ellipsis_width >= available_width:
                return "" if add_ellipsis else text_to_fit[:1]  # At least try one character
            
            effective_width = available_width - ellipsis_width
            
            # Binary search for best character fit
            left, right = 0, len(text_to_fit)
            best_length = 0
            
            while left <= right:
                mid = (left + right) // 2
                substring = text_to_fit[:mid]
                
                if text_length(substring) <= effective_width:
                    best_length = mid
                    left = mid + 1
                else:
                    right = mid - 1
            
            result = text_to_fit[:best_length]
            return result + ellipsis if add_ellipsis else result
        
        if not text.strip():
            return [text] if text else []
        
        lines = []
        remaining_text = text
        
        for line_num in range(max_lines):
            if not remaining_text.strip():
                break
            
            # If this is the last allowed line and there's more text after, we need ellipsis
            is_last_line = (line_num == max_lines - 1)
            
            if is_last_line:
                # On the last line, check if we need ellipsis
                if text_length(remaining_text) <= max_width:
                    # Text fits completely
                    lines.append(remaining_text)
                else:
                    # Need to truncate with ellipsis
                    fitted_text = fit_text_in_width(remaining_text, max_width, add_ellipsis=True)
                    if fitted_text:
                        lines.append(fitted_text)
                break
            
            # Try to fit as much as possible on this line
            # First try word-by-word wrapping
            words = remaining_text.split()
            if not words:
                break
            
            current_line = ""
            words_used = 0
            
            for i, word in enumerate(words):
                test_line = current_line + (" " if current_line else "") + word
                
                if text_length(test_line) <= max_width:
                    current_line = test_line
                    words_used = i + 1
                else:
                    break
            
            if words_used == 0:
                # Even the first word doesn't fit, cut it by characters
                first_word = words[0]
                fitted_word = fit_text_in_width(first_word, max_width, add_ellipsis=False)
                if fitted_word:
                    lines.append(fitted_word)
                    # Remove the fitted part from the first word
                    remaining_first_word = first_word[len(fitted_word):]
                    remaining_text = remaining_first_word + " " + " ".join(words[1:]) if len(words) > 1 else remaining_first_word
                else:
                    break  # Can't fit anything
            else:
                # We fit some words
                lines.append(current_line)
                remaining_text = " ".join(words[words_used:])
        
        return lines
    
    def _get_text_x_position(self, text_width: int, container_width: int, alignment: str) -> int:
        """
        Calculate x position for text based on alignment.
        
        Args:
            text_width: Width of the text in pixels
            container_width: Width of the container in pixels
            alignment: 'left', 'center', or 'right'
            
        Returns:
            X position for the text
        """
        if alignment == 'left':
            return 0
        elif alignment == 'center':
            return (container_width - text_width) // 2
        elif alignment == 'right':
            return container_width - text_width
        else:
            return (container_width - text_width) // 2  # Default to center
    
    def _load_font(self, size: int):
        """
        Load the best available font with multiple fallbacks.
        """
        # If custom font path is provided, try that first
        if self.font_path:
            try:
                return ImageFont.truetype(self.font_path, size)
            except (OSError, IOError):
                pass  # Fall back to default fonts
        
        # Try bundled Inter font first
        try:
            bundled_font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'inter-regular.ttf')
            if os.path.exists(bundled_font_path):
                return ImageFont.truetype(bundled_font_path, size)
        except (OSError, IOError):
            pass
        
        # List of font candidates in order of preference
        font_candidates = [
            # Modern system fonts
            "arial.ttf",
            "Arial.ttf",
            "helvetica.ttf",
            "Helvetica.ttf",
            "calibri.ttf",
            "Calibri.ttf",
            
            # Linux system fonts
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/arial.ttf",
            
            # macOS system fonts
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttf", 
            "/Library/Fonts/Arial.ttf",
            
            # Windows system fonts
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
        
        # Try each font candidate
        for font_path in font_candidates:
            try:
                font = ImageFont.truetype(font_path, size)
                return font
            except (OSError, IOError):
                continue
        
        # If no TrueType font works, fall back to default
        try:
            return ImageFont.load_default(size)
        except:
            # Final fallback for older PIL versions
            return ImageFont.load_default()
    
    def save(self, filename: str, **kwargs):
        """
        Save the grid image to a file.
        
        Args:
            filename: Path to save the image
            **kwargs: Additional arguments passed to PIL Image.save()
        """
        if self._grid_image is None:
            raise ValueError("Grid image not created")
        
        self._grid_image.save(filename, **kwargs)
    
    def show(self):
        """Display the grid image."""
        if self._grid_image is None:
            raise ValueError("Grid image not created")
        
        self._grid_image.show()
    
    def copy(self):
        """Return a copy of the grid image."""
        if self._grid_image is None:
            raise ValueError("Grid image not created")
        
        return self._grid_image.copy()
    
    def resize(self, size: Tuple[int, int], resample=Image.Resampling.LANCZOS):
        """
        Resize the grid image.
        
        Args:
            size: New size as (width, height)
            resample: Resampling algorithm
            
        Returns:
            New Grid object with resized image
        """
        if self._grid_image is None:
            raise ValueError("Grid image not created")
        
        resized_img = self._grid_image.resize(size, resample)
        
        # Create a new Grid object with the resized image
        new_grid = Grid([resized_img], 1, 1)
        new_grid._grid_image = resized_img
        return new_grid
    
    @property
    def size(self) -> Tuple[int, int]:
        """Get the size of the grid image."""
        if self._grid_image is None:
            return (0, 0)
        return self._grid_image.size
    
    @property
    def width(self) -> int:
        """Get the width of the grid image."""
        return self.size[0]
    
    @property
    def height(self) -> int:
        """Get the height of the grid image."""
        return self.size[1]
    
    @property
    def mode(self) -> str:
        """Get the mode of the grid image."""
        if self._grid_image is None:
            return "RGB"
        return self._grid_image.mode


def grid(images: List[Union[Image.Image, str]], 
         rows: Optional[int] = None, 
         cols: Optional[int] = None,
         x_labels: Optional[List[str]] = None,
         y_labels: Optional[List[str]] = None,
         spacing: int = 5,
         x_labels_max_lines: int = 1,
         y_labels_max_lines: int = 1,
         x_labels_align: str = 'center',
         y_labels_align: str = 'center',
         font_size: int = 12,
         font_path: Optional[str] = None,
         background_color: Union[str, Tuple[int, int, int]] = "white") -> Grid:
    """
    Create a Grid object from a list of images.
    
    Args:
        images: List of PIL Image objects or file paths
        rows: Number of rows (auto-calculated if not provided)
        cols: Number of columns (auto-calculated if not provided)
        x_labels: Optional list of labels for columns
        y_labels: Optional list of labels for rows
        spacing: Spacing between images in pixels
        x_labels_max_lines: Maximum number of lines for x-labels (default: 1)
        y_labels_max_lines: Maximum number of lines for y-labels (default: 1)
        x_labels_align: Horizontal alignment for x-labels ('left', 'center', 'right')
        y_labels_align: Horizontal alignment for y-labels ('left', 'center', 'right')
        font_size: Size of label font
        font_path: Optional path to a specific font file
        background_color: Background color for the grid
    
    Returns:
        Grid object
    """
    # Convert string paths to Image objects
    pil_images = []
    for img in images:
        if isinstance(img, str):
            if os.path.exists(img):
                pil_images.append(Image.open(img))
            else:
                raise FileNotFoundError(f"Image file not found: {img}")
        elif isinstance(img, Image.Image):
            pil_images.append(img)
        else:
            raise TypeError(f"Expected PIL Image or file path, got {type(img)}")
    
    # Auto-calculate rows and cols if not provided
    n_images = len(pil_images)
    if rows is None and cols is None:
        # Default to roughly square grid
        cols = int(n_images ** 0.5)
        rows = (n_images + cols - 1) // cols
    elif rows is None:
        rows = (n_images + cols - 1) // cols
    elif cols is None:
        cols = (n_images + rows - 1) // rows
    
    return Grid(pil_images, rows, cols, x_labels, y_labels, 
                spacing, x_labels_max_lines, y_labels_max_lines, x_labels_align, y_labels_align, font_size, font_path, background_color) 
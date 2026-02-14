#!/usr/bin/env python3
"""
Render Sudoku puzzle images using Python PIL/Pillow.
Replaces ImageMagick for simpler visualization.
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Constants for rendering
CELL_SIZE = 36  # Size of each cell in pixels
GRID_SIZE = 9  # 9x9 Sudoku grid
IMAGE_SIZE = CELL_SIZE * GRID_SIZE  # 324x324 pixels
FONT_SIZE = 28
GRID_LINE_WIDTH = 2
THICK_LINE_WIDTH = 4

def parse_sudoku_line(line):
    """
    Parse a linear Sudoku puzzle (81 characters) into a 9x9 grid.
    Replace '0' with empty string for display.
    """
    line = line.strip()
    if len(line) != 81:
        raise ValueError(f"Invalid puzzle format: expected 81 characters, got {len(line)}")
    
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            char = line[i * GRID_SIZE + j]
            # Replace 0 with empty string
            row.append('' if char == '0' else char)
        grid.append(row)
    
    return grid

def draw_sudoku_grid(draw, image_size):
    """Draw the Sudoku grid lines."""
    # Draw thin lines for cells
    for i in range(GRID_SIZE + 1):
        pos = i * CELL_SIZE
        # Determine line width (thicker for 3x3 box boundaries)
        width = THICK_LINE_WIDTH if i % 3 == 0 else GRID_LINE_WIDTH
        # Horizontal line
        draw.line([(0, pos), (image_size, pos)], fill='black', width=width)
        # Vertical line
        draw.line([(pos, 0), (pos, image_size)], fill='black', width=width)

def render_sudoku(puzzle_line, output_file, grid_image_path=None):
    """
    Render a Sudoku puzzle as an image.
    
    Args:
        puzzle_line: 81-character string representing the puzzle
        output_file: Path to save the output image
        grid_image_path: Optional path to a background grid image
    """
    # Parse the puzzle
    grid = parse_sudoku_line(puzzle_line)
    
    # Create a white background image
    img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        # Try common font paths
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            '/System/Library/Fonts/Courier.dfont',
            'C:\\Windows\\Fonts\\cour.ttf',
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, FONT_SIZE)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    # Draw the numbers
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j]:  # If cell is not empty
                # Calculate text position (centered in cell)
                x = j * CELL_SIZE + CELL_SIZE // 2
                y = i * CELL_SIZE + CELL_SIZE // 2
                
                # Draw text centered
                text = grid[i][j]
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                text_x = x - text_width // 2
                text_y = y - text_height // 2
                
                draw.text((text_x, text_y), text, fill='black', font=font)
    
    # Draw the grid lines on top
    draw_sudoku_grid(draw, IMAGE_SIZE)
    
    # If a background grid image is provided, blend with it
    if grid_image_path and os.path.exists(grid_image_path):
        try:
            # Load the background grid
            bg_grid = Image.open(grid_image_path)
            # Resize to match if needed
            if bg_grid.size != (IMAGE_SIZE, IMAGE_SIZE):
                bg_grid = bg_grid.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
            # Convert to RGB if needed
            if bg_grid.mode != 'RGB':
                bg_grid = bg_grid.convert('RGB')
            
            # Blend the images (50/50 blend like ImageMagick's -average)
            img = Image.blend(bg_grid, img, alpha=0.5)
        except Exception as e:
            print(f"Warning: Could not blend with background grid: {e}")
    
    # Save the image
    img.save(output_file)
    print(f"Rendered Sudoku to {output_file}")

def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python3 render_sudoku.py <puzzle_line> <output_file> [grid_image]")
        print("  puzzle_line: 81-character string representing the Sudoku puzzle")
        print("  output_file: Path to save the output PNG image")
        print("  grid_image: Optional background grid image to blend with")
        sys.exit(1)
    
    puzzle_line = sys.argv[1]
    output_file = sys.argv[2]
    grid_image = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        render_sudoku(puzzle_line, output_file, grid_image)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import os

# Configuration
EVENTS_FILE = "events.txt"           # Path to text file with events
BACKGROUNDS_DIR = "./background"     # Directory containing background images
OUTPUT_DIR = "bingo_cards"          # Output directory for cards
NUM_CARDS = 40                      # Number of cards to generate
FONT_SIZE = 30                      # Font size for event text
TEXT_COLOR = (255, 255, 255)        # Text color (white)
GRID_COLOR = (0, 0, 0)              # Grid line color
GRID_WIDTH = 3                      # Grid line width
PADDING = 15                        # Padding around text in pixels
BACKGROUND_OPACITY = 0.50           # 50% opacity

# Card sizing configuration
CARD_WIDTH = 800                    # Fixed width for all cards
CARD_HEIGHT = 900                   # Fixed height for all cards (header + bingo grid)
BINGO_REGION_HEIGHT = 700           # Height of the bingo grid region
HEADER_HEIGHT = CARD_HEIGHT - BINGO_REGION_HEIGHT  # Height of the header

# Card appearance
CARD_TITLE = "Sobrado en Festas 2025"     # Title text for all cards
TITLE_FONT_SIZE = 40                # Font size for card title
NUMBER_FONT_SIZE = 30               # Font size for card number

# 10 high-contrast colors that work well with white text
CARD_COLORS = [
    (70, 95, 120),    # Dark slate blue
    (139, 0, 0),      # Dark red
    (0, 100, 0),      # Dark green
    (72, 61, 139),    # Dark slate gray
    (85, 107, 47),    # Dark olive green
    (139, 69, 19),    # Saddle brown
    (47, 79, 79),     # Dark slate gray
    (100, 0, 100),    # Dark magenta
    (0, 0, 139),      # Dark blue
    (153, 50, 204)    # Dark orchid
]

def get_random_card_color():
    """Return a random color from the predefined palette that contrasts with white text."""
    return random.choice(CARD_COLORS)

def get_background_images(directory):
    """Get list of all image files in the specified directory."""
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = []
    try:
        for file in os.listdir(directory):
            if file.lower().endswith(valid_extensions):
                images.append(os.path.join(directory, file))
        return images
    except FileNotFoundError:
        print(f"Error: Background directory not found at {directory}")
        return []

def load_events(file_path):
    """Load events from a text file, one event per line."""
    events = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Strip whitespace and skip empty lines
                stripped = line.strip()
                if stripped:
                    events.append(stripped)
        return events
    except FileNotFoundError:
        print(f"Error: Events file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading events file: {str(e)}")
        return []

def generate_unique_cards(events, num_cards, card_size=9):
    """Generate unique sets of events for bingo cards."""
    if len(events) < card_size:
        raise ValueError(f"Not enough events to create unique cards. Need {card_size} but only have {len(events)}")
    
    unique_cards = set()
    max_attempts = 1000
    attempts = 0
    
    while len(unique_cards) < num_cards and attempts < max_attempts:
        card = tuple(sorted(random.sample(events, card_size)))
        if card not in unique_cards:
            unique_cards.add(card)
        attempts += 1
    
    if len(unique_cards) < num_cards:
        print(f"Warning: Only generated {len(unique_cards)} unique cards out of {num_cards} requested")
    
    return [list(card) for card in unique_cards]

def wrap_text(text, font, max_width):
    """Wrap text to fit within specified width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = font.getlength(test_line)
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_bingo_card(events, bg_image_path, output_path, card_number, card_color):
    """Create a bingo card image with events overlaid on background and a header."""
    # Prepare the background image
    try:
        bg_image = Image.open(bg_image_path).convert("RGBA")
        # Resize background to match bingo region size while maintaining aspect ratio
        bg_image = ImageOps.fit(bg_image, (CARD_WIDTH, BINGO_REGION_HEIGHT), method=Image.LANCZOS)
    except IOError:
        print(f"Error: Could not load background image at {bg_image_path}")
        return
    
    # Create a solid background for the bingo region with the random color
    bingo_base = Image.new('RGBA', (CARD_WIDTH, BINGO_REGION_HEIGHT), card_color)
    
    # Composite the semi-transparent background over the colored base
    bg_image = adjust_opacity(bg_image, BACKGROUND_OPACITY)
    bingo_base.alpha_composite(bg_image)
    draw = ImageDraw.Draw(bingo_base)
    
    # Try to load fonts
    try:
        event_font = ImageFont.truetype("arial.ttf", FONT_SIZE)
        title_font = ImageFont.truetype("arial.ttf", TITLE_FONT_SIZE)
        number_font = ImageFont.truetype("arial.ttf", NUMBER_FONT_SIZE)
    except IOError:
        try:
            event_font = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE)
            title_font = ImageFont.truetype("DejaVuSans.ttf", TITLE_FONT_SIZE)
            number_font = ImageFont.truetype("DejaVuSans.ttf", NUMBER_FONT_SIZE)
        except IOError:
            event_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            number_font = ImageFont.load_default()
            print("Using default font - consider installing arial.ttf for better results")
    
    # Calculate cell dimensions
    cell_width = CARD_WIDTH // 3
    cell_height = BINGO_REGION_HEIGHT // 3
    
    # Draw grid lines
    for i in range(1, 3):
        # Vertical lines
        x = i * cell_width
        draw.line([(x, 0), (x, BINGO_REGION_HEIGHT)], fill=GRID_COLOR, width=GRID_WIDTH)
        # Horizontal lines
        y = i * cell_height
        draw.line([(0, y), (CARD_WIDTH, y)], fill=GRID_COLOR, width=GRID_WIDTH)
    
    # Add events to the bingo grid
    for i in range(9):
        row = i // 3
        col = i % 3
        event = events[i]
        
        # Calculate cell boundaries
        x0 = col * cell_width
        y0 = row * cell_height
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        
        # Wrap text to fit in cell
        max_text_width = cell_width - 2 * PADDING
        wrapped_lines = wrap_text(event, event_font, max_text_width)
        
        # Calculate total text height
        line_heights = []
        for line in wrapped_lines:
            bbox = event_font.getbbox(line)
            line_heights.append(bbox[3] - bbox[1])
        total_text_height = sum(line_heights)
        
        # Calculate starting Y position for vertical centering
        y_pos = y0 + (cell_height - total_text_height) // 2
        
        # Draw each line of text
        for line, line_height in zip(wrapped_lines, line_heights):
            text_bbox = event_font.getbbox(line)
            text_width = text_bbox[2] - text_bbox[0]
            x_pos = x0 + (cell_width - text_width) // 2
            draw.text((x_pos, y_pos), line, fill=TEXT_COLOR, font=event_font)
            y_pos += line_height
    
    # Create the header region with the same card color
    header = Image.new('RGBA', (CARD_WIDTH, HEADER_HEIGHT), card_color)
    header_draw = ImageDraw.Draw(header)
    
    # Add title to header
    title_bbox = title_font.getbbox(CARD_TITLE)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (CARD_WIDTH - title_width) // 2
    header_draw.text((title_x, 20), CARD_TITLE, fill=TEXT_COLOR, font=title_font)
    header_draw.text(((CARD_WIDTH - number_width) // 2), )

    # Add card number to header
    number_text = f"Cartón #{card_number}"
    number_bbox = number_font.getbbox(number_text)
    number_width = number_bbox[2] - number_bbox[0]
    number_x = (CARD_WIDTH - number_width) // 2
    header_draw.text((number_x, 60), number_text, fill=TEXT_COLOR, font=number_font)
    
    # Combine header and bingo region
    final_card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT))
    final_card.paste(header, (0, 0))
    final_card.paste(bingo_base.convert('RGB'), (0, HEADER_HEIGHT))
    
    # Save the final card
    final_card.save(output_path, "PNG")

def adjust_opacity(img, opacity):
    """Adjust image opacity to specified level (0.0-1.0)."""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * opacity)
    img.putalpha(alpha)
    return img

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load events from file
    events = load_events(EVENTS_FILE)
    if not events:
        print("No events loaded. Exiting.")
        return
    
    # Check we have enough events
    if len(events) < 9:
        print(f"Error: Need at least 9 events, but only {len(events)} were provided")
        return
    
    # Get available background images
    background_images = get_background_images(BACKGROUNDS_DIR)
    if not background_images:
        print("No background images found. Exiting.")
        return
    
    # Generate unique cards
    try:
        cards = generate_unique_cards(events, NUM_CARDS)
    except ValueError as e:
        print(str(e))
        return
    
    # Create each bingo card with unique color and background
    used_colors = set()
    for i, card_events in enumerate(cards):
        # Get a unique color for each card
        while True:
            card_color = get_random_card_color()
            if card_color not in used_colors or len(used_colors) >= len(CARD_COLORS):
                break
        used_colors.add(card_color)
        
        # Select a random background image (may repeat if more cards than backgrounds)
        bg_image_path = random.choice(background_images)
        
        random.shuffle(card_events)  # Randomize event positions in the card
        output_path = os.path.join(OUTPUT_DIR, f"bingo_card_{i+1}.png")
        create_bingo_card(card_events, bg_image_path, output_path, i+1, card_color)
        print(f"Created: {output_path} with color {card_color} and background {os.path.basename(bg_image_path)}")
    
    print(f"\nSuccessfully created {len(cards)} bingo cards in '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()
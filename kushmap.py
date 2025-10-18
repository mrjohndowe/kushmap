import pygame
import sys

# === Constants ===
WIDTH, HEIGHT = 1000, 800
GRID_SIZE = 50
GRID_OFFSET_X, GRID_OFFSET_Y = 250, 150
MIN_ZOOM, MAX_ZOOM = 0.2, 5.0
FPS = 60

# === Colors ===
PALETTE = {
    'background': (11, 13, 11),
    'grid_line': (40, 60, 40),
    'buildable': (30, 50, 30),
    'sink': (43, 148, 59),
    'door': (43, 148, 59),
    'selected': (60, 100, 60),
    'preview_valid': (100, 255, 100, 150),
    'preview_invalid': (255, 100, 100, 150),
    'text': (43, 148, 59),
    'regular_text': (200, 220, 200),
    'button': (30, 70, 30),
    'button_hover': (50, 90, 50),
    'instructions_bg': (20, 40, 20, 200),
    'sink_door_text': (255, 255, 255),
    'stats_bg': (20, 40, 20, 220)
}

# === Furniture Data ===
FURNITURE = {
    'Storage': {
        'small_storage': ((110, 65, 40), "Small Storage", 2, 1, 30),
        'medium_storage': ((110, 65, 40), "Medium Storage", 3, 1, 45),
        'large_storage': ((110, 65, 40), "Large Storage", 4, 1, 60),
        'display_cabinet': ((80, 50, 20), "Display Cabinet", 3, 2, 250),  # slightly lighter/varnished?
    },
    'Furniture': {
        'bed': ((190, 60, 60), "Bed", 3, 5, 150),
        'coffee_table': ((80, 50, 20), "Coffee Table", 4, 2, 120),
        'woodensquare_table': ((100, 60, 25), "Wooden Table", 2, 2, 50),
        'metalsquare_table': ((130, 150, 180), "Metal Table", 2, 2, 150),
        'floor_lamp': ((255, 235, 180), "Lamp", 1, 1, 25),
        'tv': ((50, 50, 50), "TV", 4, 2, 300),
        
    },
    'Stations': {
        'packaging_station': ((100, 100, 100), "Packaging Station", 4, 2, 100),
        'packaging_station_mk2': ((160, 160, 160), "Packaging Station MK2", 4, 2, 750),
        'mixing_station': ((40, 90, 60), "Mixing Station", 4, 2, 500),
        'mixing_station_mk2': ((70, 130, 100), "Mixing Station MK2", 4, 2, 2000),
    },
    'Grow': {
        'grow_tent': ((100, 150, 100), "Grow Tent", 2, 2, 100),
        'suspension_rack': ((150, 200, 150), "Suspension Rack", 2, 2, 40),
        'halogen_light': ((150, 200, 150), "Halogen Light", 2, 2, 40),
        'led_light': ((150, 200, 150), "LED Light", 2, 2, 80),
        'full_spectrum_light': ((150, 200, 150), "Full Spectrum Light", 2, 2, 200),
        'plastic_pot': ((150, 100, 50), "Plastic Pot", 2, 2, 20),
        'moisture_pot': ((150, 100, 50), "Moisture Pot", 2, 2, 50),
        'air_pot': ((150, 100, 50), "Air Pot", 2, 2, 120),
    }
}

# === Layouts ===
HOUSES = {
    'motel': [
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', None, None],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', None, None],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', None, None],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', None, None],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', None, None],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '🚪', '🚪', '🚪', '■', '■', '■', '■', '■', '■'],
        ['■', '🚪', '🚪', '🚪', '■', '■', '■', '■', '■', '■']
    ],
    'sweatshop': [
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        [None, None, None, None, None, None, None, None, '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■', '■'],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', '■', '■', '■', '■', '■', '■', '■', '🚪', '🚪', '🚪'],
        ['■', '■', '■', '■', '■', '■', '⛲', '⛲', '■', '■', '■', '■', '■', '■', '■', '🚪', '🚪', '🚪']
    ],
    'bungalow': [
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", None, None, None, None, None, None, None, None, None, None, None, None],
        ["■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", "■", "■", "🚪", "🚪", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["⛲", "⛲", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["⛲", "⛲", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["⛲", "⛲", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"],
        ["⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "⛲", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■", "■"]
    ]
}

WALLS = {
    'bungalow': {
        'edges': set(
            # Horizontal wall between top and bottom left rooms (except doors at 5,6)
            ((x, 11), 'h') for x in range(0, 12) if x not in (5, 6)
        ).union(
            # Vertical wall between bottom-left and bottom-right using pattern
            ((11, y), 'v') for y in [12, 15, 16, 17, 18, 19, 20, 23]
        )
    }
}

def get_furniture_data(key):
    for group in FURNITURE.values():
        if key in group:
            return group[key]
    return None

# === Initialize pygame ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption("Home Designer")
font = pygame.font.SysFont('Arial', 16)
title_font = pygame.font.SysFont('Arial', 24, bold=True)
button_font = pygame.font.SysFont('Arial', 20, bold=True)
inventory_font = pygame.font.SysFont('Arial', 14)

# === Load logo ===
try:
    logo_image = pygame.image.load("kushmap.png").convert_alpha()
    logo_image = pygame.transform.smoothscale(logo_image, (512, 256))
except pygame.error as e:
    print("Failed to load kushmap.png:", e)
    logo_image = None


# === Global State ===
current_house = None
placed_items = {}
selected_item = None
rotation = 0
game_state = "house_selection"
zoom_level = 1.0
camera_offset = [0, 0]
show_stats = False
open_folders = {category: False for category in FURNITURE}
inventory_scroll = 0


def screen_to_grid(pos):
    x, y = pos
    return (
        (x - camera_offset[0] - GRID_OFFSET_X) / (GRID_SIZE * zoom_level),
        (y - camera_offset[1] - GRID_OFFSET_Y) / (GRID_SIZE * zoom_level)
    )


def get_house_dimensions():
    if current_house and HOUSES[current_house]:
        return len(HOUSES[current_house][0]), len(HOUSES[current_house])
    return 0, 0


def draw_button(rect, label, hover=False):
    color = PALETTE['button_hover'] if hover else PALETTE['button']
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, PALETTE['text'], rect, 2, border_radius=8)
    text = button_font.render(label, True, PALETTE['regular_text'])
    screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))


def draw_house_selection():
    screen.fill(PALETTE['background'])

    width = screen.get_width()
    height = screen.get_height()

    # Draw logo if it exists
    if logo_image:
        logo_rect = logo_image.get_rect(center=(width // 2, 180))
        screen.blit(logo_image, logo_rect)
        title_y = logo_rect.bottom + 40
    else:
        title_y = 70  # fallback if no logo

    # Title
    title = title_font.render("Select a House Layout", True, PALETTE['text'])
    screen.blit(title, (width // 2 - title.get_width() // 2, title_y))

    # Main buttons
    button_width = 300
    button_height = 80
    spacing = 10
    start_y = title_y + 50  # move buttons down to give room

    motel_rect = pygame.Rect(width // 2 - button_width // 2, start_y, button_width, button_height)
    sweatshop_rect = pygame.Rect(width // 2 - button_width // 2, start_y + button_height + spacing, button_width, button_height)
    bungalow_rect = pygame.Rect(width // 2 - button_width // 2, start_y + 2 * (button_height + spacing), button_width, button_height)

    # Quit button (smaller, near bottom)
    quit_button_width = 150
    quit_button_height = 50
    quit_rect = pygame.Rect(
        width // 2 - quit_button_width // 2,
        height - quit_button_height - 50,
        quit_button_width,
        quit_button_height
    )

    mouse_pos = pygame.mouse.get_pos()

    draw_button(motel_rect, "Motel", motel_rect.collidepoint(mouse_pos))
    draw_button(sweatshop_rect, "Sweatshop", sweatshop_rect.collidepoint(mouse_pos))
    draw_button(bungalow_rect, "Bungalow", bungalow_rect.collidepoint(mouse_pos))
    draw_button(quit_rect, "Quit", quit_rect.collidepoint(mouse_pos))

    return motel_rect, sweatshop_rect, bungalow_rect, quit_rect



def draw_grid():
    house_width, house_height = get_house_dimensions()
    for y in range(house_height):
        for x in range(house_width):
            cell = HOUSES[current_house][y][x]

            tile_x = round(GRID_OFFSET_X + x * GRID_SIZE * zoom_level + camera_offset[0])
            tile_y = round(GRID_OFFSET_Y + y * GRID_SIZE * zoom_level + camera_offset[1])
            tile_w = max(1, round(GRID_SIZE * zoom_level))
            tile_h = max(1, round(GRID_SIZE * zoom_level))

            rect = pygame.Rect(tile_x, tile_y, tile_w, tile_h)

            if cell == '■':
                overdraw_rect = rect.inflate(2, 2)
                pygame.draw.rect(screen, PALETTE['buildable'], overdraw_rect)
                pygame.draw.rect(screen, PALETTE['grid_line'], rect, 1)

def draw_wall_edges():
    if current_house not in WALLS:
        return

    wall_edges = WALLS[current_house].get('edges', set())
    wall_color = (20, 30, 20)

    for (x, y), direction in wall_edges:
        x_px = round(GRID_OFFSET_X + x * GRID_SIZE * zoom_level + camera_offset[0])
        y_px = round(GRID_OFFSET_Y + y * GRID_SIZE * zoom_level + camera_offset[1])
        if direction == 'h':
            pygame.draw.line(screen, wall_color,
                             (x_px, y_px + GRID_SIZE * zoom_level),
                             (x_px + GRID_SIZE * zoom_level, y_px + GRID_SIZE * zoom_level),
                             width=5)
        elif direction == 'v':
            pygame.draw.line(screen, wall_color,
                             (x_px + GRID_SIZE * zoom_level, y_px),
                             (x_px + GRID_SIZE * zoom_level, y_px + GRID_SIZE * zoom_level),
                             width=5)

def draw_special_zones():
    house_width, house_height = get_house_dimensions()
    drawn = set()

    for y in range(house_height):
        for x in range(house_width):
            if (x, y) in drawn:
                continue

            cell = HOUSES[current_house][y][x]
            if cell not in ['⛲', '🚪']:
                continue

            # Start building a block of same-type cells
            color = PALETTE['sink'] if cell == '⛲' else PALETTE['door']
            width = 1

            # Expand horizontally
            while x + width < house_width and HOUSES[current_house][y][x + width] == cell:
                width += 1

            # Expand vertically as long as the entire row matches
            height = 1
            valid = True
            while y + height < house_height and valid:
                for dx in range(width):
                    if HOUSES[current_house][y + height][x + dx] != cell:
                        valid = False
                        break
                if valid:
                    height += 1

            # Mark all covered tiles so we don't draw them again
            for dy in range(height):
                for dx in range(width):
                    drawn.add((x + dx, y + dy))

            # Calculate screen coords
            draw_x = round(GRID_OFFSET_X + x * GRID_SIZE * zoom_level + camera_offset[0])
            draw_y = round(GRID_OFFSET_Y + y * GRID_SIZE * zoom_level + camera_offset[1])
            draw_w = max(1, round(width * GRID_SIZE * zoom_level))
            draw_h = max(1, round(height * GRID_SIZE * zoom_level))

            # Draw the tile
            pygame.draw.rect(screen, color, pygame.Rect(draw_x, draw_y, draw_w, draw_h))

            # Only show label if it's a door
            if cell == '🚪':
                label_text = "DOOR"

                # Create a bold font that adjusts to tile size
                font_size = max(12, min(draw_w // 4, draw_h // 4))
                bold_font = pygame.font.SysFont('Arial', font_size, bold=True)
                label = bold_font.render(label_text, True, PALETTE['sink_door_text'])

                # Position the text centered inside the tile
                text_x = draw_x + (draw_w // 2 - label.get_width() // 2)
                text_y = draw_y + (draw_h // 2 - label.get_height() // 2)
                screen.blit(label, (text_x, text_y))

def draw_inventory():
    inventory_width = 220
    screen_height = screen.get_height()

    pygame.draw.rect(screen, (30, 60, 30), (0, 0, inventory_width, screen_height))
    pygame.draw.line(screen, PALETTE['text'], (inventory_width, 0), (inventory_width, screen_height), 2)


    y_offset = 30 + inventory_scroll  # ⬅️ apply scroll offset
    item_height = 70

    for category, items in FURNITURE.items():
        header = inventory_font.render(category, True, PALETTE['text'])
        screen.blit(header, (30, y_offset))
        y_offset += 25

        if open_folders.get(category, True):
            for item_key, (color, name, w, h, _) in items.items():
                item_rect = pygame.Rect(30, y_offset, inventory_width - 20, item_height - 10)
                pygame.draw.rect(screen, PALETTE['selected'] if selected_item == item_key else (40, 80, 40), item_rect, border_radius=4)
                pygame.draw.rect(screen, PALETTE['text'], item_rect, 1, border_radius=4)
                pygame.draw.rect(screen, color, (35, y_offset + 5, 50, 50), border_radius=4)
                text = inventory_font.render(name, True, PALETTE['regular_text'])
                screen.blit(text, (95, y_offset + 10))
                y_offset += item_height

def draw_stats():
    stats_surface = pygame.Surface((200, 140), pygame.SRCALPHA)
    stats_surface.fill(PALETTE['stats_bg'])
    screen.blit(stats_surface, (WIDTH - 220, 70))

    total_price = sum(get_furniture_data(item)[4] for (item, _) in placed_items.values())

    lines = [
        f"Items placed: {len(placed_items)}",
        f"Zoom: {zoom_level:.2f}",
        f"Selected: {get_furniture_data(selected_item)[1] if selected_item else 'None'}",
        f"Total Value: ${total_price}"
    ]

    for i, line in enumerate(lines):
        text = inventory_font.render(line, True, PALETTE['regular_text'])
        screen.blit(text, (WIDTH - 210, 80 + i * 20))


def draw_preview():
    if not selected_item or not current_house:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = screen_to_grid((mouse_x, mouse_y))
    house_width, house_height = get_house_dimensions()

    if not (0 <= int(grid_x) < house_width and 0 <= int(grid_y) < house_height):
        return

    w, h = get_furniture_data(selected_item)[2:4]
    if rotation % 2:
        w, h = h, w

    top_left_x = int(grid_x - w // 2)
    top_left_y = int(grid_y - h // 2)

    def is_occupied(x, y):
        for (px, py), (item, rot) in placed_items.items():
            iw, ih = get_furniture_data(item)[2:4]
            if rot % 2:
                iw, ih = ih, iw
            if px <= x < px + iw and py <= y < py + ih:
                return True
        return False

    valid = all(
        0 <= top_left_x + dx < house_width and
        0 <= top_left_y + dy < house_height and
        HOUSES[current_house][top_left_y + dy][top_left_x + dx] == '■' and
        not is_occupied(top_left_x + dx, top_left_y + dy)
        for dx in range(w) for dy in range(h)
    ) and not crosses_wall(top_left_x, top_left_y, w, h, rotation)

    color = PALETTE['preview_valid'] if valid else PALETTE['preview_invalid']

    preview_w = max(1, round(w * GRID_SIZE * zoom_level))
    preview_h = max(1, round(h * GRID_SIZE * zoom_level))
    preview_surface = pygame.Surface((preview_w, preview_h), pygame.SRCALPHA)
    pygame.draw.rect(preview_surface, color, (0, 0, preview_w, preview_h))

    draw_x = round(GRID_OFFSET_X + top_left_x * GRID_SIZE * zoom_level + camera_offset[0])
    draw_y = round(GRID_OFFSET_Y + top_left_y * GRID_SIZE * zoom_level + camera_offset[1])
    screen.blit(preview_surface, (draw_x, draw_y))


def draw_placed_items():
    for (x, y), (item, rot) in placed_items.items():
        color, name, w, h, _ = get_furniture_data(item)
        if rot % 2:
            w, h = h, w

        tile_x = round(GRID_OFFSET_X + x * GRID_SIZE * zoom_level + camera_offset[0])
        tile_y = round(GRID_OFFSET_Y + y * GRID_SIZE * zoom_level + camera_offset[1])
        tile_w = max(1, round(w * GRID_SIZE * zoom_level))
        tile_h = max(1, round(h * GRID_SIZE * zoom_level))

        rect = pygame.Rect(tile_x, tile_y, tile_w, tile_h)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, PALETTE['grid_line'], rect, 2)

        # Create a bold font that adjusts to the tile size
        font_size = max(12, min(tile_w // 4, tile_h // 4))  # Adjust font size based on the tile's size
        bold_font = pygame.font.SysFont('Arial', font_size, bold=True)

        # Render the item name as bold
        label = bold_font.render(name, True, PALETTE['sink_door_text'])

        # Position the text centered inside the item rect
        text_x = rect.centerx - label.get_width() // 2
        text_y = rect.centery - label.get_height() // 2
        screen.blit(label, (text_x, text_y))

def find_item_at(grid_x, grid_y):
    for (px, py), (item, rot) in placed_items.items():
        w, h = get_furniture_data(item)[2:4]
        if rot % 2:
            w, h = h, w
        if px <= grid_x < px + w and py <= grid_y < py + h:
            return (px, py)
    return None


def crosses_wall(x, y, w, h, rot):
    if current_house not in WALLS:
        return False

    wall_edges = WALLS[current_house].get('edges', set())

    for dx in range(w):
        for dy in range(h):
            cx = x + dx
            cy = y + dy

            if dy < h - 1 and ((cx, cy), 'h') in wall_edges:
                return True

            if dx < w - 1 and ((cx, cy), 'v') in wall_edges:
                return True

    return False


# === Main Game Loop ===
clock = pygame.time.Clock()
running = True
panning = False
last_mouse_pos = (0, 0)

while running:
    screen.fill(PALETTE['background'])
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                rotation = (rotation - 1) % 4
            elif event.key == pygame.K_e:
                rotation = (rotation + 1) % 4

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if game_state == "house_selection":
                    motel_rect, sweatshop_rect, bungalow_rect, quit_rect = draw_house_selection()

                    if motel_rect.collidepoint(mouse_pos):
                        current_house = 'motel'
                        game_state = "decorating"
                    elif sweatshop_rect.collidepoint(mouse_pos):
                        current_house = 'sweatshop'
                        game_state = "decorating"
                    elif bungalow_rect.collidepoint(mouse_pos):
                        current_house = 'bungalow'
                        game_state = "decorating"
                    elif quit_rect.collidepoint(mouse_pos):
                        running = False

                elif game_state == "decorating":
                    stats_button_rect = pygame.Rect(screen.get_width() - 120, 20, 100, 40)
                    back_button_rect = pygame.Rect(WIDTH - 230, 20, 100, 40)

                    if back_button_rect.collidepoint(mouse_pos):
                        game_state = "house_selection"
                        current_house = None
                        placed_items.clear()
                        selected_item = None
                        rotation = 0
                        show_stats = False
                        continue

                    if stats_button_rect.collidepoint(mouse_pos):
                        show_stats = not show_stats
                        continue

                    y_offset = 30 + inventory_scroll
                    item_height = 70
                    found = False  # Did we click a folder header or an item?

                    # First: check for folder header clicks
                    for category, items in FURNITURE.items():
                        header_rect = pygame.Rect(30, y_offset, 180, 25)
                        if header_rect.collidepoint(mouse_pos):
                            open_folders[category] = not open_folders.get(category, True)
                            found = True
                            break
                        y_offset += 25
                        if open_folders.get(category, True):
                            y_offset += item_height * len(items)

                    # Then: only check item clicks if no folder was clicked
                    if not found:
                        # Proceed to check for item clicks and placement
                        y_offset = 30 + inventory_scroll
                        for category, items in FURNITURE.items():
                            y_offset += 25
                            if open_folders.get(category, True):
                                for item_key in items:
                                    item_rect = pygame.Rect(30, y_offset, 180, 60)
                                    if item_rect.collidepoint(mouse_pos):
                                        selected_item = item_key
                                        found = True
                                        break
                                    y_offset += item_height
                            if found:
                                break

                            # Only try placing if not clicking inventory
                        if selected_item is not None:
        # ⬅️ this is where your placement logic (with debug prints) goes

                            grid_x, grid_y = map(int, screen_to_grid(mouse_pos))

                            item_data = get_furniture_data(selected_item)
                            if not item_data:
                                continue  # Skip if item not found

                            w, h = item_data[2:4]
                            if rotation % 2:
                                w, h = h, w

                            top_left = (grid_x - w // 2, grid_y - h // 2)
                            house_w, house_h = get_house_dimensions()

                            def is_occupied(x, y):
                                for (px, py), (item, rot) in placed_items.items():
                                    iw, ih = get_furniture_data(item)[2:4]
                                    if rot % 2:
                                        iw, ih = ih, iw
                                    if px <= x < px + iw and py <= y < py + ih:
                                        return True
                                return False

                            if all(
                                0 <= top_left[0] + dx < house_w and
                                0 <= top_left[1] + dy < house_h and
                                HOUSES[current_house][top_left[1] + dy][top_left[0] + dx] == '■' and
                                not is_occupied(top_left[0] + dx, top_left[1] + dy)
                                for dx in range(w) for dy in range(h)
                            ) and not crosses_wall(top_left[0], top_left[1], w, h, rotation):
                                placed_items[top_left] = (selected_item, rotation)

            elif event.button == 3:  # Right click to delete
                if game_state == "decorating":
                    grid_x, grid_y = map(int, screen_to_grid(mouse_pos))
                    to_remove = find_item_at(grid_x, grid_y)
                    if to_remove:
                        del placed_items[to_remove]


            elif event.button == 2:
                panning = True
                last_mouse_pos = event.pos

            elif event.button in [4, 5]:  # Scroll up or down
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # === Zooming ===
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_before = screen_to_grid((mouse_x, mouse_y))

                    zoom_amount = 1.1 if event.button == 4 else 1 / 1.1
                    new_zoom = zoom_level * zoom_amount
                    zoom_level = max(MIN_ZOOM, min(MAX_ZOOM, new_zoom))

                    grid_after = screen_to_grid((mouse_x, mouse_y))
                    dx = (grid_after[0] - grid_before[0]) * GRID_SIZE * zoom_level
                    dy = (grid_after[1] - grid_before[1]) * GRID_SIZE * zoom_level
                    camera_offset[0] += dx
                    camera_offset[1] += dy
                else:
                    # === Inventory scroll ===
                    scroll_amount = 30
                    if event.button == 4:  # Scroll up
                        inventory_scroll = min(inventory_scroll + scroll_amount, 0)
                    elif event.button == 5:  # Scroll down
                        inventory_scroll -= scroll_amount

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                panning = False

        elif event.type == pygame.MOUSEMOTION:
            if panning:
                dx, dy = event.rel
                camera_offset[0] += dx
                camera_offset[1] += dy

    if game_state == "house_selection":
        motel_rect, sweatshop_rect, bungalow_rect, quit_rect = draw_house_selection()
    else:
        draw_grid()
        draw_wall_edges()
        draw_special_zones()
        draw_placed_items()
        draw_inventory()
        draw_preview()

    if game_state == "decorating":
        screen_width = screen.get_width()
        stats_button_rect = pygame.Rect(screen_width - 120, 20, 100, 40)
        back_button_rect = pygame.Rect(screen_width - 230, 20, 100, 40)

        draw_button(back_button_rect, "Back", back_button_rect.collidepoint(mouse_pos))
        draw_button(stats_button_rect, "Stats", stats_button_rect.collidepoint(mouse_pos))

        if show_stats:
            draw_stats()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

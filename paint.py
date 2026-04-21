import pygame
import sys
import math

pygame.init()

# -------------------- SETTINGS --------------------
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 18)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 170, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
PURPLE = (150, 0, 200)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Tool names
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

current_tool = TOOL_BRUSH
current_color = BLACK
brush_size = 6

drawing = False
start_pos = None
last_pos = None

color_buttons = [
    (BLACK, pygame.Rect(20, 20, 30, 30)),
    (RED, pygame.Rect(60, 20, 30, 30)),
    (GREEN, pygame.Rect(100, 20, 30, 30)),
    (BLUE, pygame.Rect(140, 20, 30, 30)),
    (YELLOW, pygame.Rect(180, 20, 30, 30)),
    (PURPLE, pygame.Rect(220, 20, 30, 30)),
]

tool_buttons = {
    TOOL_BRUSH: pygame.Rect(300, 15, 100, 40),
    TOOL_RECT: pygame.Rect(420, 15, 100, 40),
    TOOL_CIRCLE: pygame.Rect(540, 15, 100, 40),
    TOOL_ERASER: pygame.Rect(660, 15, 100, 40),
}


# -------------------- FUNCTIONS --------------------
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw color buttons
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Draw tool buttons
    for tool, rect in tool_buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 12, rect.y + 10))

    # Show current tool and color
    info = font.render(f"Tool: {current_tool}   Brush size: {brush_size}", True, BLACK)
    screen.blit(info, (800, 20))


def draw_on_canvas():
    # Draw the saved canvas
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Preview shape while drawing
    if drawing and start_pos and current_tool in (TOOL_RECT, TOOL_CIRCLE):
        current_mouse = pygame.mouse.get_pos()
        preview_surface = canvas.copy()

        x1, y1 = start_pos
        x2, y2 = current_mouse[0], current_mouse[1] - TOOLBAR_HEIGHT

        if current_tool == TOOL_RECT:
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(preview_surface, current_color, rect, 2)

        elif current_tool == TOOL_CIRCLE:
            radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            pygame.draw.circle(preview_surface, current_color, (x1, y1), radius, 2)

        screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))


def draw_line(surface, color, start, end, width):
    # Draw continuous line for brush/eraser
    pygame.draw.line(surface, color, start, end, width)
    pygame.draw.circle(surface, color, end, width // 2)


# -------------------- MAIN LOOP --------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Click on toolbar
            if my <= TOOLBAR_HEIGHT:
                # Check colors
                for color, rect in color_buttons:
                    if rect.collidepoint(mx, my):
                        current_color = color

                # Check tools
                for tool, rect in tool_buttons.items():
                    if rect.collidepoint(mx, my):
                        current_tool = tool

            else:
                # Click on drawing area
                drawing = True
                start_pos = (mx, my - TOOLBAR_HEIGHT)
                last_pos = start_pos

                if current_tool == TOOL_BRUSH:
                    pygame.draw.circle(canvas, current_color, start_pos, brush_size // 2)

                elif current_tool == TOOL_ERASER:
                    pygame.draw.circle(canvas, WHITE, start_pos, brush_size)

        # Mouse motion
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my > TOOLBAR_HEIGHT:
                current_pos = (mx, my - TOOLBAR_HEIGHT)

                if current_tool == TOOL_BRUSH:
                    draw_line(canvas, current_color, last_pos, current_pos, brush_size)

                elif current_tool == TOOL_ERASER:
                    draw_line(canvas, WHITE, last_pos, current_pos, brush_size * 2)

                last_pos = current_pos

        # Mouse button up
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            mx, my = event.pos

            if my > TOOLBAR_HEIGHT:
                end_pos = (mx, my - TOOLBAR_HEIGHT)

                # Draw final rectangle
                if current_tool == TOOL_RECT and start_pos:
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(canvas, current_color, rect, 2)

                # Draw final circle
                elif current_tool == TOOL_CIRCLE and start_pos:
                    radius = int(math.sqrt(
                        (end_pos[0] - start_pos[0]) ** 2 +
                        (end_pos[1] - start_pos[1]) ** 2
                    ))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

            drawing = False
            start_pos = None
            last_pos = None

        # Change brush size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size += 2
            elif event.key == pygame.K_DOWN and brush_size > 2:
                brush_size -= 2

    screen.fill(WHITE)
    draw_toolbar()
    draw_on_canvas()

    pygame.display.update()
    clock.tick(60)
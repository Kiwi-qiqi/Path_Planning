import pygame
import sys

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BG_COLOR = (255, 255, 255)

def draw_button(label, x, y, w, h, color):
    font = pygame.font.Font(None, 24)
    text = font.render(label, True, (0, 0, 0))
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)
    screen.blit(text, (x + w // 2 - text.get_width() // 2, y + h // 2 - text.get_height() // 2))
    return rect

pygame.init()
pygame.display.set_caption("Pygame Interactive Interface")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

button1_rect = draw_button("Button 1", 50, 50, 100, 50, (255, 0, 0))
button2_rect = draw_button("Button 2", 50, 120, 100, 50, (0, 255, 0))

window_pos = (200, 50)
window_surface = pygame.Surface((200, 200))
window_surface.fill((200, 200, 200))
screen.blit(window_surface, window_pos)

button_pos = {
    "Option 1": (210, 70),
    "Option 2": (210, 140),
    "Option 3": (210, 210),
}

button_offsets = {
    "Option 3": (10, 10),
    "Option 4": (10, 70),
    "Option 5": (10, 130)
}
button3_rect = draw_button("Option 1", *button_pos["Option 1"], 100, 50, (0, 0, 255))
button4_rect = draw_button("Option 2", *button_pos["Option 2"], 100, 50, (255, 255, 0))
button5_rect = draw_button("Option 3", *button_pos["Option 3"], 100, 50, (255, 0, 255))

dragging_window = False
dragging_button = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button1_rect.collidepoint(event.pos):
                    print("Button 1 clicked")
                elif button2_rect.collidepoint(event.pos):
                    print("Button 2 clicked")
                elif button3_rect.collidepoint(event.pos):
                    print("Option 1 selected")
                elif button4_rect.collidepoint(event.pos):
                    print("Option 2 selected")
                elif button5_rect.collidepoint(event.pos):
                    print("Option 3 selected")
                elif event.pos[0] >= window_pos[0] and event.pos[0] <= window_pos[0] + window_surface.get_width() and event.pos[1] >= window_pos[1] and event.pos[1] <= window_pos[1] + window_surface.get_height():
                    dragging_window = True
                    mouse_offset = (event.pos[0] - window_pos[0], event.pos[1] - window_pos[1])
                elif event.pos[0] >= button_pos["Option 1"][0] and event.pos[0] <= button_pos["Option 1"][0] + 100 and event.pos[1] >= button_pos["Option 1"][1] and event.pos[1] <= button_pos["Option 1"][1] + 50:
                    dragging_button = "Option 1"
                    mouse_offset = (event.pos[0] - button_pos["Option 1"][0], event.pos[1] - button_pos["Option 1"][1])
                elif event.pos[0] >= button_pos["Option 2"][0] and event.pos[0] <= button_pos["Option 2"][0] + 100 and event.pos[1] >= button_pos["Option 2"][1] and event.pos[1] <= button_pos["Option 2"][1] + 50:
                    dragging_button = "Option 2"
                    mouse_offset = (event.pos[0] - button_pos["Option 2"][0], event.pos[1] - button_pos["Option 2"][1])
                elif event.pos[0] >= button_pos["Option 3"][0] and event.pos[0] <= button_pos["Option 3"][0] + 100 and event.pos[1] >= button_pos["Option 3"][1] and event.pos[1] <= button_pos["Option 3"][1] + 50:
                    dragging_button = "Option 3"
                    mouse_offset = (event.pos[0] - button_pos["Option 3"][0], event.pos[1] - button_pos["Option 3"][1])
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_window = False
                dragging_button = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_window:
                window_pos = (event.pos[0] - mouse_offset[0], event.pos[1] - mouse_offset[1])
                # 更新按钮的位置
                for button, offset in button_offsets.items():
                    button_pos[button] = (window_pos[0] + offset[0], window_pos[1] + offset[1])

            elif dragging_button:
                button_pos[dragging_button] = (event.pos[0] - mouse_offset[0], event.pos[1] - mouse_offset[1])

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, (30, 30, 30), button1_rect, 2)
    pygame.draw.rect(screen, (50, 50, 50), button2_rect, 2)

    window_surface.fill((200, 200, 200))
    pygame.draw.rect(window_surface, (0, 0, 0), button3_rect, 2)
    pygame.draw.rect(window_surface, (0, 0, 0), button4_rect, 2)
    pygame.draw.rect(window_surface, (0, 0, 0), button5_rect, 2)
    screen.blit(window_surface, window_pos)

    for label, pos in button_pos.items():
        draw_button(label, *pos, 100, 50, (255, 255, 255))

    pygame.display.flip()

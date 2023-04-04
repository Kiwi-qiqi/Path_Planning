import pygame


pygame.init()

# Create buttons
button1 = pygame.Surface((100, 50))
button1.fill((255, 255, 255))
button1_rect = button1.get_rect(center=(150, 150))

button2 = pygame.Surface((100, 50))
button2.fill((255, 255, 255))
button2_rect = button2.get_rect(center=(350, 150))

screen = pygame.display.set_mode((500, 500))
running = False

def main_loop():
    num = 0
    while True:
        if running:
            print(num)
            num += 1
            if num > 100:
                break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1_rect.collidepoint(event.pos):
                        running = True
                        main_loop()
                    elif button2_rect.collidepoint(event.pos):
                        running = False

while True:
    screen.fill((0, 0, 0))
    
    # Draw buttons
    screen.blit(button1, button1_rect)
    screen.blit(button2, button2_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button1_rect.collidepoint(event.pos):
                    running = True
                    main_loop()
                elif button2_rect.collidepoint(event.pos):
                    running = False
    
    pygame.display.update()

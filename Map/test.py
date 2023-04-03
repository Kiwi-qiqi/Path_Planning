import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

start_button = pygame.Rect(50, 50, 100, 50)
pause_button = pygame.Rect(200, 50, 100, 50)
continue_button = pygame.Rect(200, 50, 150, 50)
cancel_button = pygame.Rect(350, 50, 100, 50)

is_running = False
is_paused = False
counter = 0
stored_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                is_running = True
            elif pause_button.collidepoint(event.pos):
                is_paused = True
                stored_counter = counter
                start_button.text = 'Continue'
                pause_button.text = 'Cancel'
            elif continue_button.collidepoint(event.pos):
                is_paused = False
                start_button.text = 'Start'
                pause_button.text = 'Pause'
            elif cancel_button.collidepoint(event.pos):
                is_running = False
                is_paused = False
                counter = 0
                stored_counter = 0
                start_button.text = 'Start'
                pause_button.text = 'Pause'
                
    win.fill((255, 255, 255))
    
    if is_running:
        for i in range(counter, 101):
            counter = i
            text = font.render(str(i), True, (0, 0, 0))
            win.blit(text, (200, 200))
            pygame.display.update()
            clock.tick(10)
            if is_paused:
                break
    
    start_button.text_surface = font.render(start_button.text, True, (0, 0, 0))
    pygame.draw.rect(win, (0, 255, 0), start_button)
    win.blit(start_button.text_surface, (start_button.x + 10, start_button.y + 10))
    
    pause_button.text_surface = font.render(pause_button.text, True, (0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), pause_button)
    win.blit(pause_button.text_surface, (pause_button.x + 10, pause_button.y + 10))
    
    cancel_button.text_surface = font.render('Cancel', True, (0, 0, 0))
    pygame.draw.rect(win, (0, 0, 255), cancel_button)
    win.blit(cancel_button.text_surface, (cancel_button.x + 10, cancel_button.y + 10))
    
    pygame.display.update()
    clock.tick(60)

import pygame
from pygame.locals import *
import random

def main():
    pygame.init()

    # create a surface on screen that has the size of the computer screen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Our Game")
    
    font1 = pygame.font.SysFont('freesanbold.ttf', 50)
    words=["Charles", "Charle", "Charlie"]
    texts=[]
    rectangles=[]
    
    for x in range(0, 100):
        newText=font1.render(random.choice(words), True, (0, 0, 255))
        newRect=newText.get_rect()
        newRect.center=(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
        texts.append(newText)
        rectangles.append(newRect)
        
    running = True
    
    while running:
        # event handling, gets all event from the event queue
        for i in range(0, len(texts)):
            screen.blit(texts[i], rectangles[i])
        pygame.display.update()
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False





if __name__=="__main__":
    main()
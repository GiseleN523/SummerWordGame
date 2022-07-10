import pygame
from pygame import Rect

from utils import GameEvent


def start_screen(screen, game_input, fonts, common_gui):

    scr_width = screen.get_width()
    scr_height = screen.get_height()

    pygame.draw.rect(screen, (220, 220, 255), common_gui.popup)
    str1="HOW TO PLAY"
    txt1=fonts.header.render(str1, True, (0, 0, 0))
    txt1_rect=txt1.get_rect()
    txt1_rect.center=(screen.get_width() /2, 100+(txt1_rect.height/2))
    screen.blit(txt1, txt1_rect)
    ypos=100+txt1_rect.height+50
    
    str2="Here are the instructions for how to play. They explain how the game works and everything you need to know to play the game."
    str2+=" "
    while " " in str2: # wrap words when they don't fit on a line
        substr=""
        txt=fonts.paragraph.render(substr, True, (0, 0, 0))
        txt_rect=txt.get_rect()
        while txt_rect.width < scr_width - 150 - 50 and " " in str2:
            substr=substr+str2[:str2.index(" ")+1]
            str2=str2[str2.index(" ")+1:]
            txt=fonts.paragraph.render(substr, True, (0, 0, 0))
            txt_rect=txt.get_rect()
        txt_rect.center=(scr_width/2, ypos+(txt_rect.height/2))
        screen.blit(txt, txt_rect)
        ypos+=txt_rect.height/2+15
        
    play_button=fonts.button.render("PLAY", True, (0, 0, 0))
    play_button_rect=play_button.get_rect()
    play_button_rect.center=(scr_width/2, scr_height-75-40-(play_button_rect.height/2))
    play_button_background=Rect(play_button_rect.center[0]-(play_button_rect.width/2)-30, play_button_rect.center[1]-(play_button_rect.height/2)-15, play_button_rect.width+60, play_button_rect.height+30)
    
    if game_input.mouse_x>=play_button_background.left \
        and game_input.mouse_x<=play_button_background.right \
        and game_input.mouse_y>=play_button_background.top \
        and game_input.mouse_y<=play_button_background.bottom:
        
        if game_input.mouse_hold_down:
            # Start playing
            success = pygame.event.post(pygame.event.Event(GameEvent.StartGame))
            print(success)


        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.draw.rect(screen, (180, 180, 255), play_button_background, 0, 6) # invert button colors if hovering over it
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.draw.rect(screen, (150, 150, 255), play_button_background, 0, 6)   
    
    screen.blit(play_button, play_button_rect)

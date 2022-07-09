import pygame
from pygame import Rect

def end_screen(screen, game_input, fonts, common_gui):

    trigger_next_scene = (False, "")

    pygame.draw.rect(screen, (220, 220, 255), common_gui.popup)
    str1="GAME OVER; YOU LOSE"
    txt1=fonts.header.render(str1, True, (0, 0, 0))
    txt1_rect=txt1.get_rect()
    txt1_rect.center=(screen.get_width()/2, 100+(txt1_rect.height/2))
    screen.blit(txt1, txt1_rect)

    str2="Score: "
    txt2=fonts.paragraph.render(str2, True, (0, 0, 0))
    txt2_rect=txt2.get_rect()
    txt2_rect.center=(screen.get_width()/2, txt1_rect.height+100+75)
    screen.blit(txt2, txt2_rect)
    
    play_button=fonts.button.render("PLAY AGAIN", True, (0, 0, 0))
    play_button_rect=play_button.get_rect()
    play_button_rect.center=((screen.get_width()/2)-(play_button_rect.width/2)-60, screen.get_height()-75-40-(play_button_rect.height/2))
    play_button_background=Rect(play_button_rect.center[0]-(play_button_rect.width/2)-30, play_button_rect.center[1]-(play_button_rect.height/2)-15, play_button_rect.width+60, play_button_rect.height+30)
    
    exit_button=fonts.button.render("EXIT", True, (0, 0, 0))
    exit_button_rect=exit_button.get_rect()
    exit_button_rect.center=((screen.get_width()/2)+((screen.get_width()/2)-play_button_rect.center[0]), play_button_rect.center[1])
    exit_button_background=Rect(exit_button_rect.center[0]-(play_button_background.width/2), exit_button_rect.center[1]-(play_button_background.height/2), play_button_background.width, play_button_background.height)
    
    play_button_hover = game_input.mouse_x>=play_button_background.left \
        and game_input.mouse_x<=play_button_background.right \
        and game_input.mouse_y>=play_button_background.top \
        and game_input.mouse_y<=play_button_background.bottom

    exit_button_hover = game_input.mouse_x>=exit_button_background.left \
        and game_input.mouse_x<=exit_button_background.right \
        and game_input.mouse_y>=exit_button_background.top \
        and game_input.mouse_y<=exit_button_background.bottom
                
    if play_button_hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, (180, 180, 255), play_button_background, 0, 6) # invert button colors if hovering over it
        if game_input.mouse_hold_down:

            trigger_next_scene = (True, "playing")


    else:
        pygame.draw.rect(screen, (150, 150, 255), play_button_background, 0, 6)
    if exit_button_hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, (180, 180, 255), exit_button_background, 0, 6) # invert button colors if hovering over it
        if game_input.mouse_hold_down:

            trigger_next_scene = (True, "quit")

    else:
        pygame.draw.rect(screen, (150, 150, 255), exit_button_background, 0, 6)
    if not play_button_hover and not exit_button_hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    screen.blit(play_button, play_button_rect)
    screen.blit(exit_button, exit_button_rect)


    return trigger_next_scene
import pygame
import pygame_gui
import Main
from pygame_gui.elements import UIButton

#from Main import SIZE, bx, w, h, title_w

lines = [
    "This was the graph drawer project for Graph Theory class",
    "- You can read about the algorithms",
    "- Draw your own graph and see the result", 
    "- watch step by step algorithm for MST ",
    " ",
    "hope you enjoy !",
    " ",
    "Parsa Mazaheri."        
]


SIZE = (720,480) #Main.SIZE    
w, h = 140, 40
bx, by = int(SIZE[0]/2 - w/2), int(SIZE[1]/3)
title_w = 200

def aboutPage():
    # clear the screen
    Main.manager.clear_and_reset()
    Main.screen.fill(Main.manager.get_theme().get_colour(Main.background))
    
    # title
    logo_font = pygame.font.SysFont("lucida sans", 24, bold=True)
    word = logo_font.render('About', 0, pygame.Color('white'))
    Main.screen.blit(word, (int(SIZE[0]/2-25), h))
    
    # about-text alignment
    font = pygame.font.SysFont("lucida sans", 16)
    # we're using i to pu lines and button in order
    i = 1
    for line in lines:
        i += 1
        word = font.render(line, 0, pygame.Color('white'))
        Main.screen.blit(word, (int(SIZE[0]/4), h + 25 * i))
    pygame.display.update()

    i += 7
    # buttons
    back_btn = UIButton(relative_rect= pygame.Rect(bx, h+20*i, w, h), object_id='btn_style',
                            text='Back', manager=Main.manager, anchors={'left': 'left',
                                                                    'right': 'right',
                                                                    'top': 'top',
                                                                    'bottom': 'bottom'})
                                                                    
    while True:
        # get events (button clicks)
        for event in pygame.event.get():
            # about
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                    event.ui_element == back_btn:
                Main.StartPage()
            # quit 
            if event.type == pygame.QUIT:
                exit()
            
            Main.manager.process_events(event)
        
        # refresh every 10 ms
        Main.manager.update(10)
        Main.surface.blit(Main.screen, (0, 0))
        Main.manager.draw_ui(Main.surface)
        pygame.display.update()



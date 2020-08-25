import os
import subprocess
import sys
import pygame
import pygame_gui



# ---------------- screen initialize ----------------#
pygame.init()
SIZE = (800, 560)
pygame.display.set_caption('Graph')
surface = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont("lucida sans", 18, bold=True)
# theme = "C:\\Users\\Parsa Mazaheri\\Desktop\\Code\\maxmatching\\theme.json"
manager = pygame_gui.UIManager(SIZE, "theme.json")

screen = pygame.Surface(SIZE)
background = 'dark_bg' 
#background = 'hovered_text'
screen.fill(manager.get_theme().get_colour(background)) #pygame.Color('white'))


# ---------------- global variables ----------------#
w, h = 140, 40
#bx, by = int(SIZE[0]/2 - w/2), int(SIZE[1]/3)
bx, by = int(SIZE[0]/4 + 30), int(SIZE[1]/3)
btn_x = int(SIZE[0]/2 - w/2)
title_w = 200
SIZE2 = (640,320)

# ---------------- import local Classes -------------#
import About
import GraphUI


def StartPage():
    # clear the screen
    manager.set_window_resolution(SIZE)
    manager.clear_and_reset()
    #screen = pygame.Surface(SIZE2)
    #pygame.display.set_mode(SIZE2, pygame.RESIZABLE)
    screen.fill(manager.get_theme().get_colour(background))

    # title
    logo_font = pygame.font.SysFont("lucida sans", 32, bold=True)
    word = logo_font.render('graph Project', 0, pygame.Color('white'))
    screen.blit(word, (int(SIZE[0]/2 - title_w/2), h))
    pygame.display.update()

    # we're using i to put lines and buttons in order
    i = 2
    
    # vertex label
    create_label('Vertex No.', bx, h+40*i)
    # vertex input
    v_num = create_text_entry(bx + w, h+40*i)
    i += 1
    # edge label
    create_label('Edge No.', bx, h+40*i)
    # edge input
    e_num = create_text_entry(bx + w, h+40*i) 
    i += 1
    # MST button
    mst_btn = create_button('MST',btn_x, h+40*i)
    i += 1 
    # max matching button
    matching_btn = create_button('Maximum Matching',btn_x, h+40*i) 
    i += 1               
    # about button                                           
    about_btn = create_button('About',btn_x, h+40*i)
    i += 1
    # quit button
    quit_btn = create_button('Quit',btn_x, h+40*i)


    # main loop
    while True:
        # get events (button clicks)
        for event in pygame.event.get():
            # mst 
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                    event.ui_element == mst_btn:
                print("mode: MST", end=" - ")
                v, e = v_num.get_text(), e_num.get_text()
                if correct_input(v, e):
                    GraphUI.vertexes, GraphUI.edges, GraphUI.weights = [], [], []
                    GraphUI.run('mst', int(v), int(e))
                
            # maximum matching
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                    event.ui_element == matching_btn:
                print("mode: Maximum matching")
                v, e = v_num.get_text(), e_num.get_text()
                if correct_input(v, e):
                    GraphUI.vertexes, GraphUI.edges, GraphUI.weights = [], [], []
                    GraphUI.run('mm', int(v), int(e))
            
            # about
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and \
                    event.ui_element == about_btn:
                print("About Page")
                About.aboutPage()
            
            # quit 
            if event.type == pygame.QUIT or (event.type == pygame.USEREVENT and \
                event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == quit_btn):
                exit()
            
            manager.process_events(event)
        screen_update()


def screen_update():
    # refresh every 10 ms
    manager.update(100)
    surface.blit(screen, (0, 0))
    manager.draw_ui(surface)
    pygame.display.update()


# checks if the entries are number and not empty 
def correct_input(v, e):
    # v, e are not empty
    if v and e:
        if v.isdigit() and e.isdigit():
            return True
        warning('V and E must be numbers')
        return False
    warning('Fill all the entires')
    return False           


# check if entered weights are correct
def correct_weights(weights):
    for w in weights:
        if not w.get_text():
            warning("Enter all weights !")
            return False
        if not w.get_text().isdigit():
            warning("weights must be numbers !")
            return  False
    return True


# check if the start node is correct (for prim)
def correct_src_node(src, v):
    if not src.get_text():
        warning('Enter starting node')
        return False
    if not src.get_text().isdigit():
        warning('Source Node must be a number')
        return False
    if int(src.get_text()) >= v:
        warning('Source Node must be from vertexes')
        return False
    return True           


# show warning for 1s and clear
def warning(message):
    w_font = pygame.font.SysFont("lucida sans", 14, bold=True)
    # set warning
    word = w_font.render(message, 0, pygame.Color('red'))
    screen.blit(word, (10,30))
    screen_update()

    pygame.time.wait(1000)
    
    # clear warning
    word = w_font.render(message, 0, pygame.Color('#15191e'))
    screen.blit(word, (10,30))
    screen_update()


# create button with name t in x,y
def create_button(text, x, y):
    return pygame_gui.elements.UIButton(relative_rect= pygame.Rect(x, y, w, h), object_id='btn_style',
                            text=text, manager=manager, anchors={'left': 'left',
                                                                'right': 'right',
                                                                'top': 'top',
                                                                'bottom': 'bottom'})
# create reverse button (for back button)
def create_reverse_button(text, x, y):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect(x, y, w, h), object_id='btn_style',
                            text=text, manager=manager, anchors={'left': 'right',
                                                                'right': 'right',
                                                                'top': 'bottom',
                                                                'bottom': 'bottom'})
# create a input entry in x,y
def create_text_entry(x, y, *given_size):
    ww, hh = w, h
    if given_size:
        ww, hh = given_size[0], given_size[1]
    return pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(x, y, ww, hh),
                                        manager=manager, anchors={'left': 'left',
                                                                'right': 'right',
                                                                'top': 'top',
                                                                'bottom': 'bottom'})
# create label named t in x,y
def create_label(text, x, y):
    pygame_gui.elements.UILabel(relative_rect= pygame.Rect(x, y, w, h), object_id='label_style',
                            text=text, manager=manager, anchors={'left': 'left',
                                                                'right': 'right',
                                                                'top': 'top',
                                                                'bottom': 'bottom'})
# create drop down in x,y with default value = d
def create_drop_down(x, y, *d):
    # if d isn't set show "select algorithm"
    if not d:
        d += ('Select Algorithm', '')
    return pygame_gui.elements.UIDropDownMenu(['Prim', 'Kruskal'], d[0],
                                             pygame.Rect(x+0.6*w, y, 1.1*w, h),
                                             manager=manager)

# Start of the program
if __name__ == "__main__":
    # install pygame and pygame-gui
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    packages = ['pygame', 'pygame-gui']
    for p in packages:
        if p not in installed_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])
    # start program
    StartPage()
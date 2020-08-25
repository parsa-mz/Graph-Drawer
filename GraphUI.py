import pygame
import pygame_gui
import Main
from math import sqrt
from MST import GraphK, GraphMatrix
from Blossom import Graph, Vertex, Edge, Matching, find_maximum_matching


# ----------- Global variables ------------- #
radius = 18
vertexes = []
edges = []
weights = []


## main function (extra isn't necessary)
#  extra is used to pass (selected algorithm and is_graph_entered)

def run(mode, v, e, *extra):
    # clear the screen
    Main.manager.clear_and_reset()
    Main.screen.fill(Main.manager.get_theme().get_colour(Main.background))
    
    # back button                                                
    back_btn = Main.create_reverse_button('Back', -160, -60)
    next_btn = None 

    Main.screen_update()


    ## 1 - max matching
    if mode == 'mm':
        G = matchingGraph(v, e)
        matching = Matching.from_graph(G)
        matching = find_maximum_matching(G, matching)
        print(matching)

        # draw maximum matching edges blue 
        draw_matching(matching)
        back_btn = Main.create_reverse_button('Back', -160, -60)

    ## 2 - minimum spanning tree
    if mode == 'mst':
        if extra:
            # when graph entered -> refresh page -> draw graph again with weights -> show algo selection
            draw_graph()
            # first time (extra == True) --> show algoirthm selection
            # second time (extra == algorithm) --> show algorithm name
            if extra[0] == True:
                selected_algo = Main.create_drop_down(Main.SIZE[0] - 1.8*Main.w, Main.h)
            else: # extra == algorithm_name
                selected_algo = Main.create_drop_down(Main.SIZE[0] - 1.8*Main.w, Main.h, extra[0])
        else:
            # get graph
            mstGraph(v, e)
            next_btn = Main.create_button('Next', Main.SIZE[0] - 1.1*Main.w, 1.1*Main.h*2)
        
        i = 2
        strt_point = None
        # for prim add start node
        if extra and extra[0] == 'Prim':
            Main.create_label('Start Node:', Main.SIZE[0] - 1.4*Main.w, 1.05*i*Main.h)
            strt_point = Main.create_text_entry(Main.SIZE[0] - 1.4*Main.w + Main.w, 1.1*Main.h*i, 40, 30)
            i += 1
        # run button
        if extra and extra != True:
            run_btn = Main.create_button('Run', Main.SIZE[0] - 1.1*Main.w, 1.1*Main.h*i)
        
        Main.screen_update()



    while True:
        # get events (button clicks)
        for event in pygame.event.get():
            # next button
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED \
                and event.ui_element == next_btn:
                # all weights have been entered correctly
                if Main.correct_weights(weights):
                    run('mst', v, e, True)
            
            # back button
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED \
                and event.ui_element == back_btn:
                Main.StartPage()

            # select algorithm
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED \
                and event.ui_element == selected_algo:
                run('mst', v, e, selected_algo.selected_option)
            
            # algorithm run button
            if extra and event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED \
                and event.ui_element == run_btn:
                run_algorithm(extra[0], v, e, strt_point)
            # quit 
            if event.type == pygame.QUIT:
                exit()
            
            Main.manager.process_events(event)
        Main.screen_update()




def matchingGraph(v, e):
    # clear screen
    Main.manager.clear_and_reset()
    Main.screen.fill(Main.manager.get_theme().get_colour(Main.background))
    
    # create a new matching graph
    G = Graph()                                       
    # get vertice
    draw_text("Select {} Vertex".format(v), 's')
    for i in range(v):
        # get vertex position
        vertexes.append(get_pos())
        # add vertex to graph
        G.add_vertex(Vertex('V'+ str(i)))                  
        # draw vertex
        draw_node(G.vertices[i], i)                        
    draw_text("Select {} Vertex".format(v), 'c')
    
    G.init_connected()
    # get edges 
    draw_text("Select {} Edges".format(e), 's')
    for i in range(e):
        # vertex 1,2 position
        pos1 = get_pos()                                
        pos2 = get_pos()
        # get real position (nearest vertex to selected position)
        u, v = get_vertice(pos1, pos2)
        
        # while i, j are the same get position again
        while u == v:
            pos1 = get_pos()                                
            pos2 = get_pos()
            u, v = get_vertice(pos1, pos2)

        # draw edge
        draw_edge(u, v, 'grey')                            
        # add to graph
        G.add_edge(G.vertices[u], G.vertices[v])
        # u and v are connected to something (not alone)
        G.connected[u] = G.connected[v] = True
    draw_text("Select {} Edges".format(e), 'c')
    # alone vertex is a vertex that isn't connected to anyone
    G.kick_out_alone_vertex()
    return G 


def mstGraph(v, e):
    # clear screen
    Main.manager.clear_and_reset()
    Main.screen.fill(Main.manager.get_theme().get_colour(Main.background))
    
    draw_text("Select {} Vertex".format(v), 's')
    for i in range(v):
        # get vertex position
        vertexes.append(get_pos())                  
        # draw vertex
        draw_node(vertexes[i], i)                        
    draw_text("Select {} Vertex".format(v), 'c')
    
    # get edges 
    draw_text("Select {} Edges".format(e), 's')
    for i in range(e):
        # vertex 1,2 position
        pos1 = get_pos()                                
        pos2 = get_pos()
        # get real position (nearest vertex to selected position)
        u, v = get_vertice(pos1, pos2)
        
        # while i == j get new position again
        # i, j must be diffrent nodes
        while u == v:
            pos1 = get_pos()                                
            pos2 = get_pos()
            u, v = get_vertice(pos1, pos2)

        # draw edge
        draw_edge(u, v, 'grey') 
        Main.screen_update()
        # add to edge and weight(weights are text_entry objects not numbers)
        edges.append((u,v))
    draw_text("Select {} Edges".format(e), 'c')
    
    draw_text("Enter Edge Weights", 's')
    for i in range(e):
        u, v = edges[i][0], edges[i][1]
        x, y = (vertexes[u][0] + vertexes[v][0])/2, (vertexes[u][1] + vertexes[v][1])/2  
        weight_i = Main.create_text_entry(x, y, 30, 20)
        Main.screen_update()
        weights.append(weight_i)                         



# run algorithm
def run_algorithm(algoirthm, v, e, strt):
    # for kruskal start is null (don't need it)
    if algoirthm == 'Kruskal':
        g = GraphK(vertexes, edges, weights) 
        g.KruskalMST() 
    # algoirthm == 'Prim'
    elif Main.correct_src_node(strt, v): 
        g = GraphMatrix(vertexes, edges, weights) 
        g.primMST( int(strt.get_text()) )
        


# draw graph with weights(for MST)
def draw_graph():
    # vertexs
    for i in range(len(vertexes)):
        draw_node(vertexes[i], i)
    # edges
    for i in range(len(edges)):
        draw_edge(edges[i][0], edges[i][1], 'grey')
    # weights
    for i in range(len(edges)):
        # edge vertexes
        u, v = edges[i][0], edges[i][1]
        # middle of edge location
        x,y = (vertexes[u][0] + vertexes[v][0])/2, (vertexes[u][1] + vertexes[v][1])/2
        pos = (int(x), int(y))
        draw_text(weights[i].get_text(), 's', pos)



# darw node  
# input: vertex v -  index i
def draw_node(v, i):  
    pygame.draw.circle(Main.screen, pygame.Color('red'), vertexes[i], radius, 1)
    vertex_name = 'V' + str(i)
    word = Main.font.render(vertex_name, 0, pygame.Color('white'))
    Main.screen.blit(word, (vertexes[i][0] - 7, vertexes[i][1] - 7))
    Main.screen_update() 


# darw edges 
# input: index i, j -  color (grey: defualt -- blue: maxMatching)
def draw_edge(i, j, color):
    pygame.draw.line(Main.screen, pygame.Color(color), vertexes[i], vertexes[j], 2)
    Main.screen_update() 


# draw text on screen
# input: mode: (s: set / c: clear)
#        pos: position is optional [default is (10,10)] 
def draw_text(message, option, *pos):
    if not pos:
        pos += ((10,10), ())
    if option == 's':
        word = Main.font.render(message, 0, pygame.Color('white'))
        Main.screen.blit(word, pos[0])
    else: # option == 'c'
        word = Main.font.render(message, 0, pygame.Color('#15191e'))
        Main.screen.blit(word, pos[0])
    Main.screen_update() 


# get node position
# input: option: v: for adding vertex -> add to vertexes 
#                e: for edge -> return position
def get_pos():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos
   

# chooses the nearest vertex to each position 
# input: pos1, pos2 -> returns index i, j (vertex_i, vertex_j)
def get_vertice(pos1, pos2):
    # min dist = INF
    min_dist1, min_dist2 = 1010101, 1010101
    s1, s2 = -1, -1
    for i in range(len(vertexes)):
        d1 = sqrt((pos1[0] - vertexes[i][0])**2 + (pos1[1] - vertexes[i][1])**2)
        if d1 < min_dist1:
            min_dist1 = d1
            s1 = i

        d2 = sqrt((pos2[0] - vertexes[i][0])**2 + (pos2[1] - vertexes[i][1])**2)
        if d2 < min_dist2:
            min_dist2 = d2
            s2 = i
    if s1 == s2:
        Main.warning("edge's 2 vertice are the same. Try again!")
    return s1, s2


# draw maximum matching
def draw_matching(matching):
    draw_text("Graph's Maximum Matching: ", 's')
    for edge in matching.edges:
        s = str(edge)
        i, j = int(s[2:3]), int(s[7:8])
        # make max mtaching edges blue
        draw_edge(i, j, 'blue')                        
        
    return 


if __name__ == "__main__":
    run('mm', 5, 4)
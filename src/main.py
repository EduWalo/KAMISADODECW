# Library imports
import numpy as np
import pygame
import copy
from pygame import color
from nodo import Nodo


# Class imports

from tablero import Tablero

# get_pos_mouse 
def get_pos_mouse(pos):
    # recibe la posición y la procesa  
    return (pos[0]//75,pos[1]//75)

# print message in screeen

def print_title(screen, dialog_turn, pos =(610,10), fontsize = 30):
    #letreros
    font = pygame.font.Font(None,fontsize)
    text = font.render(dialog_turn,0,(255,255,255))
    screen.blit(text,pos)
    pygame.display.update()  
    


# main 
def main():
    #load screen 
    successes, failures = pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    #temporizador
    clock = pygame.time.Clock()
    FPS = 120 

    running = True
    #win,loose = False,False
    
    # INIT REFRESH RATE
    clock.tick(FPS)
    
    # tablero de juego
    tablero_game = Tablero()

    

    # position of player
    playeri =0
    playerj =0

    # color olbigatorio
    color_obligatorio = -1
    resalt_ob = True

    
    

    while running:
        # generar pantalla
        screen.fill((0,0,0))

        # dibujado
        tablero_game.show_all(screen)
        pygame.display.update()

        # mira si hay victorias 
        if (tablero_game.win_condition()):
            print_title(screen,"GANA LA IA")
            running = False
            input()
            break

        ## delay
        pygame.time.delay(10)

        # show posibilities
        if (color_obligatorio != -1 and resalt_ob):
            resalt_ob = False
            coor =tablero_game.get_coor_ficha('B',color_obligatorio)
            tablero_game.resalt((coor[1],coor[0]),screen)
            


        #Load mouse to generathe player position
        ev = pygame.event.get()
        for event in ev:
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #print(get_pos_mouse(pos))
                if(color_obligatorio == -1):
                    result = tablero_game.resalt(get_pos_mouse(pos),screen)
                elif (get_pos_mouse((pos[0],pos[1])) in tablero_game.posible_option):
                    # se verifica solo el color obligartorio
                    result = tablero_game.resalt(get_pos_mouse(pos),screen)
                else :
                    coor = tablero_game.get_coor_ficha('B',color_obligatorio)
                    result = tablero_game.resalt((coor[1],coor[0]),screen)
                    


                
                # dibujado
                tablero_game.show_all(screen)
                pygame.display.update()

                if (tablero_game.win_condition()):
                    print_title(screen,"GANA HUMANO")
                    running = False
                    input()
                    break

                if(result != None or (tablero_game.posible_option == [] and tablero_game.resalt_pos[0] != None)):
                    if (tablero_game.posible_option == [] and tablero_game.resalt_pos[0] != None):
                        print_title(screen,"BLOQUEO")
                        print_title(screen,"HUMANO PIERDE TURNO", (605,40), 20)
                        
                        input()
                    # se realizo la jugada y sigue la IA
                    tbtemp = copy.copy (tablero_game)
                    tbtemp.piezasK = np.copy(tablero_game.piezasK)

                    if (result == None):
                        
                        nodoIA = Nodo("Max",color_obligatorio,'N',0,tbtemp)
                    else:
                        color_obligatorio = result;
                        nodoIA = Nodo("Max",result,'N',0,tbtemp)
                        ##
                        print_title(screen,"IA PLAYING...")
                        nodoIA.get_utility()
                    
                    # se verifica si hubo cambios en la ia 
                    if (nodoIA.cambios_estado):
                        tablero_game = copy.copy(nodoIA.estado_min_max);
                        tablero_game.piezasK = np.copy(nodoIA.estado_min_max.piezasK) 
                        color_obligatorio = nodoIA.color_expandido
                        
                    else :
                        
                        print_title(screen,"BLOQUEO")
                        print_title(screen,"IA PIERDE TURNO", (605,40),20)
                        pygame.time.delay(200)
                    
                    resalt_ob = True

                    
                
                
            if event.type == pygame.QUIT:
                running = False
        
    

            
    
    


if __name__ == "__main__":
    main()
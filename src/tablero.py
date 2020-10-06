#imports
from operator import truediv
from numpy.lib.function_base import select
import pygame
import numpy as np

# Def

class  Tablero():
    
    # fichas de seleccion 
    # las ficas son una matriz que solo me dibuja las fichas
    # tiene 3 dimeciones 
    # i [8] pos
    # j [8] pos
    # k [3] {existencia (0,1) ; tipo(blanca,negra) ;  color}

    piezasK = np.zeros((8,8,3),dtype=str )

    # Tabla
    # tabla con los colores de las posiciones
    # posee un numero de los colores designados para las fichas
    tableroK = np.zeros((8,8),dtype=str)


    # DEFINICION DE VALORES MAXIMOS Y MINIMOS
    maxVal =  999999;
    minVal = -999999;

    # resalt position
    resalt_pos = [None,None]
    posible_option =[]


    # INICIALIZATION
    def __init__(self) :
        self.generarficahs()
        self.construirtablero()
        self.rectangulos = [] # lista de los rectangulos
        
        
    
    

    # generarfichas genera la posición de las fichas inicial
    # asignandoles tipo y color
    
    def generarficahs(self):
        for i in range(0,8,7):#0 7
            for j in range(8):
                self.piezasK[i][j][0]=1 #existe la ficha
                # tipo de la ficha 
                if i < 7 :
                    self.piezasK[i][j][1]= "N"
                    # color de la ficha
                    self.piezasK[i][j][2] = j+1
                else :
                    self.piezasK[i][j][1]= "B"
                    # color de la ficha
                    self.piezasK[i][j][2] = 8-j 
        
    # genera las posiciones de los colores en el tablero 
    def construirtablero(self):
        cont=0
        for i in range(8):
           for j in range(8):
               cont+=1
               self.tableroK[i][j] = self.get_color_tabla(cont);


    # me retorna el color que necesito con respecto a un numero dado 
    def get_color_str(self,num):
        switcher = {
            1: "#D36135",
            2: "#487DA7",
            3: "#8800A0",
            4: "#E40F8D",
            5: "#E9AA0C",
            6: "#CC0025",
            7: "#14B850",
            8: "#8C5254"
        }
        return switcher[num]
    
    # retorna el color seleccionado para cada cacilla de la tabla
    def get_color_tabla(self, num):

        if (num == 1 or num == 10 or num == 19 or num == 28 or num == 37 or num == 46 or num == 55 or num == 64 ):
            color = 1
        elif (num == 2 or num == 13 or num == 24 or num == 27 or num == 38 or num == 41 or num == 52 or num == 63 ):
            color = 2
        elif (num == 3 or num == 16 or num == 21 or num == 26 or num == 39 or num == 44 or num == 49 or num == 62 ):
            color = 3
        elif (num == 4 or num == 11 or num == 18 or num == 25 or num == 40 or num == 47 or num == 54 or num == 61 ):
            color = 4
        elif (num == 5 or num == 14 or num == 23 or num == 32 or num == 33 or num == 42 or num == 51 or num == 60 ):
            color = 5
        elif (num == 6 or num == 9 or num == 20 or num == 31 or num == 34 or num == 45 or num == 56 or num == 59 ):
            color = 6
        elif (num == 7 or num == 12 or num == 17 or num == 30 or num == 35 or num == 48 or num == 53 or num == 58 ):
            color = 7
        # (num == 8 or num == 15 or num == 22 or num == 29 or num == 36 or num == 43 or num == 50 or num == 57 )
        else :
            color = 8

        return color;
    
    # Permite mover a una pieza de un punto a optro
    def mover_ficha(self, oldi, oldj, newi, newj):
        # Adicionar el contenido
        self.piezasK[newi][newj][0] = self.piezasK[oldi][oldj][0] # agrega contenido existente
        self.piezasK[newi][newj][1] = self.piezasK[oldi][oldj][1]
        self.piezasK[newi][newj][2] = self.piezasK[oldi][oldj][2]

        # vaciar el contenido del movimiento anterior
        self.piezasK[oldi][oldj][0] = ''
        self.piezasK[oldi][oldj][1] = ''
        self.piezasK[oldi][oldj][2] = ''

        return self.tableroK[newi][newj]; # retornando el color que le toca al rival 

    
    # Obtiene las coordenadas de un color para un tipo de ficha determinado
    def get_coor_ficha(self, tipo, color):
        for i in range(8):
            for j in range(8):
                if self.piezasK[i][j][1] == tipo  and self.piezasK[i][j][2] == color:
                    return (i,j)

    # Permite saber si un movimieto es valido
    def eval_mov(self, oldi, oldj, newi, newj):
        # las oldx no  necesitan validación porque son
        # una posición actua que se en una ficha determinada

        #### validar desborde
        ### validar dirección 
        # se asimila que solo se debe validar 
        # las jugadas de las blancas
        # por ende ellas solo decrementan la posición de 
        # i para llegar a 0 (el otro lado)
        if ( newj > 7 or oldj < 0  or oldi < newi ) :
            return False #por desbordar o por intentar devolverse
        
        # en este punto se sabe que el cambio en i
        # es ninguno 0 o negativo (subiendo)
        # entonces se valida que cambie de manera equivalente a i
        if (oldi == newi and oldj == newj):
            # no hubo cambios
            return True
        
        elif (oldi != newi and oldj != newj):
            # se valida los cambios 
            # porque en donde solo cambia uno de los 
            # elementos i o j seria los lados o arriba
            # aque se valida que el cambio que ocurra sea lineal
            m = (newj - oldj )/(newi - oldi)
            if (m*m != 1 ):
                return False # por no respetar la diagonal
            
        
        ### validar que no salte fichas
        # direcciones 
        cambio_i=0
        camiio_j=0
        if (newi != oldi ):
            cambio_i=1
        if (newj < oldj):
            # decremento
            camiio_j = -1
        elif (newj > oldj):
            # incremento
            camiio_j =1

        # mientras aún halla diferencias se debe seguir comparando
        while(newj != oldj or newi != oldi): 
            # Aumento en las cordenadas viejas 
            # hasta llegar a las nuevas
            oldi += cambio_i
            oldj += camiio_j
            if( self.piezasK[oldi][oldj][0] != ''):
                # si hay una ficha en el camino no es posible
                # generar el movimiento
                return False
        
        return True
        

    # Permite determinar si hay una victoria
    def win_condition(self):
        # las fichas negras van de 0 a 7
        # las blancas van de 7 a 0
        for i in range(0,8,7):
            for j in range(8):
                if ( (i == 0  and self.piezasK[i][j][1] == 'B' ) or  (i == 7  and self.piezasK[i][j][1] == 'N')):
                    return True
        
        return False


    # devuelve el numeor de posibilidades que se tiene para que una ficha negra
    # logre coronar (direcciones despejadas para que se corone)

    def get_val_corona(self):
        cont_direcciones = 0
        # debo recorrer todas las posibilidades de coronar
        # contando desde i 0 e iterar en sus direcciones
        for j in range(8):
            # solo se puede coronar si no hay una ficha blanca en la 
            # posicion 0
            if (self.piezasK[0][j][0]  == ''):
                # puedo proceder por que está vacio
                # i++, j--
                for k in range(1,8):
                    if (k > 7 or j-k < 0 ):
                        break
                    elif(self.piezasK[k][j-k][1] == 'B'):
                        break
                    elif(self.piezasK[k][j-k][1] == 'N'):
                        cont_direcciones +=1
                        break

                # i++ 
                for k in range(1,8):
                    if (k > 7 or j-k < 0 ):
                        break
                    elif(self.piezasK[k][j][1] == 'B'):
                        break
                    elif(self.piezasK[k][j][1] == 'N'):
                        cont_direcciones +=1
                        break

                # i++, j++
                for k in range(1,8):
                    if (k > 7 or j +k > 0 ):
                        break
                    elif(self.piezasK[k][j+k][1] == 'B'):
                        break
                    elif(self.piezasK[k][j+k][1] == 'N'):
                        cont_direcciones +=1
                        break
        
        return cont_direcciones

    # Obtiene la utilidad
    def get_profit(self):
        # la utilidad siempre se genera a favor de la snegras
        # ya que ella son quien usan el la utilidad 
        # para decidir
        cont_pos =0
        for i in range (8):
            for j in range (8):
                if (self.piezasK[i][j][0] != ''):
                    if (i == 0 and self.piezasK[i][j][1] == 'B'):
                        cont_pos +=self.minVal
                    elif (i == 7 and self.piezasK[i][j][1] == 'N'):
                        cont_pos +=self.maxVal
                    else:
                        cont_pos += self.get_val_corona()

        return cont_pos



    
    ## show table and picis

    def show_all(self,screen_k):
        ### print tablero
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(
                    screen_k,
                    pygame.Color(self.get_color_str(int (self.tableroK[i][j]))),
                    pygame.Rect(j*75,i*75,75,75)
                    )
                if (self.piezasK[i][j][0] != ''):
                    if (self.piezasK[i][j][1] == 'B'):
                        pygame.draw.circle(
                            screen_k,
                            pygame.Color("#ffffff"),
                            (j*75+37,i*75+37),
                            34
                            )
                        
                    elif (self.piezasK[i][j][1] == 'N'): 
                        pygame.draw.circle(
                            screen_k,
                            pygame.Color("#000000"),
                            (j*75+37,i*75+37),
                            34
                            )
                    
                    pygame.draw.circle(
                        screen_k,
                        pygame.Color(self.get_color_str(int (self.piezasK[i][j][2]))),
                        (j*75+37,i*75+37),
                        28
                        )
        
        if(self.resalt_pos[0] != None):
            pygame.draw.circle(
                    screen_k,
                    pygame.Color("#C7EF00"),
                    (self.resalt_pos[0]*75+37,self.resalt_pos[1]*75+37),
                    35,
                    10
                    )

        # posiciones posibles 
        if (self.posible_option != []):
            for i in self.posible_option:

                pygame.draw.circle(
                    screen_k,
                    pygame.Color("#C7EF00"),
                    (i[0]*75+37,i[1]*75+37),
                    30,
                    1
                    )
                
    
    # resalta la posición ingresada
    def resalt(self,pos,screen_k):
        # li el resalto ya esta resaltado no se vuelve a dibujar
        # si está por fuera tampoco se dibuja 
        # solo se dibuja si es una pieza = B
        # se muestran sus posibilidades
        
        if (pos[0] < 8 and pos[0] >=0 and pos[1] < 8 and pos[1] >=0  ):
            # rango de opcions
            
            if ((self.resalt_pos[0] == None) or (self.resalt_pos[0] != pos[0] or self.resalt_pos[1] != pos[1])): # se debe cambiar
                #print("Resalt " , pos)
                
                # draw resalt 
                if (self.piezasK[pos[1]][pos[0]][1] == 'B'):
                    
                    
                    
                    # fuarda la ficha resaltada
                    self.resalt_pos[0] = pos[0]
                    self.resalt_pos[1] = pos[1]

                    #limpiar lista
                    self.posible_option = []
                    
                    
                    # left j-- pos[0]  up i-- pos[1]
                    for k in range(1,8):
                        if (  pos[0] - k < 0  or pos[1] - k < 0):
                            break; #desborde
                        elif (self.piezasK[ pos[1] - k ][ pos[0] - k][0] != ''):
                            break;
                        else : 
                            # genero la dupa
                            self.posible_option.append(( pos[0] - k, pos[1] - k))

                    # up i-- pos[1]
                    for k in range(1,8):
                        if (   pos[1] - k < 0):
                            break; #desborde
                        elif (self.piezasK[ pos[1] - k ][ pos[0] ][0] != ''):
                            break;
                        else : 
                            # genero la dupa
                            self.posible_option.append(( pos[0] , pos[1] - k))
                    
                    # rigth j++ pos[0]  up i-- pos[1]
                    for k in range(1,8):
                        if (  pos[0] + k > 7  or pos[1] - k < 0):
                            break; #desborde
                        elif (self.piezasK[ pos[1] - k ][ pos[0] + k][0] != ''):
                            break;
                        else : 
                            # genero la dupa
                            self.posible_option.append(( pos[0] + k, pos[1] - k))
                    
                        
                elif (self.posible_option != [] ):
                    if ( pos in self.posible_option ):
                        #jugar 
                        color_obl = self.mover_ficha(self.resalt_pos[1], self.resalt_pos[0], pos[1], pos[0] );
                        # elimieno la definición anterior
                        self.resalt_pos = [None,None]
                        self.posible_option =[]
                        # Color obligatorio 
                        return color_obl
                        

                    
        
        #if 
        #self.posible_option == []
                            
                
                

            

        
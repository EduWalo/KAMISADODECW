#imports
from operator import truediv
from numpy.lib.function_base import select
import pygame
import numpy as np
import copy

from tablero import Tablero

# Def

class  Nodo(): 

    ### profunfidad maxima para la xpanción de los nodos
    profundidad_max = 5
    # valor del abuelo
    padre = None

    # tipo (Max,Min)
    tipo = ''
    
    # profundidad
    profundidad = 0
    
    # utilidad que permite determinar el valor del nodo
    utility = 0

    # tipo de la pieza (Negra o Blanca)
    tipo_pieza = ''

    # color de la pieza a mover en numero
    color_a_mover = ''

    # tablero (estado de la jugada)
    estado_actual = Tablero()

    # dupla de la posición en la que comienza la ia 
    pos = [None,None]

    # color que genera el hijo o nodo expandido
    color_expandido = ''

    # tablero que debo devolver
    estado_min_max = Tablero()

    # booleano para los cambios de estado posibles 
    cambios_estado = False
    
    # booleano de poda
    podar = False
    
    def __init__(self, tipo_min_max, color_p, tipo_p, profundidad_h, tablero_de_estado) :
        self.tipo = tipo_min_max
        self.color_a_mover = color_p
        self.tipo_pieza = tipo_p
        self.profundidad = profundidad_h
        self.estado_actual = tablero_de_estado

        ## valores minimos y max
        if ( self.tipo == "Max"):
            self.utility = -99999999999
        else :
            self.utility =  99999999999


    # sobrecarga 
    def __str__(self) :
        return f"{self.tipo} {self.pos} -> "
    def __repr__(self) :
        return f"{self.tipo} {self.pos} -> "
    


    # 
    def copia(self, tb):
        tr = tb
        return tr
    # print nodo
    #def show_nodo()

    # generar utilidad
    def get_utility(self):
        # obtengo la coordenada obligatoria por el color
        pos_ob = self.estado_actual.get_coor_ficha(self.tipo_pieza, self.color_a_mover)
        self.pos = pos_ob

        # mostrar nodo 
        #print ("->",self.profundidad,self)

        ########### estado de parada por profundidad
        if (self.profundidad == self.profundidad_max):
            self.utility = self.estado_actual.get_profit()
            return self.utility
        
        ########### verificar estado
        if (self.estado_actual.win_condition()):
            self.utility = self.estado_actual.get_profit()
            return self.utility
        

        ########## se debe establecer un recorrido de actividades
        if (self.tipo == "Max"):
            #maximisar

            #print("LP")
            # left j-- up i++
            for k in range(1,8):
                if (pos_ob[0] + k > 7 or  pos_ob[1] - k < 0):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] + k ][ pos_ob[1] - k][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                    # se copia el estado 
                    tablero_temporal = copy.copy (self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] + k, pos_ob[1] -k)
                    nodo_temporal = Nodo("Min",color_temporal,'B',self.profundidad +1,tablero_temporal)
                    
                    # generar padrentzco
                    nodo_temporal.padre = self

                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility < utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        # forzar paso por valor
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)
                        
                        self.color_expandido = color_temporal

                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Max, su abuelo tambien es Max, 
                                    # podo si la utilidad de este nodo es menor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility > self.utility):
                                        self.padre.podar = True
            
            #print("P")
            # up i++
            for k in range(1,8):
                if (pos_ob[0] + k > 7 ):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] + k ][ pos_ob[1] ][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                    # se copia el estado 
                    tablero_temporal = copy.copy(self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] + k, pos_ob[1] )
                    nodo_temporal = Nodo("Min",color_temporal,'B',self.profundidad +1,tablero_temporal)

                    # generar padrentzco
                    nodo_temporal.padre = self
                    
                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility < utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)

                        self.color_expandido = color_temporal

                        
                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Max, su abuelo tambien es Max, 
                                    # podo si la utilidad de este nodo es menor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility > self.utility):
                                        self.padre.podar = True

            #print("RP")
            # left j++ up i++
            for k in range(1,8):
                if (pos_ob[0] + k > 7 or  pos_ob[1] + k > 7):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] + k ][ pos_ob[1] + k][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                     # se copia el estado 
                    tablero_temporal = copy.copy (self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] + k , pos_ob[1] + k)
                    nodo_temporal = Nodo("Min",color_temporal,'B',self.profundidad +1,tablero_temporal)

                    # generar padrentzco
                    nodo_temporal.padre = self

                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility < utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)
                        self.color_expandido = color_temporal
                        
                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Max, su abuelo tambien es Max, 
                                    # podo si la utilidad de este nodo es menor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility > self.utility):
                                        self.padre.podar = True

        else:
             #minimizar

            #print("LP")
            # left j-- up i--
            for k in range(1,8):
                if (pos_ob[0] - k <0 or  pos_ob[1] - k < 0):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] - k ][ pos_ob[1] - k][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                    # se copia el estado 
                    tablero_temporal = copy.copy (self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] - k, pos_ob[1] -k)
                    nodo_temporal = Nodo("Max",color_temporal,'N',self.profundidad +1,tablero_temporal)

                    # generar padrentzco
                    nodo_temporal.padre = self

                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility > utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)
                        self.color_expandido = color_temporal

                        
                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Min, su abuelo tambien es Min, 
                                    # podo si la utilidad de este nodo es mayor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility < self.utility):
                                        self.padre.podar = True

            #print("P")
            # up i--
            for k in range(1,8):
                if (pos_ob[0] - k < 0 ):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] - k ][ pos_ob[1] ][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                    # se copia el estado 
                    tablero_temporal = copy.copy (self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] - k, pos_ob[1] )
                    nodo_temporal = Nodo("Max",color_temporal,'N',self.profundidad +1,tablero_temporal)

                    # generar padrentzco
                    nodo_temporal.padre = self

                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility > utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)
                        self.color_expandido = color_temporal

                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Min, su abuelo tambien es Min, 
                                    # podo si la utilidad de este nodo es mayor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility < self.utility):
                                        self.padre.podar = True


            #print("RP")
            # left j++ up i--
            for k in range(1,8):
                if (pos_ob[0] - k < 0 or  pos_ob[1] + k > 7):
                    break # por desborde
                elif (self.estado_actual.piezasK[ pos_ob[0] - k ][ pos_ob[1] + k][0] != ''):
                    break # por no poder avanzar
                elif (self.podar):
                    break 
                else:
                     # se copia el estado 
                    tablero_temporal = copy.copy (self.estado_actual)
                    tablero_temporal.piezasK = np.copy(self.estado_actual.piezasK)
                    # generar el color
                    color_temporal = tablero_temporal.mover_ficha(pos_ob[0], pos_ob[1], pos_ob[0] - k , pos_ob[1] + k)
                    nodo_temporal = Nodo("Max",color_temporal,'N',self.profundidad +1,tablero_temporal)

                    # generar padrentzco
                    nodo_temporal.padre = self

                    #utilidad de hijo
                    utilidad_temporal = nodo_temporal.get_utility()

                    # calculo 
                    if ( self.utility > utilidad_temporal or (not(self.cambios_estado))):
                        self.cambios_estado = True;
                        # cambio de utilidad
                        self.utility = utilidad_temporal
                        self.estado_min_max =  copy.copy (nodo_temporal.estado_actual)
                        self.estado_min_max.piezasK = np.copy(nodo_temporal.estado_actual.piezasK)
                        self.color_expandido = color_temporal

                        # poda
                        # como se posee una instancia del nodo anterior (padre), si su utilidad
                        # es del tipo que posee se implementa la suceción de estos para generar la utilidad buscada
                        if (isinstance (self.padre, Nodo) ): # es posible eredar la utilidad
                            if (isinstance (self.padre.padre, Nodo)):#el abuelo existe
                                if (self.padre.padre.cambios_estado): # hubo cambio en el padre se puede proceder a verificar poda
                                    # sie ste nodo es Min, su abuelo tambien es Min, 
                                    # podo si la utilidad de este nodo es mayor que la del abuelo
                                    # ya no es posible cambiar el estado asi que se poda
                                    if (self.padre.padre.utility < self.utility):
                                        self.padre.podar = True


        if (self.cambios_estado ):
            return self.utility
        else :

            return self.estado_actual.get_profit()
        



                


        
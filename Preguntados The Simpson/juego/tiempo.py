# Gestion del sistema de tiempo.
# (ya sea por pregunta o general)

import pygame

def iniciar_tiempo():
    """
    Devuelve el tiempo inicial (en milisegundos) tomando el reloj de pygame.
    """
    return pygame.time.get_ticks()

def tiempo_transcurrido(tiempo_inicio):
    """
    Calcula el tiempo transcurrido desde un punto de inicio.
    
    parametros:
      tiempo_inicio: Tiempo en milisegundos al inicio del calculo.
      
    retorno:
      tiempo transcurrido en segundos(entero).
    """
    
    tiempo_actual = pygame.time.get_ticks() # obtengo el tiempo actual.
    return (tiempo_actual - tiempo_inicio) // 1000 # lo convierto a segundos.
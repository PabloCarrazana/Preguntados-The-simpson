import pygame
from Constantes import *

def manejar_eventos(boton_regresar):
    """
    Maneja los eventos del juego, como el cierre de la ventana y los clics en botones.
    
    parametros:
    - boton_regresar: El boton de regresar que el jugador puede hacer clic.
    
    retorno:
    - ejecutando: Devuelve un valor Booleano que indica si el juego sigue ejecutandose.
    
    """
    ejecutando = True
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Si se cierra la ventana.
            ejecutando = False # Finaliza el juego
        if evento.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic en el ratom
            if boton_regresar.collidepoint(evento.pos):  # Si se hace clic en el boton de regresar
                ejecutando = False  # Sale del juego
    return ejecutando


def actualizar_pantalla_y_fps():
    """
    Actualiza la pantalla con los cambios y controla la tasa de cuadros por segundo (FPS).
    
    """
    pygame.display.flip() # Actualiza la pantalla.
    pygame.time.Clock().tick(FPS)  # Controla la tasa de FPS.
    

def inicializar_juego():
    """
    Inicializar Pygame, crea la ventana del juego y establece el titulo.
    
    Retorna la pantalla creada para el juego.
    """
    pygame.init() # Inicializa Pygame.
    pantalla = pygame.display.set_mode(VENTANA) # Crea la ventana con las dimensiones especificadas en Constantes.py
    pygame.display.set_caption("Preguntados: The Simpson") # Titulo de la ventana.
    return pantalla


def crear_boton(pantalla, texto, x, y, ancho, alto, color_fondo, color_texto, fuente):
    """
    Crea un botón y lo dibuja en la pantalla.

    Parámetros:
    - pantalla: Superficie donde se dibujará el botón.
    - texto: El texto que se mostrará en el botón.
    - x, y: Coordenadas de la esquina superior izquierda del botón.
    - ancho, alto: Dimensiones del botón.
    - color_fondo: Color del fondo del botón.
    - color_texto: Color del texto del botón.
    - fuente: Fuente del texto del botón.

    Retorna:
    - pygame.Rect: El rectángulo del botón, para detectar interacciones.
    """
    # Creo el rectángulo del botón
    rect = pygame.Rect(x, y, ancho, alto) # Define el área del boton.
    pygame.draw.rect(pantalla, color_fondo, rect)  # Dibujar el boton

    # Renderizar el texto y centrarlo dentro del boton
    texto_render = fuente.render(texto, True, color_texto) # Renderiza el texto del botón.
    texto_rect = texto_render.get_rect(center=rect.center) # Centra el texto en el boton.
    pantalla.blit(texto_render, texto_rect) # Dibuja el texto sobre el boton.

    return rect  # Retornar el rectángulo del botón
    
        
def dibujar_texto(pantalla, texto, x, y, fuente, color):
    """
    Dibija un texto en la pantalla.
    
    parametros:
    - pantalla: La superficie de Pygame donse se dibuja el texto.
    - texto: El texto a mostrar (str)
    - x, y: Coordenadas donde se posicionara el texto(int, int)
    - fuente: fuente para el texto
    - color: Color del texto
    
    """
    
    superficie = fuente.render(texto, True, color) # Creo la superficie del texto.
    pantalla.blit(superficie, (x,y)) # Dibuja el texto en la pantalla.
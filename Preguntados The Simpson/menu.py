# menu.py sera responsable de mostrar las opciones del juego, 
# como jugar, configuracion, top 10 y salir.

import pygame
from Constantes import *
from funciones import *
from juego.top_partidas import *
from juego.configuracion import menu_configuracion
from juego.jugar import *


def menu_principal(): 
    """
    Funcion que muestra el menu principal del juego.
    """
    # Llamo a la funcion para inicializar Pygame y crear la ventana
    pantalla = inicializar_juego()
    pygame.mixer.init() # Inicializo el sonido.
    
    # Cargar una imagen de fondo (para el menu).
    fondo = pygame.image.load("juego/recursos\imagenes\menu.jpg")
    fondo = pygame.transform.scale(fondo, VENTANA)  # Escala la imagen al tamaño de la ventana.
    
    # Cargo y reproduce la musica de fondo.
    pygame.mixer.music.load("juego/recursos\sonidos\menu.ogg") # Ruta al archivo de musica.
    pygame.mixer.music.set_volume(0.5) # Ajusta el volumen (0.0 a 0.1)
    pygame.mixer.music.play(-1) # Reproduce la musica en bucle.
    
    # Cargo los sonidos de los botones.
    sonido_jugar = pygame.mixer.Sound("juego/recursos\sonidos\empezar.mp3")
    sonido_config = pygame.mixer.Sound("juego/recursos\sonidos\click.mp3")
    sonido_top = pygame.mixer.Sound("juego/recursos\sonidos\click.mp3")
    
    # Defino la fuente para el texto.
    fuente = pygame.font.Font(None, 36) # Fuente predeterminada, tamaño 36.
    
    # Reloj para controlar FPS.
    reloj = pygame.time.Clock()
    
    
    ejecutando = True # variable para controlar el bucle del menu.
    
    # Bucle principal del menu.
    while ejecutando:
        # Itera sobre los eventos registrados por pygame.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si se cierra la ventana
                ejecutando = False  # Finaliza el bucle

            
            # Detecto clics del mouse.
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifico si se hizo clics en el boton "Jugar".
                if boton_jugar.collidepoint(evento.pos):
                    sonido_jugar.play()
                    jugar()
                    print ("Iniciar juego") # # Mensaje de prueba para saber que el boton funciona
                # Verifica si se hizo clic en el boton "Configuracion"
                elif boton_config.collidepoint(evento.pos):
                    sonido_config.play()
                    menu_configuracion()
                    print("Abrir configuración")  # Mensaje de prueba para saber que el boton funciona
                # Verifica si se hizo clic en el boton "Top 10"
                elif boton_top.collidepoint(evento.pos):
                    sonido_top.play()
                    mostrar_top10() # Llamo a la funcion mostrar top10.
                    print("Mostrar TOP 10")  # Mensaje de prueba para saber que el boton funciona
                # Verifica si se hizo clic en el boton "Salir"
                elif boton_salir.collidepoint(evento.pos):
                    ejecutando = False  # Cierra el menu
        
        # Dibujo el fondo del menu principal.
        pantalla.blit(fondo, (0, 0)) # Coloca la imagen en la posicion (0 , 0)
        
        # Dibuja los botones del menú usando la función crear_boton
        boton_jugar = crear_boton(pantalla, "Jugar", 125, 150, 250, 60, COLOR_AZUL, COLOR_BLANCO, fuente)
        boton_config = crear_boton(pantalla, "Configuración", 125, 230, 250, 60, COLOR_AZUL, COLOR_BLANCO, fuente)
        boton_top = crear_boton(pantalla, "Top 10", 125, 310, 250, 60, COLOR_AZUL, COLOR_BLANCO, fuente)
        boton_salir = crear_boton(pantalla, "Salir", 125, 390, 250, 60, COLOR_ROJO, COLOR_BLANCO, fuente)
        
        # Actualizo la pantalla con los botones
        actualizar_pantalla_y_fps()
        
        # Controla la cantidad de fotogramas por segundo.
        reloj.tick(FPS)
    
    # Detiene la musica al salir.
    pygame.mixer.music.stop()   
    # Finaliza pygame cuando se sale del bucle.
    pygame.quit()
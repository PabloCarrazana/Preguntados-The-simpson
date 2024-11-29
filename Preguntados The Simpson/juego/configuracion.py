# Modulo para gestionar la configuracion del juego.
# (va a contener) Contiene la logica para activar/desactivar musica y ajustar su volumen.

import pygame
from Constantes import *
from funciones import *

def menu_configuracion():
    """
    Muestra el menu de configuracion del juego.
    permite activar/desactivar la musica y ajustar el volumen.
    """
    pantalla = inicializar_juego()
    
    # Fondo del menu de configuracion.
    fondo = pygame.image.load("juego/recursos\imagenes\configuracion.jpg") # Cargo la imagen de fondo.
    fondo = pygame.transform.scale(fondo, VENTANA) # Ajusto la imagen al tamaño de la Ventana.
    
    # Fuente para el texto.
    fuente = pygame.font.Font(None, 36) # Fuente predeterminada, tamaño 36.
    
    # Reloj para controlar FPS
    reloj = pygame.time.Clock()  # Permite controlar la tasa de refresco de la pantalla.
    
    # Variables para el estado de configuracio.
    musica_activada = True # Estado inicial de la musica: Activada.
    volumen = 0.5 # Volumen inicial de la musica (50%).
    
    # Cargar musica y establecer volumen inicial.
    pygame.mixer.music.load("juego/recursos\sonidos\menu.ogg") # Carga el archivo de musica.
    pygame.mixer.music.set_volume(volumen)  # Establece el volumen inicial.
    if musica_activada: # ? Si la musica esta activa
        pygame.mixer.music.play(-1)  # Reproduce la musica en bucle infinito.
    
        
    ejecutando = True # Variable para mantener el bucle de configuracion en ejecucion.
    while ejecutando: # Bucle principal del menu de configuracion.
        for evento in pygame.event.get(): # Itera sobre los eventos de pygame.
            if evento.type == pygame.QUIT: # Si se cierra la ventana.
                pygame.quit() # cierra correctamente pygame.
                return # Salir de la funcion, cerrando la ventana correctamente.
                
            # Detectar clics en los botones.
            if evento.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic con el mouse.
                if boton_musica.collidepoint(evento.pos): # Si se hace clic en el boton de musica.
                    musica_activada = not musica_activada # Alterna entre activado/desactivado.
                    if musica_activada: # Si ahora esta activada.
                        pygame.mixer.music.play(-1) # Se reproduce la musica en bucle.
                    else: # Si esta desactivada.
                        pygame.mixer.music.stop() # Se detiene la musica.
                elif boton_volumen_mas.collidepoint(evento.pos): # Si se hace clic en "Volumen +"
                    if volumen + 0.1 <= 1.0: # Verifico que no supere el maximo permitido (1.0).
                        volumen += 0.1 # incrementa el volumen
                    pygame.mixer.music.set_volume(volumen) # Aplico el nuevo volumen.
                elif boton_volumen_menos.collidepoint(evento.pos):  # Si se hace clic en "Volumen -"
                    if volumen - 0.1 >= 0.0: # Verifico que no sea menor al minimo permitido (0.0).
                        volumen -= 0.1 # Reduce el volumen.
                    pygame.mixer.music.set_volume(volumen) # Aplica el nuevo volumen.
                elif boton_volver.collidepoint(evento.pos): # Si se hace clic en "Volver".
                    return # Finaliza la funcion y regresa al menu principal.

        # Dibujar fondo.
        pantalla.blit(fondo, (0, 0)) # Dibuja la imagen de fondo en la ventana.
        
        # Dibujar texto del volumen.
        porcentaje_volumen = int(volumen * 100) # Convierto el volumen a un porcentaje (0-100).
        texto_volumen = f"Volumen:  {porcentaje_volumen} % " # Formatea el texto del volumen.
        texto_superficie = fuente.render(texto_volumen, True, COLOR_BLANCO) # Aparece el texto en blanco.
        pantalla.blit(texto_superficie, (10, 10)) # Dibuja el texto en la esquina superior izquierda.
        
        # Dibujar botones
        texto_musica = "Música: Activada" if musica_activada else "Música: Desactivada"  # Texto dinamico del boton de musica.
        boton_musica = crear_boton(pantalla, texto_musica, 125, 150, 250, 60, COLOR_AZUL, COLOR_BLANCO, fuente)  # Boton de msica.
        boton_volumen_mas = crear_boton(pantalla, "Volumen +", 125, 230, 250, 60, COLOR_VERDE, COLOR_BLANCO, fuente)  # Boton para subir volumen.
        boton_volumen_menos = crear_boton(pantalla, "Volumen -", 125, 310, 250, 60, COLOR_ROJO, COLOR_BLANCO, fuente)  # Boton para bajar volumen.
        boton_volver = crear_boton(pantalla, "Volver", 125, 390, 250, 60, COLOR_NEGRO, COLOR_BLANCO, fuente)  # Boton para volver al menu principal.
        
        # Actualizar pantalla.
        actualizar_pantalla_y_fps()
    
    pygame.quit()  # Finaliza pygame al salir del bucle.
# Logica para finalizar una partida.
# Módulo para pedir el nombre del jugador al terminar y guardar la partida.

import pygame
import json
import os
from datetime import datetime
from funciones import *
from Constantes import *

def guardar_partida(nombre, puntos):
    """
    Guarda los datos de la partida en el archivo JSON.
    
    Parámetros:
    - nombre: Nombre del jugador.
    - puntaje: Puntaje obtenido.
    """
    ruta_archivo = "partidas.json"
    nueva_partida = {
        "nombre": nombre,
        "puntaje": puntos,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Guarda la fecha actual.
    }

    # Leer datos existentes
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r") as archivo:
            contenido = archivo.read()
            datos = json.loads(contenido) if contenido.strip() else []
    else:
        datos = []

    # Agregar nueva partida
    datos.append(nueva_partida)

    # Guardar datos actualizados
    with open(ruta_archivo, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def pantalla_fin_juego(puntos):
    """
    Muestra la pantalla de fin de juego, guarda los datos y permite interactuar.
    
    Parámetros:
    - puntaje: Puntaje del jugador.
    - duracion: Duración del juego en segundos.
    """
    pantalla = inicializar_juego()
    fondo = pygame.image.load("juego/recursos\imagenes\Top10.jpg")
    fondo = pygame.transform.scale(fondo, VENTANA)

    pygame.mixer.music.load("juego/recursos\sonidos\jugar1.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    fuente = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 48)

    titulo = fuente_titulo.render("Fin del Juego", True, COLOR_NEGRO)
    instrucciones = fuente.render("Ingrese su nombre y presione 'Guardar':", True, COLOR_NEGRO)

    reloj = pygame.time.Clock()
    ejecutando = True
    nombre = ""

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip():
                    guardar_partida(nombre, puntaje, duracion)
                    pygame.mixer.music.stop()
                    return  # Regresa al menú o donde lo invoques
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15 and evento.unicode.isalnum():
                        nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_guardar.collidepoint(evento.pos):
                    # Detecta clic en el botón "Guardar"
                    if nombre.strip():  # Solo guarda si hay un nombre ingresado
                        guardar_partida(nombre, puntos) # Se guarda el nombre y el puntaja.
                        pygame.mixer.music.stop()
                        from juego.top_partidas import mostrar_top10
                        mostrar_top10()  # Redirige al Top 10
                        return
                    
                    
        # Dibujar fondo
        pantalla.blit(fondo, (0, 0))

        # Dibujar título e instrucciones
        pantalla.blit(titulo, (VENTANA[0] // 2 - titulo.get_width() // 2, 50))
        pantalla.blit(instrucciones, (50, 150))

        # Dibujar el cuadro de entrada del nombre
        cuadro_nombre = pygame.Rect(50, 200, 400, 50)
        pygame.draw.rect(pantalla, COLOR_NEGRO, cuadro_nombre, 2)
        texto_nombre = fuente.render(nombre, True, COLOR_NEGRO)
        pantalla.blit(texto_nombre, (cuadro_nombre.x + 10, cuadro_nombre.y + 10))

        # Crear y dibujar el botón de guardar
        boton_guardar = crear_boton(pantalla, "Guardar", 150, 300, 200, 60, COLOR_VERDE, COLOR_BLANCO, fuente)

        # Actualizar pantalla
        actualizar_pantalla_y_fps()
        reloj.tick(60)

import os
import csv
import pygame
import random 
from funciones import *  
from Constantes import *
from juego.fin_partidas import *
from juego.tiempo import *
from juego.comodines import *


# Función para cargar las preguntas desde un archivo CSV
def cargar_preguntas():
    # lista_datos = []
    # if os.path.exists("preguntas.csv"):
    #     with open("preguntas.csv", "r", encoding="utf-8") as archivo:
    #         archivo.readline()  # Salta la primera línea (cabecera)
    #         for linea in archivo:
    #             linea = linea.replace("\n", "")
    #             lista_valores = linea.split(",")
    #             diccionario = {
    #                 "pregunta": lista_valores[0],
    #                 "respuesta_1": lista_valores[1],
    #                 "respuesta_2": lista_valores[2],
    #                 "respuesta_3": lista_valores[3],
    #                 "respuesta_4": lista_valores[4],
    #                 "respuesta_correcta": int(lista_valores[5])
    #             }
    #             lista_datos.append(diccionario)
    # return lista_datos
    
    preguntas = []
    try:
        with open("preguntas.csv", mode="r", encoding="utf-8") as archivo_csv:
            lector = csv.reader(archivo_csv)
            for fila in lector:
                # Verificamos que la fila tenga al menos 6 columnas
                if len(fila) < 6:
                    print(f"Fila incompleta, se omite: {fila}")
                    continue  # Si la fila está incompleta, la ignoramos
                
                # Limpieza de espacios adicionales en cada valor
                pregunta = {
                    "pregunta": fila[0].strip(),
                    "respuesta_1": fila[1].strip(),
                    "respuesta_2": fila[2].strip(),
                    "respuesta_3": fila[3].strip(),
                    "respuesta_4": fila[4].strip()
                }
                
                # Intentamos convertir la respuesta correcta a un entero
                try:
                    pregunta["respuesta_correcta"] = int(fila[5].strip())
                except ValueError:
                    print(f"Error al convertir la respuesta correcta a entero: {fila[5]} no es un número.")
                    continue  # Si no se puede convertir, se omite la pregunta
                
                preguntas.append(pregunta)
                
    except FileNotFoundError:
        print("El archivo de preguntas no se encuentra en la ruta especificada.")
        return []

    return preguntas
    

# Función para mostrar texto en pantalla
def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # El ancho de un espacio
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height
        

# Función para mostrar un cuadro con los comodines en la esquina inferior derecha
def mostrar_comodines(surface, font, color_fondo, color_texto, posicion, comodines):
    """
    Muestra un cuadro con los comodines en la esquina inferior derecha.
    Parámetros:
        surface (pygame.Surface): Superficie de la pantalla.
        font (pygame.Font): Fuente para el texto.
        color_fondo (tuple): Color del fondo del cuadro.
        color_texto (tuple): Color del texto.
        posicion (tuple): Posición inicial del cuadro.
        comodines (list): Lista de comodines a mostrar.
    """
    margen = 10
    ancho, alto = 210, len(comodines) * 25 + 20  # Calcula el alto dinámico según los comodines
    x, y = posicion

    # Fondo del cuadro
    cuadro = pygame.Surface((ancho, alto))
    cuadro.fill(COLOR_VERDE)

    # Dibujar texto de comodines
    y_texto = 10  # Margen superior dentro del cuadro
    for comodin, tecla in comodines:
        texto = font.render(f"{comodin}: {tecla.upper()}", True, COLOR_NEGRO)
        cuadro.blit(texto, (10, y_texto))
        y_texto += 25  # Espaciado entre líneas

    # # Pegar el cuadro en la superficie principal
    # surface.blit(cuadro, (x, y - alto - margen))
    # Dibujar el cuadro en la pantalla principal
    surface.blit(cuadro, (x - ancho - margen, y - alto - margen))

def jugar():
    # Inicializo pygame y creo la ventana
    pantalla = inicializar_juego()
    
    # Cargo la imagen del fondo del juego
    fondo = pygame.image.load("juego/recursos/imagenes/jugar.png")
    fondo = pygame.transform.scale(fondo, VENTANA)
    
    # Sonidos para aciertos y errores
    sonido_acierto = pygame.mixer.Sound("juego/recursos\sonidos\Acierto.mp3")
    sonido_error = pygame.mixer.Sound("juego/recursos\sonidos\ouch.mp3")
    
    # Lista de música del juego
    lista_musica = [
        "juego/recursos/sonidos/jugar.ogg",  # Primer tema musical
        "juego/recursos/sonidos/jugar1.ogg"  # Segundo tema musical
    ]
    
    # Selecciono un tema aleatorio de la lista y lo reproduzco
    musica_actual = random.choice(lista_musica)
    pygame.mixer.music.load(musica_actual)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    

    # Configuración inicial
    puntos = 0
    vidas = 3
    aciertos_consecutivos = 0
    comodines_usados = {"bomba": False, "x2": False, "doble_chance": False, "pasar": False}  # Control de uso de comodines


    # Fuente para mostrar texto en pantalla
    fuente = pygame.font.Font(None, 36)
    
    
     # Cuadros de la pregunta y respuestas
    cuadro_pregunta = {}
    cuadro_pregunta["superficie"] = pygame.Surface((VENTANA[0] // 2 - 20, 150))  # Tamaño reducido
    cuadro_pregunta["superficie"].fill((255, 255, 255))  # Fondo blanco para la pregunta
    cuadro_pregunta["rectangulo"] = cuadro_pregunta["superficie"].get_rect()

    lista_respuestas = []
    for i in range(4):
        cuadro_respuesta = {}
        cuadro_respuesta["superficie"] = pygame.Surface((VENTANA[0] // 2 - 20, 50))  # Tamaño ajustado para respuestas
        cuadro_respuesta["superficie"].fill((255, 255, 0))  # Fondo amarillo
        cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
        lista_respuestas.append(cuadro_respuesta)
        
    # Cargar las preguntas y barajarlas #######
    lista_datos = cargar_preguntas()
    random.shuffle(lista_datos)
    indice_pregunta = 0  # Índice de la pregunta actual
    
    # Variables para el sistema del tiempo.
    TIEMPO_LIMITE = 15   # Tiempo maximo por pregunta en segundos.
    tiempo_inicio = iniciar_tiempo()  # Tiempo inicial de la primera pregunta

    # Bucle del juego
    corriendo = True
    while corriendo:
        # Calculamos el tiempo restante para responder.
        tiempo_restante = TIEMPO_LIMITE - tiempo_transcurrido(tiempo_inicio)
        
        # Verificar si se acabó el tiempo para la pregunta
        if tiempo_restante <= 0:
            vidas -= 1  # Resta una vida
            indice_pregunta += 1  # Avanza a la siguiente pregunta
            if indice_pregunta >= len(lista_datos):  # Reinicio de preguntas si es necesario
                indice_pregunta = 0
            pregunta_actual = lista_datos[indice_pregunta]  # Actualizar pregunta actual
            tiempo_inicio = iniciar_tiempo()  # Reiniciar el contador de tiempo para la nueva pregunta
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            # Detectar teclas de comodines
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_b and not comodines_usados["bomba"]:  # Bomba
                    comodines_usados["bomba"] = True
                    pregunta_actual = lista_datos[indice_pregunta]
                    respuestas = bomba(pregunta_actual)
                    print(f"Respuestas tras usar Bomba: {respuestas}")
                elif evento.key == pygame.K_x and not comodines_usados["x2"]:  # X2
                    comodines_usados["x2"] = True
                    puntos = x2(puntos)
                elif evento.key == pygame.K_d and not comodines_usados["doble_chance"]:  # Doble Chance
                    comodines_usados["doble_chance"] = True
                    print("Activaste Doble Chance")
                elif evento.key == pygame.K_p and not comodines_usados["pasar"]:  # Pasar
                    comodines_usados["pasar"] = True
                    indice_pregunta = pasar(indice_pregunta, len(lista_datos))
                    tiempo_inicio = iniciar_tiempo()
                
            #Definir el tamaño del cuadro de la pregunta (ajustado)
            ANCHO_CUADRO_PREGUNTA = VENTANA[0] // 2  # La mitad del ancho de la pantalla
            ALTO_CUADRO_PREGUNTA = 150  # Alto del cuadro de la pregunta (ajustable)
            
            # Definir el cuadro de la pregunta
            cuadro_pregunta["superficie"] = pygame.image.load("juego/recursos/imagenes/Fondo_pregunta.jpg")  # Carga de la imagen de fondo
            cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], (ANCHO_CUADRO_PREGUNTA, ALTO_CUADRO_PREGUNTA))  # Escala la imagen al tamaño del cuadro
            
            
            # Dibujo el fondo
            pantalla.blit(fondo, (0, 0))
            
            # Mostrar vidas y puntos en la pantalla
            texto_vidas = fuente.render(f"Vidas: {vidas}", True, COLOR_BLANCO)
            texto_puntos = fuente.render(f"Puntos: {puntos}", True, COLOR_BLANCO)
            texto_tiempo = fuente.render(f"Tiempo: {max(0, int(tiempo_restante))}", True, COLOR_BLANCO)
            pantalla.blit(texto_vidas, (10, 10))
            pantalla.blit(texto_puntos, (10, 50))
            pantalla.blit(texto_tiempo, (VENTANA[0] - texto_tiempo.get_width() - 10, 10))  # Tiempo en la esquina superior derecha
            
            # Mostrar la pregunta actual #######
            pregunta_actual = lista_datos[indice_pregunta]
            mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual["pregunta"], (20, 20), fuente, (0, 0, 0))
            
            # Dibujo el cuadro de la pregunta alineado a la izquierda (mitad de la pantalla)
            cuadro_pregunta["rectangulo"] = pantalla.blit(
                cuadro_pregunta["superficie"],
                (10, 90)  # Alineado a la izquierda debajo de vidas y puntos
            )
            
            
            # Dibujo las respuestas justo debajo del cuadro de la pregunta
            espaciado_respuestas = 10  # Espacio vertical entre respuestas
            posicion_inicial_respuestas = 250  # Ajuste para mover las respuestas hacia abajo

            # for i in range(4):
            #     lista_respuestas[i]["rectangulo"] = pantalla.blit(
            #         lista_respuestas[i]["superficie"],
            #         (10, posicion_inicial_respuestas + i * (lista_respuestas[i]["superficie"].get_height() + espaciado_respuestas))
            #     )
            
            #########
            for i in range(4): 
                lista_respuestas[i]["superficie"] = pygame.Surface((VENTANA[0] // 2 - 20, 50))  # Crear la superficie de la respuesta
                lista_respuestas[i]["superficie"].fill((255, 255, 0))  # Fondo amarillo para cada respuesta
                mostrar_texto(lista_respuestas[i]["superficie"], f"{pregunta_actual[f'respuesta_{i+1}']}", (5, 5), fuente, (0, 0, 0))  # Mostrar texto en cada respuesta
                lista_respuestas[i]["rectangulo"] = pantalla.blit(
                    lista_respuestas[i]["superficie"],
                    (10, posicion_inicial_respuestas + i * (lista_respuestas[i]["superficie"].get_height() + espaciado_respuestas))
                )

            # Manejo de eventos de clic (selección de respuestas)
            if evento.type == pygame.MOUSEBUTTONDOWN: # Si el jugador hace clic
                for i in range(4): # Verificamos si hizo clic en una de las respuestas.
                    if lista_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                        respuesta_seleccionada = i + 1
                        if respuesta_seleccionada == pregunta_actual["respuesta_correcta"]:
                            sonido_acierto.play()  # Reproducir sonido de acierto
                            lista_respuestas[i]["superficie"].fill(COLOR_VERDE)  # Cambiar a verde
                            puntos += 10  # Sumar puntos por respuesta correcta
                            aciertos_consecutivos += 1
                            if aciertos_consecutivos % 5 == 0:  # Ganar una vida cada 5 aciertos consecutivos
                                vidas += 1
                        else:
                            sonido_error.play()  # Reproducir sonido de error
                            lista_respuestas[i]["superficie"].fill(COLOR_ROJO)  # Cambiar a rojo
                            vidas -= 1  # Restar vida por respuesta incorrecta
                            
                        # Mostrar el cambio de color en el cuadro específico
                        pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])
                        mostrar_texto(
                            lista_respuestas[i]["superficie"],
                            pregunta_actual[f"respuesta_{i+1}"],
                            (5, 5),
                            fuente,
                            (0, 0, 0),
                             )  # Volver a dibujar el texto en el cuadro
                        

                        # Avanzar a la siguiente pregunta
                        indice_pregunta += 1
                        if indice_pregunta >= len(lista_datos):
                            indice_pregunta = 0  # Reiniciar las preguntas al llegar al final
                        pregunta_actual = lista_datos[indice_pregunta]
                        tiempo_inicio = iniciar_tiempo()  # Reinicio el tiempo
                        break
        
        
        # Mostrar el cuadro de comodines en la esquina inferior derecha
        mostrar_comodines(
            pantalla, fuente, COLOR_NEGRO, (0, 0, 0),
            (VENTANA[0] , VENTANA[1]), 
            [("Bomba", "b"), ("X2", "x"), ("Doble Chance", "d"), ("Pasar", "p")]
        )            

        ####################
        # Si se acaba el juego (vidas 0), redirigir a la pantalla de fin de juego
        if vidas <= 0:
            #from fin_partidas import pantalla_fin_juego
            pantalla_fin_juego(puntos)  # Pasar el puntaje a la pantalla de fin de juego
            return  # Salir de la función para terminar el juego    
        ####################    
            
        # Actualizar pantalla
        pygame.display.flip()
    
    pygame.mixer.music.stop()  # Detengo la música cuando termina el juego
    pygame.quit()

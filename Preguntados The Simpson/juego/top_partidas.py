# Aca se va hacer en manejo del top 10 de partidas.
# Muestra el TOP 10 de jugadores con mayor puntaje desde el archivo partidas.json.
import pygame
import json
import os # importo os para manejar archivos
from funciones import *
from Constantes import *

def cargar_top10(ruta_archivo = "partidas.json"):
    """
    Cargar las 10 mejores partidas desde un archivo JSON si existe y tiene datos validos.
    
    parametros:
    - ruta_archivo: Ruta del archivo JSON donde estan las partidas.
    
    retorno:
    - Lista con las 10 mejores partidas, ordenadas por puntaje mayor a menor.
    """
    
    if os.path.exists(ruta_archivo): # Verifico si el archivo existe.
        with open(ruta_archivo, "r") as archivo:
            contenido = archivo.read() # Lee todo el contenido del archivo.
            
            if contenido.strip(): # Verifico si el archivo no esta vacio.
                datos = json.loads(contenido) # Carga los datos JSON.
                
                # Ordeno las partidas por puntaje de mayor a menor con un algoritmo de burbujeo.
                n = len(datos)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if datos[j]["puntaje"] < datos[j + 1]["puntaje"]:
                            datos[j], datos[j + 1] = datos[j + 1], datos[j]
                
                return datos[:10] # Retorna solo las 10 mejores partidas.
            
            else:
                print("El archivo esta vacio..")
                return[] # Retorna una lista vacia si el archivo no tiene datos.
    
    else:
        print(f"El archivo {ruta_archivo} no existe..")
        return [] # Retornar una lista vacia si el archivo no existe.
    

def mostrar_top10():
    """
    Mostrar las 10 mejores partidas en pantalla.
    """
     # Inicializar la pantalla
    pantalla = inicializar_juego()
    
    # Fondo del Top 10
    fondo = pygame.image.load("juego/recursos\imagenes\Top10.jpg")
    fondo = pygame.transform.scale(fondo, VENTANA)
    
    # Música de fondo
    pygame.mixer.music.load("juego/recursos\sonidos\jugar1.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    # Cargar el Top 10
    ruta_archivo = "partidas.json" # Defino la ruta del archivo donde estan las partidas.
    top10 = cargar_top10(ruta_archivo) # Llamo a la funcion para cargar el top 10.
    
    # Fuente para el texto
    fuente = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 48)
    
    # Título del Top 10
    titulo = fuente_titulo.render("Top 10 Partidas", True, COLOR_NEGRO)
    
    # Dibujar botón "Volver"
    #boton_volver = crear_boton(pantalla, "Volver", 125, VENTANA[1] - 100, 250, 60, COLOR_NEGRO, COLOR_BLANCO, fuente)
    
    # Reloj para controlar FPS
    reloj = pygame.time.Clock()
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):  # Si clic en "Volver"
                    pygame.mixer.music.stop()  # Detener la música al volver
                    return  # Volver al menú principal
                
        # Dibujar fondo
        pantalla.blit(fondo, (0, 0))
        
        # Dibujar título
        pantalla.blit(titulo, (VENTANA[0] // 2 - titulo.get_width() // 2, 20))
        
        # if top10: # Si hay datos en el top10.
        #     print("Top 10 partidas: \n")
            
        #     # Recorro las partidas.
        #     posicion = 1 # Inicio el contador de posicion en 1.
        #     for partida in top10:
        #         nombre = partida["nombre"]
        #         puntaje = partida["puntaje"]
        #         fecha = partida["fecha"]
                
        #         print(f"{posicion}, {nombre} -  {puntaje}  ({"fecha"})") # Mostrar la partida
        #         posicion += 1 # Incrementa la posicion.
        if top10:
            posicion_y = 100  # Posición inicial vertical
            for indice, partida in enumerate(top10):
                texto = f"{indice + 1}. {partida['nombre']} - {partida['puntaje']} puntos ({partida['fecha']})"
                texto_renderizado = fuente.render(texto, True, COLOR_NEGRO)
                pantalla.blit(texto_renderizado, (0, posicion_y))
                posicion_y += 40  # Separación entre filas
        
        
        else:
            print("No hay partidas registradas aun..")
        
        
        # Dibujar botón "Volver"
        boton_volver = crear_boton(pantalla, "Volver", 125, VENTANA[1] - 100, 250, 60, COLOR_NEGRO, COLOR_BLANCO, fuente)
        
    
        
        # Actualizar pantalla
        actualizar_pantalla_y_fps()
        reloj.tick(60)
        
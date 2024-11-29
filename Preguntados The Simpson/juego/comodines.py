# Logica para los comodines.
# (Va) Implementa la lógica de los comodines (bomba, x2, etc.).

import random

def bomba(pregunta):
    """
    Elimina dos respuestas incorrectas dejando la correcta y una incorrecta.
    Parámetros:
        pregunta (dict): Diccionario con la pregunta y sus respuestas.
    Retorna:
        list: Lista con las respuestas que quedan después de usar el comodín.
    """
    correcta = pregunta[f"respuesta_{pregunta['respuesta_correcta']}"]
    respuestas_incorrectas = [
        pregunta[f"respuesta_{i}"]
        for i in range(1, 5)
        if i != pregunta["respuesta_correcta"]
    ]
    # Seleccionamos una respuesta incorrecta al azar
    incorrecta_mantenida = random.choice(respuestas_incorrectas)
    # Retornamos la correcta y la incorrecta seleccionada
    return [correcta, incorrecta_mantenida]


def x2(puntos):
    """
    Duplica los puntos obtenidos.
    Parámetros:
        puntos (int): Puntos obtenidos en la ronda.
    Retorna:
        int: Puntos duplicados.
    """
    return puntos * 2


def doble_chance(respuesta_seleccionada, respuesta_correcta):
    """
    Permite una segunda oportunidad si la primera respuesta es incorrecta.
    Parámetros:
        respuesta_seleccionada (int): Respuesta elegida por el jugador.
        respuesta_correcta (int): Respuesta correcta de la pregunta.
    Retorna:
        bool: True si acierta en el segundo intento, False si no.
    """
    if respuesta_seleccionada == respuesta_correcta:
        return True  # Acierto en el primer intento
    else:
        return None  # Permitir un segundo intento


def pasar(indice_pregunta, total_preguntas):
    """
    Salta a la siguiente pregunta.
    Parámetros:
        indice_pregunta (int): Índice de la pregunta actual.
        total_preguntas (int): Número total de preguntas.
    Retorna:
        int: Índice de la siguiente pregunta.
    """
    return (indice_pregunta + 1) % total_preguntas

from operator import pos

from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

DIRECCIONES : list[Direccion] = [NORTE, SUR, ESTE, OESTE]

#### Ejercicio 1

def tablero_bien_formado(t : Tablero) -> bool:
    bien_formado : bool = True
    if len(t) != ALTO:
        bien_formado = False
    for fila in t:
        if len(fila) != ANCHO:
            bien_formado = False    
    res : bool = bien_formado
    return res

def posicion_en_tablero(pos : Posicion) -> bool:
    res: bool = (0 <= pos.fila < ALTO) and (0 <= pos.columna < ANCHO)
    return res

def movimiento_bien_formado(m : Movimiento) -> bool:
    origen_valido : bool = posicion_en_tablero(m.origen)

    pasos_validos : bool = False
    if m.accion== MOVER_A_SECAS:
        pasos_validos = len(m.pasos) == 1
    elif m.accion== ARRASTRAR or m.accion== EMPUJAR:
        pasos_validos = len(m.pasos) == 2

    res : bool = origen_valido and pasos_validos
    return res
        
def juego_bien_formado(j : Juego) -> bool:
    res : bool = tablero_bien_formado(j.tablero) and 0 <= j.pasos_consumidos < MAX_PASOS
    return res

#### Ejercicio 2

def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    fila : int = pos.fila
    columna : int = pos.columna

    if d == NORTE:
        fila += 1
    elif d == SUR:
        fila -= 1
    elif d == ESTE:
        columna += 1
    elif d == OESTE:
        columna -= 1
    res : Posicion = Posicion(fila, columna)
    return res

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """Devuelve la casilla en la posición p del tablero t.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(p)

    Args:
        t (Tablero): El tablero de juego.
        p (Posicion): La posición a consultar en el tablero.

    Returns:
        Casilla: La casilla en la posición p.
    """

    posicion : Casilla = t[p.fila][p.columna]
    res : Casilla = posicion
    return res

def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """Indica si en la posición pos del tablero t hay una casilla vacía.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar en el tablero.

    Returns:
        True si hay una casilla vacía en pos, y False en caso contrario.
    """

    casilla : Casilla = casilla_en_posicion(t, pos)
    res : bool = casilla == VACIA

    return res

## -- FUNCIONES AUXILIARES  -- ##

def hay_pieza(t : Tablero, pos : Posicion) -> bool:
    """Indica si en la posición pos del tablero t hay una pieza.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar en el tablero.

    Returns:
        True si hay una pieza en pos, y False en caso contrario.
    """
    res : bool = not hay_casilla_vacia(t, pos)
    return res

def figura_en_posicion(t: Tablero, pos: Posicion) -> Figura:
    """Devuelve la figura de la pieza ubicada en la posición pos del tablero.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.

    Returns:
        Figura: La figura de la pieza en dicha posición.
    """
    casilla: Casilla = casilla_en_posicion(t, pos)
    res: Figura = casilla.figura
    return res


def color_en_posicion(t: Tablero, pos: Posicion) -> Color:
    """Devuelve el color de la pieza ubicada en la posición pos del tablero.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.

    Returns:
        Color: El color de la pieza en dicha posición.
    """
    casilla: Casilla = casilla_en_posicion(t, pos)
    res: Color = casilla.color
    return res

def hay_figura_de_color(t: Tablero, pos: Posicion, f: Figura, col: Color) -> bool:
    """Indica si en la posición pos del tablero t hay una pieza de la figura f y del color col.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar en el tablero.
        f (Figura): La figura de la pieza buscada.
        col (Color): El color de la pieza buscada.

    Returns:
        True si hay una pieza en pos con la figura f y el color col, y False en caso contrario.
    """
    res: bool = False
    
    if hay_pieza(t, pos):
        misma_figura: bool = figura_en_posicion(t, pos) == f
        mismo_color: bool = color_en_posicion(t, pos) == col
        res = misma_figura and mismo_color

    return res

def es_mas_fuerte(f1: Figura, f2: Figura) -> bool:
    """Indica si la figura f1 es más fuerte que la figura f2.

    PRE: f1 in FIGURAS and f2 in FIGURAS

    Args:
        f1 (Figura): La primera figura a comparar.
        f2 (Figura): La segunda figura a comparar.

    Returns:
        True si f1 es más fuerte que f2, y False en caso contrario.
    """
    res : bool = fuerza(f1) > fuerza(f2)
    return res

## -- CONTINUA EJERCICIO 2  -- ##

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    
    res : bool = False
    if hay_pieza(t, pos):
        res = color_en_posicion(t, pos) == col

    return res

## FUNCION AUXILIAR DE PIEZA ENEMIGA ##

def hay_pieza_enemiga(t : Tablero, pos : Posicion, col : Color) -> bool:
    res : bool = hay_pieza_de_color(t, pos, oponente(col))
    return res


#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    res : bool = hay_casilla_vacia(t, posicion_vecina_hacia(pos, d))
    return res

def es_vecino_valido(pos1 : Posicion, pos2 : Posicion) -> bool:
    """Indica si dos posiciones son vecinas válidas en el tablero.

    PRE: True

    Args:
        pos1 (Posicion): La primera posición.
        pos2 (Posicion): La segunda posición.

    Returns:
        True si las posiciones son vecinas válidas, y False en caso contrario.
    """
    res : bool = posicion_en_tablero(pos1) and posicion_en_tablero(pos2) and son_posiciones_vecinas(pos1, pos2)
    return res

def hay_pieza_vecina_de_color(t: Tablero, pos: Posicion, col: Color) -> bool:
    """Indica si en alguna posición vecina válida a pos hay una pieza del color col.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.
        col (Color): El color de la pieza buscada.

    Returns:
        True si hay una pieza vecina de color col, y False en caso contrario.    
    """
    res: bool = False
    i: int = 0
    
    while i < len(DIRECCIONES) and not res:
        pos_vecina: Posicion = posicion_vecina_hacia(pos, DIRECCIONES[i])
        
        if es_vecino_valido(pos, pos_vecina) and hay_pieza_de_color(t, pos_vecina, col):
            res = True
            
        i += 1
        
    return res

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    casilla : Casilla = casilla_en_posicion(t, pos)
    res : bool = hay_pieza_vecina_de_color(t, pos, casilla.color)
    return res

def hay_pieza_enemiga_vecina(t : Tablero, pos : Posicion) -> bool:
    casilla : Casilla = casilla_en_posicion(t, pos)
    color_oponente : Color = oponente(casilla.color)
    res : bool = hay_pieza_vecina_de_color(t, pos, color_oponente)
    return res

def es_enemiga_comparando_fuerza(t: Tablero, pos: Posicion, d: Direccion, buscar_mas_debil: bool) -> bool:
    """Indica si la pieza vecina en dirección d es enemiga y cumple la relación de fuerza buscada.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)
    """
    pos_vecina: Posicion = posicion_vecina_hacia(pos, d)
    res: bool = False

    if es_vecino_valido(pos, pos_vecina) and hay_pieza_enemiga(t, pos_vecina, color_en_posicion(t, pos)):
        casilla: Casilla = casilla_en_posicion(t, pos)
        casilla_vecina: Casilla = casilla_en_posicion(t, pos_vecina)
        if buscar_mas_debil:
            res = es_mas_fuerte(casilla.figura, casilla_vecina.figura)
        else:
            res = es_mas_fuerte(casilla_vecina.figura, casilla.figura)

    return res

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la dirección d desde pos hay una pieza enemiga de menor fuerza.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.
        d (Direccion): La dirección vecina a evaluar.

    Returns:
        True si hay una pieza enemiga de menor fuerza en la dirección d, False en caso contrario.
    """
    buscar_mas_debil: bool = True
    res: bool = es_enemiga_comparando_fuerza(t, pos, d, buscar_mas_debil)
    return res

def hay_pieza_enemiga_mas_fuerte_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la dirección d desde pos hay una pieza enemiga de mayor fuerza.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.
        d (Direccion): La dirección vecina a evaluar.

    Returns:
        True si hay una pieza enemiga de mayor fuerza en la dirección d, False en caso contrario.
    """
    buscar_mas_debil: bool = False
    res: bool = es_enemiga_comparando_fuerza(t, pos, d, buscar_mas_debil)
    return res

def es_vecino_enemigo(t : Tablero, pos1 : Posicion, pos2 : Posicion) -> bool:
    res : bool = es_vecino_valido(pos1, pos2) and hay_pieza_enemiga(t, pos2, color_en_posicion(t, pos1))
    return res

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """Indica si en alguna posición vecina válida a pos hay una pieza enemiga de mayor fuerza.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.

    Returns:
        True si hay al menos una pieza enemiga contigua con mayor fuerza, False en caso contrario.
    """
    casilla_actual: Casilla = casilla_en_posicion(t, pos)
    
    res: bool = False
    i: int = 0
    
    while i < len(DIRECCIONES) and not res:
        pos_vecina: Posicion = posicion_vecina_hacia(pos, DIRECCIONES[i])
        
        if es_vecino_enemigo(t, pos, pos_vecina):
            casilla_vecina: Casilla = casilla_en_posicion(t, pos_vecina)
            if es_mas_fuerte(casilla_vecina.figura, casilla_actual.figura):
                res = True
                
        i = i + 1
        
    return res

def hay_pieza_enemiga_mas_debil_vecina(t : Tablero, pos : Posicion) -> bool:
    """Indica si en alguna posición vecina válida a pos hay una pieza enemiga de menor fuerza.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and not hay_casilla_vacia(t, pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.

    Returns:
        True si hay al menos una pieza enemiga contigua con menor fuerza, False en caso contrario.
    """
    casilla_actual: Casilla = casilla_en_posicion(t, pos)
    
    res: bool = False
    i: int = 0
    
    while i < len(DIRECCIONES) and not res:
        pos_vecina: Posicion = posicion_vecina_hacia(pos, DIRECCIONES[i])
        
        if es_vecino_enemigo(t, pos, pos_vecina):
            casilla_vecina: Casilla = casilla_en_posicion(t, pos_vecina)
            if es_mas_fuerte(casilla_actual.figura, casilla_vecina.figura):
                res = True
                
        i = i + 1
        
    return res

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

#### Ejercicio 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    raise Exception("No implementado")

#### Ejercicio 5

def activar_trampas(t : Tablero) -> Tablero:
    raise Exception("No implementado")

#### Ejercicio 6

def realizar_movimiento(j : Juego, m : Movimiento) -> Juego:
    raise Exception("No implementado")

#### Ejercicio 7

def hay_ganador_determinado(j : Juego) -> bool:
    raise Exception("No implementado")

def ganador_del_juego(j : Juego) -> Color:
    raise Exception("No implementado")


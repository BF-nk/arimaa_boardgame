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
        res : bool = color_en_posicion(t, pos) == col

    return res

## FUNCION AUXILIAR DE PIEZA ENEMIGA ##

def hay_pieza_enemiga(t : Tablero, pos : Posicion, col : Color) -> bool:
    res : bool = hay_pieza_de_color(t, pos, oponente(col))
    return res


#### Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    res : bool = hay_casilla_vacia(t, posicion_vecina_hacia(pos, d))
    return res

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    res : bool = not hay_casilla_vacia(t, pos) and hay_pieza_de_color(t, pos, casilla_en_posicion(t, pos).color)
    return res

def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    raise Exception("No implementado")

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    raise Exception("No implementado")

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


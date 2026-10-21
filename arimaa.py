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

## LISTAS AUXILIARES
DIRECCIONES : list[Direccion] = [NORTE, SUR, ESTE, OESTE]
FIGURAS : list[Figura] = [ELEFANTE, CAMELLO, CABALLO, PERRO, GATO, CONEJO]

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
    """Devuelve la posición vecina a pos en la dirección d.
        PRE: posicion_en_tablero(pos) and d in DIRECCIONES

    Args:
        pos (Posicion): La posición de referencia.
        d (Direccion): La dirección hacia la que se busca la posición vecina.

    Returns:
        Posicion: La posición vecina a pos en la dirección d.
    """
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

def esPosicionVecinaHacia(pos1 : Posicion, pos2 : Posicion, d : Direccion) -> bool:
    """Indica si pos2 es la posición vecina a pos1 en la dirección d.

    PRE:
        posicion_en_tablero(pos1)
        posicion_en_tablero(pos2)
        d in DIRECCIONES

    Args:
        pos1 (Posicion): La posición de referencia.
        pos2 (Posicion): La posición a consultar.
        d (Direccion): La dirección hacia la que se busca la posición vecina.

    Returns:
        bool: True si pos2 es la posición vecina a pos1 en la dirección d, False en caso contrario.
    """
    casilla_vecina : Posicion = posicion_vecina_hacia(pos1, d)
    res : bool = (casilla_vecina == pos2)
    return res

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """Devuelve la posición p de una casilla en el tablero t

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(t)

    
    """
    res : Casilla = t[p.fila][p.columna]
    return res

def hay_casilla_vacia(t: Tablero, pos: Posicion) -> bool:
    """Indica si la casilla en la posición pos está vacía.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición a consultar.

    Returns:
        bool: True si la casilla está vacía, False en caso contrario.
    """
    casilla: Casilla = casilla_en_posicion(t, pos)
    res: bool = (casilla == VACIA)
    return res

def hayFiguraDeColor(t : Tablero, pos : Posicion, f : Figura, col : Color) -> bool:
    posicion_valida : bool = posicion_en_tablero(pos)
    
    res : bool = False
    if posicion_valida:
        casilla : Casilla = casilla_en_posicion(t, pos)
        res = not hay_casilla_vacia(t, pos) and casilla.figura == f and casilla.color == col

    return res

def hayPieza(t: Tablero, pos: Posicion) -> bool:
    i : int = 0
    res : bool = False
    while i < len(FIGURAS) and not res:
        f : Figura = FIGURAS[i]
        res = hayFiguraDeColor(t, pos, f, DORADO) or hayFiguraDeColor(t, pos, f, PLATEADO)    
        i += 1
    return res

def hayPiezaDeColor(t: Tablero, pos : Posicion, col : Color) -> bool:

    i : int = 0
    res : bool = False
    while i < len(FIGURAS) and not res:
        f : Figura = FIGURAS[i]
        res : bool = hayFiguraDeColor(t, pos, f, col)
        i += 1
            
    return res

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    res : bool = hayPiezaDeColor(t, pos, col)
    return res

#### Ejercicio 3

def hayCasillaVaciaHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    posicion_vecina : Posicion = posicion_vecina_hacia(pos, d)
    posicion_valida : bool = posicion_en_tablero(posicion_vecina)
    res : bool = False
    if posicion_valida:
        res : bool = hay_casilla_vacia(t, posicion_vecina)
    return res

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    res : bool = hayCasillaVaciaHacia(t, pos, d)
    return res

def hayPiezaAmigaHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    color_pieza : Color = casilla_en_posicion(t, pos).color
    posicion_vecina : Posicion = posicion_vecina_hacia(pos, d)
    res : bool = hayPiezaDeColor(t, posicion_vecina, color_pieza)
    return res

def hayPiezaAmigaVecina(t : Tablero, pos : Posicion) -> bool:
    res : bool = False
    i : int = 0
    while i < len(DIRECCIONES) and not res:
        d : Direccion = DIRECCIONES[i]
        res : bool = hayPiezaAmigaHacia(t, pos, d)
        i += 1
    return res

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    res : bool = hayPiezaAmigaVecina(t, pos)
    return res

def esMasFuerte(f1 : Figura, f2 : Figura) -> bool:
    res : bool = fuerza(f1) > fuerza(f2)
    return res

def hayPiezaEnemigaMasDebilHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    posicion_enemiga : Posicion = posicion_vecina_hacia(pos, d) #hayFiguraDeColor se fija si es una pos valida
    color_enemigo : Color = oponente(casilla_en_posicion(t, pos).color)
    figura_propia : Figura = casilla_en_posicion(t, pos).figura

    i : int = 0
    while i < len(FIGURAS):
        figura_enemiga : Figura = FIGURAS[i]

        hay_enemiga : bool = hayFiguraDeColor(t, posicion_enemiga, figura_enemiga, color_enemigo)
        es_mas_fuerte : bool = esMasFuerte(figura_enemiga, figura_propia)

        i += 1

    res : bool = hay_enemiga and es_mas_fuerte
    return res


def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    res : bool = hayPiezaEnemigaMasDebilHacia(t, pos, d)
    return res

def hayPiezaEnemigaMasFuerteHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    posicion_enemiga : Posicion = posicion_vecina_hacia(pos, d) #hayFiguraDeColor se fija si es una pos valida
    color_enemigo : Color = oponente(casilla_en_posicion(t, pos).color)
    figura_propia : Figura = casilla_en_posicion(t, pos).figura

    i : int = 0
    while i < len(FIGURAS):
        figura_enemiga : Figura = FIGURAS[i]

        hay_enemiga : bool = hayFiguraDeColor(t, posicion_enemiga, figura_enemiga, color_enemigo)
        es_mas_fuerte : bool = esMasFuerte(figura_propia, figura_enemiga)

        i += 1

    res : bool = hay_enemiga and es_mas_fuerte
    return res

def hayPiezaEnemigaMasFuerteVecina(t : Tablero, pos : Posicion):
    i : int = 0
    res : bool = False
    while i < len(DIRECCIONES) and not res:
        d : Direccion = DIRECCIONES[i]
        res = hayPiezaEnemigaMasFuerteHacia(t, pos, d)
    return res

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    res : bool = hayPiezaEnemigaMasFuerteVecina(t, pos)
    return res

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    res : bool = hayPieza(t, pos) and hayPiezaEnemigaMasFuerteVecina(t, pos) and (not hayPiezaAmigaVecina(t, pos))
    return res

#### Ejercicio 4
##AUX 1 (veo si la direccion es valida)
def es_una_direccion_valida(f:Figura, c: Color, d: Direccion) -> bool:
    res:bool = True
    if f == CONEJO:
        if (c== DORADO) and (d== SUR):
            res= False
        elif (c== PLATEADO) and (d==NORTE):
            res = False
    return res 
    ##AUX2 (una veo si esa posicion es efectivamente valida y a su vez chequeo que el espacio vecino
    ##       a cual se traslada esta libre)
         
def direccion_de_movimiento_habilitada(t: Tablero, pos: Posicion, d:Direccion) -> bool:
    pieza: Casilla = casilla_en_posicion(t,pos)
    pos_vecina : Posicion = posicion_vecina_hacia(pos,d)
    direccion_permitida: bool = es_una_direccion_valida (pieza.figura, pieza.color, d)
    casilla_libre: bool = posicion_en_tablero(pos_vecina) and hay_casilla_vacia(t,pos_vecina)
    return direccion_permitida and casilla_libre
    
    
def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    pasos_suficientes: bool = (j.pasos_consumidos + len(m.pasos)) <= MAX_PASOS


    

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


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
    """Indica si el tablero t cumple con la estructura y dimensiones bien formadas (8x8).

    PRE: True

    Args:
        t (Tablero): El estado del tablero a evaluar.

    Returns:
        bool: True si el tablero está bien formado, y False en caso contrario.
    """
    bien_formado : bool = True
    if len(t) != ALTO:
        bien_formado = False
    for fila in t:
        if len(fila) != ANCHO:
            bien_formado = False    
    res : bool = bien_formado
    return res

def posicion_en_tablero(pos : Posicion) -> bool:
    """Indica si la posición pos se encuentra dentro de los límites válidos del tablero (8x8).

    PRE: True

    Args:
        pos (Posicion): La posición a evaluar.

    Returns:
        bool: True si la posición está dentro del tablero, y False en caso contrario.
    """
    res: bool = (0 <= pos.fila < ALTO) and (0 <= pos.columna < ANCHO)
    return res

def movimiento_bien_formado(m : Movimiento) -> bool:
    """Indica si la estructura del movimiento m es válida en origen, cantidad de pasos y tipo de acción.

    PRE: True

    Args:
        m (Movimiento): El movimiento a evaluar.

    Returns:
        bool: True si el movimiento está bien formado, y False en caso contrario.
    """
    origen_valido : bool = posicion_en_tablero(m.origen)

    pasos_validos : bool = False
    if m.accion== MOVER_A_SECAS:
        pasos_validos = len(m.pasos) == 1
    elif m.accion== ARRASTRAR or m.accion== EMPUJAR:
        pasos_validos = len(m.pasos) == 2

    res : bool = origen_valido and pasos_validos
    return res
        
def juego_bien_formado(j : Juego) -> bool:
    """Indica si el estado del juego j está bien formado en su tablero, turno y cantidad de pasos consumidos.

    PRE: True

    Args:
        j (Juego): El estado del juego a evaluar.

    Returns:
        bool: True si el juego está bien formado, y False en caso contrario.
    """
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

    Args:
        t (Tablero): El tablero del juego.
        p (Posición): La posición de la casilla.
    
    Returns:
        Casilla: La casilla en el tablero t asociada a la posición p.
    
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
    """Indica si la posición pos está en el tablero y contiene una figura f de color col.

    PRE:
        tablero_bien_formado(t)

    Args:
        t (Tablero): El estado actual del tablero.
        pos (Posicion): La posición a consultar.
        f (Figura): La figura a verificar.
        col (Color): El color de la pieza a verificar.

    Returns:
        bool: True si la posición es válida y contiene la figura f de color col, y False en caso contrario.
    """
    posicion_valida : bool = posicion_en_tablero(pos)
    
    res : bool = False
    if posicion_valida:
        casilla : Casilla = casilla_en_posicion(t, pos)
        res = not hay_casilla_vacia(t, pos) and casilla.figura == f and casilla.color == col

    return res

def hayPieza(t: Tablero, pos: Posicion) -> bool:
    """Indica si existe alguna pieza (de cualquier figura y color) en la posición pos del tablero.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado actual del tablero.
        pos (Posicion): La posición a consultar.

    Returns:
        bool: True si hay una pieza ocupando la posición pos, y False en caso contrario.
    """
    i : int = 0
    res : bool = False
    while i < len(FIGURAS) and not res:
        f : Figura = FIGURAS[i]
        res = hayFiguraDeColor(t, pos, f, DORADO) or hayFiguraDeColor(t, pos, f, PLATEADO)    
        i += 1
    return res

def hayPiezaDeColor(t: Tablero, pos : Posicion, col : Color) -> bool:
    """Indica si en la posición pos del tablero hay alguna pieza que pertenezca al color col.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado actual del tablero.
        pos (Posicion): La posición a consultar.
        col (Color): El color a verificar.

    Returns:
        bool: True si la posición pos contiene una pieza del color col, y False en caso contrario.
    """

    i : int = 0
    res : bool = False
    while i < len(FIGURAS) and not res:
        f : Figura = FIGURAS[i]
        res : bool = hayFiguraDeColor(t, pos, f, col)
        i += 1
            
    return res

def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """Determina si la posición pos del tablero contiene una pieza correspondiente al color col.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado actual del tablero.
        pos (Posicion): La posición a consultar.
        col (Color): El color a verificar (DORADO o PLATEADO).

    Returns:
        bool: True si en pos se encuentra una pieza de color col, y False en caso contrario.
    """
    res : bool = hayPiezaDeColor(t, pos, col)
    return res

#### Ejercicio 3

def hayCasillaVaciaHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la dirección d desde la posición pos existe una casilla dentro del tablero que esté vacía.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de origen.
        d (Direccion): La dirección hacia la cual evaluar.

    Returns:
        bool: True si la casilla vecina está dentro del tablero y se encuentra vacía, y False en caso contrario.
    """

    posicion_vecina : Posicion = posicion_vecina_hacia(pos, d)
    posicion_valida : bool = posicion_en_tablero(posicion_vecina)
    res : bool = False
    if posicion_valida:
        res : bool = hay_casilla_vacia(t, posicion_vecina)
    return res

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Determina si existe una casilla vacía en la dirección d contigua a pos.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de origen.
        d (Direccion): La dirección a evaluar.

    Returns:
        bool: True si la posición vecina en dirección d está dentro del tablero y vacía, y False en caso contrario.
    """
    res : bool = hayCasillaVaciaHacia(t, pos, d)
    return res

def hayPiezaAmigaHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la posición vecina hacia la dirección d hay una pieza del mismo color que la de pos.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza propia.
        d (Direccion): La dirección ortogonal a evaluar.

    Returns:
        bool: True si en la dirección d se encuentra una pieza amiga, y False en caso contrario.
    """
    color_pieza : Color = casilla_en_posicion(t, pos).color
    posicion_vecina : Posicion = posicion_vecina_hacia(pos, d)
    res : bool = hayPiezaDeColor(t, posicion_vecina, color_pieza)
    return res

def hayPiezaAmigaVecina(t : Tablero, pos : Posicion) -> bool:
    """Verifica si la pieza en la posición pos tiene al menos una pieza del mismo color en alguna dirección adyacente.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza a consultar.

    Returns:
        bool: True si existe alguna pieza amiga en las casillas vecinas, y False en caso contrario.
    """
    res : bool = False
    i : int = 0
    while i < len(DIRECCIONES) and not res:
        d : Direccion = DIRECCIONES[i]
        res : bool = hayPiezaAmigaHacia(t, pos, d)
        i += 1
    return res

def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    """Indica si la pieza ubicada en pos cuenta con al menos una pieza amiga adyacente.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza a verificar.

    Returns:
        bool: True si la pieza en pos tiene alguna pieza amiga vecina, y False en caso contrario.
    """
    res : bool = hayPiezaAmigaVecina(t, pos)
    return res

def esMasFuerte(f1 : Figura, f2 : Figura) -> bool:
    """Indica si la figura f1 tiene estrictamente mayor fuerza que la figura f2.

    PRE:
        f1, f2 in FIGURAS

    Args:
        f1 (Figura): La primera figura.
        f2 (Figura): La segunda figura a comparar.

    Returns:
        bool: True si la fuerza de f1 es mayor que la de f2, y False en caso contrario.
    """
    res : bool = fuerza(f1) > fuerza(f2)
    return res

def hayPiezaEnemigaMasDebilHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la dirección d desde pos hay una pieza del oponente con estrictamente menor fuerza que la propia.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza propia.
        d (Direccion): La dirección hacia la cual evaluar.

    Returns:
        bool: True si en la dirección d existe una pieza enemiga más débil, y False en caso contrario.
    """
    posicion_enemiga : Posicion = posicion_vecina_hacia(pos, d) #hayFiguraDeColor se fija si es una pos valida
    color_enemigo : Color = oponente(casilla_en_posicion(t, pos).color)
    figura_propia : Figura = casilla_en_posicion(t, pos).figura
    res : bool = False
    i : int = 0
    while i < len(FIGURAS) and not res:
        figura_enemiga : Figura = FIGURAS[i]

        hay_enemiga : bool = hayFiguraDeColor(t, posicion_enemiga, figura_enemiga, color_enemigo)
        es_mas_fuerte : bool = esMasFuerte(figura_propia, figura_enemiga)
        res = hay_enemiga and es_mas_fuerte
        i += 1

    
    return res


def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Determina si existe una pieza enemiga de menor jerarquía/fuerza en la dirección d desde pos.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza a verificar.
        d (Direccion): La dirección a consultar.

    Returns:
        bool: True si la casilla vecina en dirección d tiene una pieza enemiga más débil, y False en caso contrario.
    """
    res : bool = hayPiezaEnemigaMasDebilHacia(t, pos, d)
    return res

def hayPiezaEnemigaMasFuerteHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si en la dirección d desde pos hay una pieza del oponente con estrictamente mayor fuerza que la propia.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza propia.
        d (Direccion): La dirección hacia la cual evaluar.

    Returns:
        bool: True si en la dirección d existe una pieza enemiga más fuerte, y False en caso contrario.
    """
    posicion_enemiga : Posicion = posicion_vecina_hacia(pos, d) #hayFiguraDeColor se fija si es una pos valida
    color_enemigo : Color = oponente(casilla_en_posicion(t, pos).color)
    figura_propia : Figura = casilla_en_posicion(t, pos).figura

    i : int = 0
    res : bool = False
    while i < len(FIGURAS) and not res:
        figura_enemiga : Figura = FIGURAS[i]

        hay_enemiga : bool = hayFiguraDeColor(t, posicion_enemiga, figura_enemiga, color_enemigo)
        es_mas_fuerte : bool = esMasFuerte(figura_enemiga, figura_propia)
        res = hay_enemiga and es_mas_fuerte

        i += 1

    return res

def hayPiezaEnemigaMasFuerteVecina(t : Tablero, pos : Posicion):
    """Verifica si la pieza en pos se encuentra adyacente a al menos una pieza del oponente estrictamente más fuerte.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza a consultar.

    Returns:
        bool: True si existe alguna pieza enemiga más fuerte en las casillas vecinas, y False en caso contrario.
    """
    i : int = 0
    res : bool = False
    while i < len(DIRECCIONES) and not res:
        d : Direccion = DIRECCIONES[i]
        res = hayPiezaEnemigaMasFuerteHacia(t, pos, d)
        i+=1
    return res

def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """Determina si la pieza en pos tiene alguna pieza enemiga de mayor fuerza en sus posiciones contiguas.

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
        hayPieza(t, pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición de la pieza a consultar.

    Returns:
        bool: True si hay al menos una pieza enemiga más fuerte vecina, y False en caso contrario.
    """
    res : bool = hayPiezaEnemigaMasFuerteVecina(t, pos)
    return res

def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    """Determina si la pieza en la posición pos está congelada (tiene una pieza enemiga más fuerte vecina y ninguna amiga vecina).

    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)

    Args:
        t (Tablero): El estado del tablero.
        pos (Posicion): La posición a consultar.

    Returns:
        bool: True si hay una pieza en pos y está congelada, y False en caso contrario.
    """
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

##AUX3 realizar accion (verificamos primero que pueda efectivamente realizar alguno de esos movimientos con las siguentes auxiliares:)
def puede_mover_a_secas(t:Tablero, pos: Posicion, d: Direccion) -> bool:
    res: bool = hayCasillaVaciaHacia(t ,pos, d)
    return res
##Hago la funcion opuesta, que devuelve la direccion opuesta a la dada)

def puede_arrastrar(t:Tablero, pos: Posicion, d :Direccion, d_arrastre: Direccion) -> bool:
    res:bool = hayCasillaVaciaHacia(t, pos, d) and hay_pieza_enemiga_mas_debil_hacia(t, pos, opuesta(d_arrastre)) 
    return res
def puede_empujar(t:Tablero, pos: Posicion, d: Direccion, d_empuje: Direccion) -> bool:
    pos_enemiga: Posicion = posicion_vecina_hacia(pos, d)
    res: bool = posicion_en_tablero(pos_enemiga) and hayCasillaVaciaHacia(t, pos_enemiga, d_empuje) and hay_pieza_enemiga_mas_debil_hacia(t, pos, d)
    return res 

def puede_realizar_accion(t: Tablero, m: Movimiento) -> bool:
    """Indica si la acción que se indica en Movimiento m puede realizarse en el tablero t.
    PRE: 
        tablero_bien_formado(t)
        movimiento_bien_formado(m)
        posicion_en_tablero(m.origen)
    ARGS:
        t (Tablero): El tablero de juego.
        m (Movimiento): El movimiento o accion que se desea verificar. 
    Returns:
        bool: True si la accion puede realizarse, False en caso contrario.
    """
    res: bool = False 
    if m.accion == MOVER_A_SECAS:
        res = puede_mover_a_secas(t, m.origen, m.pasos[0]) 
    elif m.accion == ARRASTRAR:
        res = puede_arrastrar(t, m.origen, m.pasos[0], m.pasos[1])
    else:
        res = puede_empujar(t, m.origen, m.pasos[0], m.pasos[1])
    return res 

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    """Indica si el movimiento m puede realizarse en el juego j.
    PRE:
        juego_bien_formado(j)
        movimiento_bien_formado(m)
        posicion_en_tablero(m.origen)
    ARGS:
        j (Juego): El juego en el que se desea realizar el movimiento( donde el juego incluye el tablero, turno y pasos consumidos).
        m (Movimiento): El movimiento que se pretende o quiere realizar. 
    Returns:
        bool: True si el movimiento puede realizarse, False en caso contrario.
    """
    pasos_por_turno: bool = (j.pasos_consumidos + len(m.pasos)) <= MAX_PASOS
    no_pieza_congelada: bool = not hay_pieza_congelada(j.tablero, m.origen)
    res: bool = (hay_pieza_de_color(j.tablero, m.origen, j.turno) and no_pieza_congelada and direccion_de_movimiento_habilitada(j.tablero, m.origen, m.pasos[0]) and pasos_por_turno and puede_realizar_accion(j.tablero, m))
    return res 



    

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


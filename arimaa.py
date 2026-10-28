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

def hayPiezaEnemigaMasFuerteVecina(t : Tablero, pos : Posicion) -> bool:
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

def esDireccionHabilitadaParaFiguraDeColor(f : Figura, col : Color, d : Direccion) -> bool:
    """Indica si la dirección d es válida para la figura f de color col, considerando las restricciones específicas de movimiento.
    PRE:
        True
    Args: 
        f (Figura): La figura de la pieza que se desea mover.
        col (Color): El color de la figura.
        d (Direccion): La dirección de movimiento.
    Returns:
        bool: True si la dirección es válida para la figura y color dados, False en caso contrario.
    """
    res : bool = True
    if f == CONEJO and col == DORADO and d == SUR:
        res = False
    elif f == CONEJO and col == PLATEADO and d == NORTE:
        res = False
    return res

def direccionDeMovimientoHabilitada(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """Indica si el movimiento en la dirección d es válido para la pieza en la posición pos.
    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición de la pieza.
        d (Direccion): La dirección de movimiento.
    Returns:
        bool: True si la dirección es válida para el movimiento, False en caso contrario.
    """
    casillero : Casilla = casilla_en_posicion(t, pos)
    f : Figura = casillero.figura
    col : Color = casillero.color
    res : bool = hayFiguraDeColor(t, pos, f, col) and esDireccionHabilitadaParaFiguraDeColor(f, col, d)
    return res

##AUX3 realizar accion (verificamos primero que pueda efectivamente realizar alguno de esos movimientos con las siguentes auxiliares:)
def puedeMoverASecas(t:Tablero, pos: Posicion, d: Direccion) -> bool:
    """Indica si una pieza ubicada en la posición pos puede realizar un movimiento simple (moverse a secas) en la dirección d.
    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
    Args: 
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición de la pieza que se mueve.
        d (Direccion): La dirección hacia la cual se desea mover la pieza.
    Returns:
        bool: True si la casilla de destino en la dirección d está vacía y la pieza puede moverse a secas hacia ella, False en caso contrario.
    
    """
    res: bool = hayCasillaVaciaHacia(t ,pos, d)
    return res

def puedeArrastrar(t:Tablero, pos: Posicion, d :Direccion, d_arrastre: Direccion) -> bool:
    """Indica si una pieza ubicada en la posicion pos puede realizar un movimiento de arrastre en la dirección d, arrastrando a una pieza enemiga hacia la dirección opuesta a d_arrastre.
    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
    Args:
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición de la pieza que se mueve.
        d (Direccion): La dirección hacia la cual se desea mover la pieza principal.
        d_arrastre (Direccion): La dirección en la que se arrastra la pieza enemiga.
    Returns:
        bool: True si se cumplen las condiciones casilla vacía hacia la dirección d y hay una pieza enemiga más débil en la dirección opuesta a d_arrastre, False en caso contrario.
    """
    direccion_enemigo : Direccion = opuesta(d_arrastre)
    res:bool = hayCasillaVaciaHacia(t, pos, d) and hayPiezaEnemigaMasDebilHacia(t, pos, direccion_enemigo) 
    return res

def puedeEmpujar(t:Tablero, pos: Posicion, d: Direccion, d_empuje: Direccion) -> bool:
    """Indica si una pieza ubicada en la posición pos puede empujar a una pieza enemiga hacia la dirección d_empuje.
    PRE:
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
    Args: 
        t (Tablero): El tablero de juego.
        pos (Posicion): La posición de la pieza que empuja.
        d (Direccion): La dirección hacia la cual se encuentra la pieza enemiga a empujar.
        d_empuje (Direccion): La dirección hacia la cual se empuja a la pieza enemiga.
    Returns:
        bool: True si hay una pieza enemiga más débil en la dirección d y la casilla vecina en la dirección d_empuje está vacía, False en caso contrario.
    
    """
    pos_enemiga: Posicion = posicion_vecina_hacia(pos, d)
    res: bool = hayPiezaEnemigaMasDebilHacia(t, pos, d) and hayCasillaVaciaHacia(t, pos_enemiga, d_empuje)
    return res 

def puedeRealizarAccion(t: Tablero, m: Movimiento) -> bool:
    """Indica si la acción que se indica en Movimiento m puede realizarse en el tablero t.
    PRE: 
        tablero_bien_formado(t)
        movimiento_bien_formado(m)
        posicion_en_tablero(m.origen)
    Args:
        t (Tablero): El tablero de juego.
        m (Movimiento): El movimiento o accion que se desea verificar. 
    Returns:
        bool: True si la accion puede realizarse, False en caso contrario.
    """
    es_mover_a_secas : bool = m.accion == MOVER_A_SECAS
    es_arrastrar : bool = m.accion == ARRASTRAR

    res: bool = False 
    if es_mover_a_secas:
        res = puedeMoverASecas(t, m.origen, m.pasos[0]) 
    elif es_arrastrar:
        res = puedeArrastrar(t, m.origen, m.pasos[0], m.pasos[1])
    else:
        res = puedeEmpujar(t, m.origen, m.pasos[0], m.pasos[1])
    return res 

def puedeRealizarMovimiento(j : Juego, m : Movimiento) -> bool:
    """Indica si el movimiento m puede realizarse en el juego j.
    PRE: 
        juego_bien_formado(j)
        movimiento_bien_formado(m)
        posicion_en_tablero(m.origen)
    Args: 
        j (Juego): El juego en el que se desea realizar el movimiento( donde el juego incluye el tablero, turno y pasos consumidos).
        m (Movimiento): El movimiento que se pretende o quiere realizar.
    Returns:
        bool: True si el movimiento puede realizarse, False en caso contrario.
    """
    
    t : Tablero = j.tablero
    pos : Posicion = m.origen
    col : Color = j.turno
    d : Direccion = m.pasos[0]
    pasos_consumidos : int = j.pasos_consumidos
    quedan_pasos : bool = pasos_consumidos + len(m.pasos) <= MAX_PASOS

    res : bool = hayPiezaDeColor(t, pos, col) and (not hay_pieza_congelada(t, pos)) and direccionDeMovimientoHabilitada(t, pos, d) and quedan_pasos and puedeRealizarAccion(t, m)
    return res

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:
    """Indica si el movimiento m puede realizarse en el juego j.
    PRE:
        juego_bien_formado(j)
        movimiento_bien_formado(m)
        posicion_en_tablero(m.origen)
    Args:
        j (Juego): El juego en el que se desea realizar el movimiento( donde el juego incluye el tablero, turno y pasos consumidos).
        m (Movimiento): El movimiento que se pretende o quiere realizar. 
    Returns:
        bool: True si el movimiento puede realizarse, False en caso contrario.
    """
    res: bool = puedeRealizarMovimiento(j, m)
    return res 

#### Ejercicio 5

def copiarTablero(t0 : Tablero) -> Tablero:
    """ Devuelve una copia del tablero ingresado(t0) para evitar modificar el original.
    PRE: tablero_bien_formado(t0)
    Args:
        t0 (Tablero): El tablero original el cual se desea copiar
    Returns:
        Tablero: Una copia identica del tablero original t0.
    """
    res : Tablero = []
    for fila in t0:
        res.append(fila.copy())
    return res

def sacarPieza(t0 : Tablero, pos : Posicion) -> Tablero :
    """ Devuelve un tablero nuevo en la cual la pieza ubicada en la posicion pos ha sido removida
    PRE:
        tablero_bien_formado(t0)
        posicion_en_tablero(pos) 
    Args:
        t0 (Tablero): El tablero original del cual se desea remover la pieza.
        pos (Posicion): La posicion de la casilla donde se encuentra la pieza que se desea remover.
    Returns:
        Tablero: Un tablero nuevo en el cual la pieza ubicada en pos ha sido removida.
    """

    res : Tablero = copiarTablero(t0)
    res[pos.fila][pos.columna] = VACIA
    return res

def activarTrampa(t: Tablero, pos: Posicion) -> Tablero:
    """Verifica si la casilla en trampa pos debe activarse, en caso de que haya una pieza en ella sin piezas amigas vecinas, la pieza es removida del tablero.
    PRE: 
        tablero_bien_formado(t)
        posicion_en_tablero(pos)
    Args: 
        t (Tablero): El tablero sobre el cual se activa la trampa.
        pos (Posicion): La posición de la casilla trampa que se desea evaluar.
    Returns:
        Tablero: el tablero resultante después de haber evaluado la trampa.
    
    
    """
  
    res : Tablero = copiarTablero(t)
    if not hay_casilla_vacia(t, pos) and not hay_pieza_amiga_vecina(t, pos):
        res = sacarPieza(t, pos)
    return res

def activarTodasLasTrampas(t : Tablero) -> Tablero:
    """Aplica la activacion de trampas sobre todas las posiciones trampa del tablero
     PRE:
        tablero_bien_formado(t)
    Args:
        t (Tablero): El tablero sobre el cual se activan las trampas.
    Returns:
        Tablero: Un tablero nuevo con todas las trampas activadas.
        
        
        """
    


    tablero_con_trampas_activas : Tablero = copiarTablero(t)
    for posicion_trampa in POSICIONES_TRAMPA:
        tablero_con_trampas_activas = activarTrampa(tablero_con_trampas_activas, posicion_trampa)
    return tablero_con_trampas_activas

def activar_trampas(t: Tablero) -> Tablero:
    """ Devuelve el tablero que resulta de activar, en orden, las cuatro casillas trampa sobre *t*.
    Cada pieza que esté en una casilla trampa sin piezas vecinas de su mismo color se retira del tablero.

    PRE: *t* es un tablero bien formado.

    Args:
        t (Tablero): El tablero sobre el que se activan las trampas.

    Returns:
        Un tablero nuevo, bien formado, con todas las trampas activadas.
    """
    res : Tablero = activarTodasLasTrampas(t)
    return res

#### Ejercicio 6


def moverASecas(t: Tablero, pos: Posicion, d: Direccion) -> Tablero:
    """Traslada la pieza ubicada en la posición pos una casilla hacia la dirección d.

    PRE: 
        tableroBienFormado(t)
        posicionEnTablero(pos)
        hayPieza(t, pos)
        puedeMoverASecas(t, pos, d)

    Args:
        t (Tablero): El tablero sobre el cual se realiza el movimiento.
        pos (Posicion): La posición de origen de la pieza a mover.
        d (Direccion): La dirección hacia la cual se desplaza la pieza.

    Returns:
        Un nuevo tablero resultante de mover la pieza a secas.
    """
    pos_destino: Posicion = posicion_vecina_hacia(pos, d)
    casilla_origen: Casilla = t[pos.fila][pos.columna]
    
    t[pos_destino.fila][pos_destino.columna] = casilla_origen
    t[pos.fila][pos.columna] = VACIA
    
    return t


def arrastrar(t: Tablero, pos: Posicion, d: Direccion, d_arrastrar: Direccion) -> Tablero:
    """Traslada la pieza ubicada en pos hacia la dirección d y arrastra a una pieza enemiga
    adyacente hacia la casilla de origen pos.

    PRE: 
        tableroBienFormado(t)
        posicionEnTablero(pos)
        hayPieza(t, pos)
        puedeArrastrar(t, pos, d, d_arrastrar)

    Args:
        t (Tablero): El tablero sobre el cual se realiza el arrastre.
        pos (Posicion): La posición de la pieza propia que inicia el movimiento.
        d (Direccion): La dirección hacia la cual se mueve la pieza propia.
        d_arrastrar (Direccion): La dirección de movimiento de la pieza enemiga arrastrada.

    Returns:
        Un nuevo tablero con ambas piezas trasladadas según la acción de arrastrar.
    """
    pos_destino: Posicion = posicion_vecina_hacia(pos, d)
    pos_arrastre: Posicion = posicion_vecina_hacia(pos, opuesta(d_arrastrar))
    casilla_arrastre: Casilla = t[pos_arrastre.fila][pos_arrastre.columna]
    casilla_origen: Casilla = t[pos.fila][pos.columna]

    t[pos_destino.fila][pos_destino.columna] = casilla_origen
    t[pos.fila][pos.columna] = casilla_arrastre
    t[pos_arrastre.fila][pos_arrastre.columna] = VACIA
    return t


def empujar(t: Tablero, pos: Posicion, d: Direccion, d_empuje: Direccion) -> Tablero:
    """Desplaza una pieza enemiga adyacente ubicada en dirección d hacia d_empuje,
    y mueve la pieza propia en pos hacia la casilla dejada por el enemigo.

    PRE: 
        tableroBienFormado(t)
        posicionEnTablero(pos)
        hayPieza(t, pos)
        puedeEmpujar(t, pos, d, d_empuje)

    Args:
        t (Tablero): El tablero sobre el cual se realiza el empuje.
        pos (Posicion): La posición de origen de la pieza propia que empuja.
        d (Direccion): La dirección donde se encuentra la pieza enemiga a empujar.
        d_empuje (Direccion): La dirección hacia la cual es empujada la pieza enemiga.

    Returns:
        Un nuevo tablero con las piezas desplazadas tras el empuje.
    """
    pos_destino: Posicion = posicion_vecina_hacia(pos, d)
    pos_empuje: Posicion = posicion_vecina_hacia(pos_destino, d_empuje)
    pieza_destino: Casilla = t[pos_destino.fila][pos_destino.columna]
    pieza_origen: Casilla = t[pos.fila][pos.columna]

    t[pos_empuje.fila][pos_empuje.columna] = pieza_destino
    t[pos_destino.fila][pos_destino.columna] = pieza_origen
    t[pos.fila][pos.columna] = VACIA
    
    return t


def crearJuegoPostMovimiento(j: Juego, t: Tablero, pasos_consumidos: int) -> Juego:
    """Genera el nuevo estado de Juego tras un movimiento, actualizando el tablero, 
    el turno del jugador y la cantidad de pasos consumidos.

    PRE: 
        juegoBienFormado(j)
        tableroBienFormado(t)
        0 <= pasos_consumidos <= MAX_PASOS

    Args:
        j (Juego): El estado del juego previo al movimiento.
        t (Tablero): El tablero resultante tras aplicar el movimiento y activar trampas.
        pasos_consumidos (int): La cantidad acumulada de pasos tras el movimiento actual.

    Returns:
        Una nueva instancia de Juego con el turno y los pasos consumidos correspondientes.
    """
    if pasos_consumidos == MAX_PASOS:
        nuevo_turno: Color = oponente(j.turno)
        nuevos_pasos: int = 0
    else:
        nuevo_turno: Color = j.turno
        nuevos_pasos: int = pasos_consumidos
        
    nuevo_juego = Juego(t, nuevo_turno, nuevos_pasos)
    return nuevo_juego


def realizar_movimiento(j: Juego, m: Movimiento) -> Juego:
    """Devuelve el estado del juego resultante de realizar el movimiento m sobre j.

    PRE: 
        juegoBienFormado(j)
        movimientoBienFormado(m)
        puedeRealizarMovimiento(j, m)

    Args:
        j (Juego): Estado actual del juego.
        m (Movimiento): El movimiento que se desea ejecutar.

    Returns:
        Un nuevo objeto Juego que representa el estado del juego tras aplicar m,
        haber activado todas las trampas correspondientes y actualizado el turno y pasos.
    """
    accion: Accion = m.accion
    tablero: Tablero = copiarTablero(j.tablero)
    pos_origen: Posicion = m.origen
    pasos_movimiento: list[Direccion] = m.pasos
    pasos_consumidos: int = j.pasos_consumidos

    if accion == MOVER_A_SECAS:
        tablero = moverASecas(tablero, pos_origen, pasos_movimiento[0])
    elif accion == ARRASTRAR:
        tablero = arrastrar(tablero, pos_origen, pasos_movimiento[0], pasos_movimiento[1])
    else:
        tablero = empujar(tablero, pos_origen, pasos_movimiento[0], pasos_movimiento[1])

    tablero_nuevo: Tablero = activar_trampas(tablero)
    pasos_totales: int = pasos_consumidos + len(pasos_movimiento)
    nuevo_juego: Juego = crearJuegoPostMovimiento(j, tablero_nuevo, pasos_totales)
    return nuevo_juego

#### Ejercicio 7

def esInicioDeTurno(j : Juego, col : Color) -> bool:
    """
    Indica si el juego se encuentra en el inicio del turno del jugador dado.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador a evaluar.
    Returns:
        True si el turno actual corresponde a col y se han consumido 0 pasos.
    """
    res : bool = j.turno == col and j.pasos_consumidos == 0
    return res

def hayConejoEnTablero(j : Juego, col : Color) -> bool:
    """
    Indica si existe al menos un conejo del color especificado en el tablero.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador del cual se buscan los conejos.
    Returns:
        True si hay al menos un conejo de color col en el tablero, False en caso contrario.
    """
    tablero = j.tablero
    i : int = 0
    res : bool = False

    while i < len(tablero) and not res:
        h : int = 0
        while h < len(tablero[i]) and not res:
            pos : Posicion = Posicion(i,h)
            res = hayFiguraDeColor(j.tablero, pos, CONEJO, col)
            h += 1
        i += 1

    return res

def filaInicialColor(t: Tablero, col: Color) -> list[Posicion]:
    """
    Devuelve la lista con todas las posiciones correspondientes a la fila inicial de un color.

    PRE: tablero_bien_formado(t)
    Args:
        t (Tablero): El tablero del juego.
        col (Color): El color del jugador (DORADO o PLATEADO).
    Returns:
        list[Posicion]: Lista de posiciones correspondientes a la fila 0 si es DORADO o la fila 7 si es PLATEADO.
    """
    lista : list[Posicion] = []
    i : int = 0
    if col == DORADO:
        while i < len(t[0]):
            pos_actual : Posicion = Posicion(0,i)
            lista.append(pos_actual)
            i += 1
    else:
        while i < len(t[7]):
            pos_actual : Posicion = Posicion(7,i)
            lista.append(pos_actual)
            i += 1

    return lista

def hayConejoEnFilaInicialOponente(j : Juego, col : Color) -> bool:
    """
    Indica si el jugador de color col tiene al menos un conejo en la fila inicial del oponente.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador a evaluar.
    Returns:
        True si hay al menos un conejo de color col en la fila inicial de su oponente, False en caso contrario.
    """
    color_oponente : Color = oponente(col)
    tablero : Tablero = j.tablero
    posiciones_iniciales : list[Posicion] = filaInicialColor(tablero, color_oponente)
    res : bool = False
    i : int = 0

    while i < len(posiciones_iniciales) and not res:
        pos_actual : Posicion = posiciones_iniciales[i]
        res = hayFiguraDeColor(tablero, pos_actual, CONEJO, col)
        i += 1
    return res

def reuneCondicionesDeGanar(j : Juego, col: Color) -> bool:
    """
    Indica si el jugador de color col cumple al menos una condición de victoria 
    (tener un conejo en la fila inicial oponente o que el oponente se quede sin conejos).

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador a evaluar.
    Returns:
        True si col reúne condiciones de ganar, False en caso contrario.
    """
    res : bool = hayConejoEnFilaInicialOponente(j, col) or not hayConejoEnTablero(j, oponente(col))
    return res

def reuneCondicionesDeGanarExclusivas(j : Juego, col : Color) -> bool:
    """
    Indica si el jugador de color col reúne condiciones de ganar y su oponente no.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador a evaluar.
    Returns:
        True si solo col reúne condiciones de ganar, False en caso contrario.
    """
    res : bool = reuneCondicionesDeGanar(j , col) and not reuneCondicionesDeGanar(j, oponente(col))
    return res

def esJugadorGanador(j : Juego, col : Color)-> bool:
    """
    Indica si el jugador de color col es el ganador del juego según las reglas
    de inicio de turno y exclusividad de condiciones de ganar.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
        col (Color): El color del jugador a evaluar.
    Returns:
        True si col es el ganador definitivo del juego, False en caso contrario.
    """
    res : bool = (esInicioDeTurno(j, oponente(col)) and reuneCondicionesDeGanar(j,col)) or (esInicioDeTurno(j, col) and reuneCondicionesDeGanarExclusivas(j, col))
    return res


def hay_ganador_determinado(j : Juego) -> bool:
    """
    Indica si existe un ganador en el estado actual del juego.

    PRE: juego_bien_formado(j)
    Args:
        j (Juego): El estado actual del juego.
    Returns:
        True si DORADO o PLATEADO es el ganador, False si el juego continúa o está trabado.
    """
    res : bool = esJugadorGanador(j, DORADO) or esJugadorGanador(j, PLATEADO)
    return res

def ganador_del_juego(j : Juego) -> Color:
    """
    Devuelve el color del jugador ganador del juego.

    PRE: juego_bien_formado(j) y hay_ganador_determinado(j)
    Args:
        j (Juego): El estado actual del juego.
    Returns:
        DORADO si el ganador es las piezas doradas, PLATEADO en caso contrario.
    """
    res: Color = PLATEADO
    if esJugadorGanador(j, DORADO):
        res = DORADO
    return res


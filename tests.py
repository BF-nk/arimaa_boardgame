import unittest
from arimaa import *

# Las piezas se representan con las siguientes letras:
#   E : elefante
#   M : camello
#   H : caballo
#   D : perro
#   C : gato
#   R : ratón
# donde
#   mayúscula : dorado
#   minúscula : plateado

def tablero_8x8_vacio():
    return leer_tablero([
              '--------', #7
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])

def tablero_lista_vacia():
    return leer_tablero([])

def tablero_7x8_incompleto():
    return leer_tablero([
              '-------', #7
              '-------', #6
              '-------', #5
              '-------', #4
              '-------', #3
              '-------', #2
              '-------', #1
              '-------', #0
              #0123456
            ])

def tablero_8x7_incompleto():
    return leer_tablero([
              '--------', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              '--------', #1
              '--------', #0
              #01234567
            ])

def tablero_7x7_incompleto():
    return leer_tablero([
              '-------', #6
              '-------', #5
              '-------', #4
              '-------', #3
              '-------', #2
              '-------', #1
              '-------', #0
              #0123456
            ])

def tablero_8x8_inicial_ejemplo():
    return leer_tablero([
              'hcdmedch', #7
              'rrrrrrrr', #6
              '--------', #5
              '--------', #4
              '--------', #3
              '--------', #2
              'RRRRRRRR', #1
              'HCDMEDCH', #0
              #01234567
            ])

def tablero_8x8_mezclado():
    return leer_tablero([
                '--r---rr', #7
                '-mrh----', #6
                '-r---r--', #5
                'd-EH---c', #4
                '-M--hD-d', #3
                '-R-e----', #2
                '---H-R-C', #1
                'R-R--R-R', #0
                #01234567
                ])

def tablero_8x8_vecinos():
    return leer_tablero([
              'R-hRD-Rr', #7
              'M----d--', #6
              '-h-rrCR-', #5
              'R-rcE---', #4
              '--drRR--', #3
              '-HD-H--m', #2
              '--r-RCc-', #1
              're---r--', #0
              #01234567
            ])
def tablero_8x8_vecinos_debiles():
    return leer_tablero([
              '--Hdm---', #7
              'r--HhC--', #6
              'e---R-C-', #5
              'ME--d---', #4
              'h--RDcRr', #3
              'R-R-r--r', #2
              '-RRcrRD-', #1
              '--r---rr', #0
              #01234567
            ])

#### Ejercicio 1

class test_tablero_bien_formado(unittest.TestCase):

    def test_8x8_lleno(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(tablero_bien_formado(t))

    def test_tablero_lista_vacia(self):
        t = tablero_lista_vacia()
        self.assertFalse(tablero_bien_formado(t))

    def test_8x8_vacio(self):
        t = tablero_8x8_vacio()
        self.assertTrue(tablero_bien_formado(t))

    def test_7x8_ancho_incompleto(self):
        t = tablero_7x8_incompleto()
        self.assertFalse(tablero_bien_formado(t))

    def test_8x7_alto_incompleto(self):
        t = tablero_8x7_incompleto()
        self.assertFalse(tablero_bien_formado(t))

    def test_7x7_ancho_y_alto_incompleto(self):
        t = tablero_7x7_incompleto()
        self.assertFalse(tablero_bien_formado(t))

class test_posicion_en_tablero(unittest.TestCase):

    def test_posicion_ok(self):
        self.assertTrue(posicion_en_tablero(Posicion(5, 3)))

    def test_fila_fuera_de_rango(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(8, 3)))

    def test_columna_fuera_de_rango(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(0, 8)))

    def test_fila_y_columna_fuera_de_rango(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(8, 8)))

    def test_fila_y_columna_negativas(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(-1, -1)))

    def test_columna_negativa(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(0, -1)))

    def test_fila_negativa(self) -> None:
        self.assertFalse(posicion_en_tablero(Posicion(-1, 0)))

class test_movimiento_bien_formado(unittest.TestCase):

    # --- MOVER_A_SECAS ---
    def test_movimiento_ok(self):
        self.assertTrue(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])))

    def test_movimiento_mover_a_secas_ok(self) -> None:
        self.assertTrue(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])))

    def test_movimiento_mover_a_secas_sin_pasos(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(0, 1), [])))

    def test_movimiento_mover_a_secas_mas_de_un_paso(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE, SUR])))

    def test_movimiento_mover_a_secas_fuera_de_tablero(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(8, 1), [NORTE])))

    # --- ARRASTRAR ---
    def test_movimiento_arrastrar_ok(self) -> None:
        self.assertTrue(movimiento_bien_formado(Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE, SUR])))

    def test_movimiento_arrastrar_con_un_paso(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE])))

    def test_movimiento_arrastrar_con_tres_pasos(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(ARRASTRAR, Posicion(0, 1), [NORTE, SUR, ESTE])))

    def test_movimiento_arrastrar_fuera_de_tablero(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(ARRASTRAR, Posicion(8, 1), [NORTE, NORTE])))

    # --- EMPUJAR ---
    def test_movimiento_empujar_ok(self) -> None:
        self.assertTrue(movimiento_bien_formado(Movimiento(EMPUJAR, Posicion(0, 1), [NORTE, SUR])))

    def test_movimiento_empujar_con_un_paso(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(EMPUJAR, Posicion(0, 1), [NORTE])))

    def test_movimiento_empujar_con_tres_pasos(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(EMPUJAR, Posicion(0, 1), [NORTE, SUR, ESTE])))

    def test_movimiento_empujar_fuera_de_tablero(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(EMPUJAR, Posicion(8, 1), [NORTE, NORTE])))

    # --- POSICIONES NEGATIVAS ---
    def test_movimiento_posicion_negativa(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(MOVER_A_SECAS, Posicion(-1, 1), [NORTE])))

    def test_movimiento_arrastrar_posicion_negativa(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(ARRASTRAR, Posicion(0, -1), [NORTE, NORTE])))

    def test_movimiento_empujar_posicion_negativa(self) -> None:
        self.assertFalse(movimiento_bien_formado(Movimiento(EMPUJAR, Posicion(-1, -1), [NORTE, NORTE])))

class test_juego_bien_formado(unittest.TestCase):

    def test_juego_ok(self):
        j = Juego(tablero_8x8_vacio(), DORADO, 0)
        self.assertTrue(juego_bien_formado(j))

    # --- TABLEROS INVALIDOS ---
    def test_juego_tablero_ancho_incompleto(self):
        j = Juego(tablero_7x8_incompleto(), DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_tablero_ancho_y_alto_incompleto(self):
        j = Juego(tablero_7x7_incompleto(), DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_tablero_alto_incompleto(self):
        j = Juego(tablero_8x7_incompleto(), DORADO, 0)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_consumidos_negativos(self):
        j = Juego(tablero_8x8_vacio(), DORADO, -1)
        self.assertFalse(juego_bien_formado(j))

    
    # --- PASOS INVALIDOS ---
    def test_juego_pasos_consumidos_igual_a_maximo(self):
        j = Juego(tablero_8x8_vacio(), DORADO, MAX_PASOS)
        self.assertFalse(juego_bien_formado(j))

    def test_juego_pasos_consumidos_mayor_a_maximo(self):
        j = Juego(tablero_8x8_vacio(), DORADO, MAX_PASOS + 1)
        self.assertFalse(juego_bien_formado(j))

    # --- DISTINTO COLOR ---
    def test_distinto_color_de_turno(self):
        j = Juego(tablero_8x8_vacio(), PLATEADO, 0)
        self.assertTrue(juego_bien_formado(j))

#### Ejercicio 2

class test_posicion_vecina_hacia(unittest.TestCase):

    def test_vecina_al_norte(self):
        self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), NORTE), Posicion(1, 0))
    def test_vecina_al_sur(self):
            self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), SUR), Posicion(-1, 0))
    def test_vecina_al_este(self):
            self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), ESTE), Posicion(0, 1))
    def test_vecina_al_oeste(self):
            self.assertEqual(posicion_vecina_hacia(Posicion(0, 0), OESTE), Posicion(0, -1))

    def test_vecina_desde_posicion_no_nula(self):
    # Probar desde coordenadas positivas arbitrarias
        self.assertEqual(posicion_vecina_hacia(Posicion(5, 10), NORTE), Posicion(6, 10))
    # Probar desde coordenadas negativas
        self.assertEqual(posicion_vecina_hacia(Posicion(-3, -4), OESTE), Posicion(-3, -5))

class test_son_posiciones_vecinas(unittest.TestCase):

    def test_vecinas(self):
        self.assertTrue(son_posiciones_vecinas(Posicion(0, 0), Posicion(1, 0)))

    def test_no_vecinas(self):
            # No son vecinas en fila
            self.assertFalse(son_posiciones_vecinas(Posicion(4, 0), Posicion(1, 0)))
            # No son vecinas en columna
            self.assertFalse(son_posiciones_vecinas(Posicion(0, 5), Posicion(0, 1)))
            # No son vecinas ni en fila ni en columna
            self.assertFalse(son_posiciones_vecinas(Posicion(2, 5), Posicion(3, 1)))
            # Negativas
            self.assertFalse(son_posiciones_vecinas(Posicion(-2, -5), Posicion(-3, -1)))

    def test_vecinas_negativas(self):
        #En fila
        self.assertTrue(son_posiciones_vecinas(Posicion(-1,0),Posicion(-2,0)))
        #En columna
        self.assertTrue(son_posiciones_vecinas(Posicion(0, -2), Posicion(0, -3)))

class test_casilla_en_posicion(unittest.TestCase):

    def test_casilla_en_esquinas(self):
        t = tablero_8x8_inicial_ejemplo()

        #SUROESTE
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 0)), Pieza(CABALLO, DORADO))

        #SURESTE
        self.assertEqual(casilla_en_posicion(t, Posicion(0, 7)), Pieza(CABALLO, DORADO))

        #NORESTE
        self.assertEqual(casilla_en_posicion(t, Posicion(7, 7)), Pieza(CABALLO, PLATEADO))

        #NOROESTE
        self.assertEqual(casilla_en_posicion(t, Posicion(7, 0)), Pieza(CABALLO, PLATEADO))

    def test_casilla_con_distinta_pieza(self):

        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t, Posicion(7, 3)), Pieza(CAMELLO, PLATEADO))
        self.assertEqual(casilla_en_posicion(t, Posicion(1, 2)), Pieza(CONEJO, DORADO))


    def test_casilla_vacia_en_posicion(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertEqual(casilla_en_posicion(t, Posicion(4, 0)), VACIA)
    

class test_hay_casilla_vacia(unittest.TestCase):

    def test_casilla_vacia(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_casilla_vacia(t, Posicion(2, 1)))

    def test_casilla_no_vacia(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_casilla_vacia(t, Posicion(0, 1)))

class test_hay_pieza_de_color(unittest.TestCase):

    def test_hay_pieza_de_color_ok(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertTrue(hay_pieza_de_color(t, Posicion(1, 4), DORADO))

    def test_hay_pieza_de_color_ok__en_esquinas(self):
        t = tablero_8x8_inicial_ejemplo()

        #SUROESTE
        self.assertTrue(hay_pieza_de_color(t, Posicion(0, 0), DORADO))
        #SURESTE
        self.assertTrue(hay_pieza_de_color(t, Posicion(0, 7), DORADO))
        #NOROESTE
        self.assertTrue(hay_pieza_de_color(t, Posicion(7, 0), PLATEADO))
        #NORESTE
        self.assertTrue(hay_pieza_de_color(t, Posicion(7, 7), PLATEADO))

    def test_no_hay_pieza_de_color(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_pieza_de_color(t, Posicion(3, 4), PLATEADO))
        self.assertFalse(hay_pieza_de_color(t, Posicion(2, 5), DORADO))

    def test_hay_pieza_de_color_opuesto(self):
        t = tablero_8x8_inicial_ejemplo()
        self.assertFalse(hay_pieza_de_color(t, Posicion(1, 2), PLATEADO))
        self.assertFalse(hay_pieza_de_color(t, Posicion(7, 5), DORADO))

#### Ejercicio 3

class test_hay_casilla_vacia_hacia(unittest.TestCase):

    def test_hay_casilla_vacia_hacia_desde_esquinas(self):
        t = tablero_8x8_mezclado()

        #SUROESTE
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(0, 0), NORTE))

        #SURESTE
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(0, 7), OESTE))

        #NORESTE
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(7, 7), SUR))

        #NOROESTE
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(7, 0), ESTE))

    def test_no_hay_casilla_vacia_hacia_desde_arbitrario(self):
        t = tablero_8x8_mezclado()
        self.assertFalse(hay_casilla_vacia_hacia(t, Posicion(1, 3), NORTE))

    def test_hay_casilla_vacia_hacia_desde_arbitrario(self):
        t = tablero_8x8_mezclado()
        self.assertTrue(hay_casilla_vacia_hacia(t, Posicion(4, 3), ESTE))

        
class test_hay_pieza_amiga_vecina(unittest.TestCase):

    def test_hay_pieza_amiga_vecina(self):
        t = tablero_8x8_vecinos()

        #PLATEADO
        self.assertTrue(hay_pieza_amiga_vecina(t, Posicion(4, 3)))
        #DORADO
        self.assertTrue(hay_pieza_amiga_vecina(t, Posicion(3, 4)))

    def test_no_hay_pieza_amiga_vecina(self):
        t = tablero_8x8_vecinos()
        #PLATEADO
        self.assertFalse(hay_pieza_amiga_vecina(t, Posicion(1, 2)))
        #DORADO
        self.assertFalse(hay_pieza_amiga_vecina(t, Posicion(7, 6)))


class test_hay_pieza_enemiga_mas_debil_hacia(unittest.TestCase):

    def test_hay_pieza_enemiga_mas_debil_hacia(self):
        t = tablero_8x8_vecinos_debiles()
        # HACIA PIEZA MÁS DÉBIL DORADA
        self.assertTrue(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 3), OESTE))
        # HACIA PIEZA MÁS DÉBIL PLATEADA
        self.assertTrue(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(3, 4), ESTE))
    
    def test_no_hay_pieza_enemiga_mas_debil_hacia(self):
        t = tablero_8x8_vecinos_debiles()
        # HACIA PIEZA MÁS FUERTE DORADA
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(7, 3), OESTE))
        # HACIA PIEZA MÁS FUERTE PLATEADA
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(4, 0), OESTE))
        # CASILLA VACIA
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(6, 5), ESTE))

    def test_pieza_amiga_mas_debil_hacia(self):
        t = tablero_8x8_vecinos_debiles()
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(1, 4), OESTE))

    def test_hacia_enemigo_con_misma_fuerza(self):
        t = tablero_8x8_vecinos_debiles()
        self.assertFalse(hay_pieza_enemiga_mas_debil_hacia(t, Posicion(6, 3), ESTE))

class test_hay_pieza_enemiga_mas_fuerte_vecina(unittest.TestCase):

    def setUp(self):
        # Tablero de prueba compartido
        self.t = leer_tablero([
            'R-e--mRr', #7
            '------dE', #6
            'h--Rr-RR', #5
            'c--R-C--', #4
            '-rCHDrr-', #3
            '----rc--', #2
            'h-R-M-R-', #1
            'rr-D-dH-', #0
            #01234567
        ])

    def test_hay_pieza_enemiga_mas_fuerte_vecina__dorada_y_plateada(self):
        # Pieza dorada 'r' (conejo) en (3,1) tiene al lado 'C' (gato dorado) que es más fuerte
        self.assertTrue(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(3, 1)))

        # Pieza plateada 'd' (perro plateado) en (6,6) tiene al lado 'E' (elefante dorado) en (6,7)
        self.assertTrue(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(6, 6)))

    def test_no_hay_pieza_enemiga_mas_fuerte_vecina__es_mas_fuerte(self):
        # 'E' (elefante dorado) en (6,7) es la pieza más fuerte, no tiene nada más fuerte alrededor
        self.assertFalse(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(6, 7)))

    def test_no_hay_pieza_enemiga_mas_fuerte_vecina__misma_fuerza(self):
        # 'r' (conejo plateado) en (0,1) tiene al lado 'r' (conejo plateado) en (0,0) -> igual fuerza
        self.assertFalse(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(0, 1)))

    def test_no_hay_pieza_enemiga_mas_fuerte_vecina__pieza_amiga_mas_fuerte(self):
        # 'R' (conejo dorado) en (3,2) tiene al lado 'H' (caballo dorado) en (3,3) -> es más fuerte pero amiga
        self.assertFalse(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(3, 2)))

    def test_no_hay_pieza_enemiga_mas_fuerte_vecina__rodeado_de_vacias(self):
        # 'm' (camello plateado) en (7,5) solo tiene casillas vacías a su alrededor en la fila 6
        self.assertFalse(hay_pieza_enemiga_mas_fuerte_vecina(self.t, Posicion(7, 5)))

class test_hay_pieza_congelada(unittest.TestCase):

    def setUp(self):
        self.t = leer_tablero([
            '--d--H-D', #7
            '-hMc--r-', #6
            '--r--C-H', #5
            '--------', #4
            '-CeD----', #3
            '---R----', #2
            '--------', #1
            '--------', #0
            #01234567
        ])

    def test_hay_pieza_congelada__casos_positivos(self):
        # 'h' (caballo plateado) en (6, 1) tiene a 'M' (camello dorado) en (6, 2) al lado y no tiene amigas adyacentes -> CONGELADO
        self.assertTrue(hay_pieza_congelada(self.t, Posicion(6, 1)))

        # 'C' (gato dorado) en (3, 1) tiene a 'e' (elefante plateado) en (3, 2) al lado y no tiene amigas adyacentes -> CONGELADO
        self.assertTrue(hay_pieza_congelada(self.t, Posicion(3, 1)))

    def test_no_hay_pieza_congelada_con_vecinos_enemigos_mas_debiles(self):
        # 'e' (elefante plateado) en (3, 2) es la pieza más fuerte, nadie la puede congelar -> FALSO
        self.assertFalse(hay_pieza_congelada(self.t, Posicion(3, 2)))
    def test_no_hay_pieza_congelada_con_vacias_alrededor(self):
        # 'R' (conejo dorado) en (2, 3) solo tiene casillas vacías alrededor -> FALSO
        self.assertFalse(hay_pieza_congelada(self.t, Posicion(2, 3)))

    def test_no_hay_pieza_congelada__casilla_vacia(self):
        # En una casilla vacía como (4, 4) no hay pieza congelada -> FALSO
        self.assertFalse(hay_pieza_congelada(self.t, Posicion(4, 4)))

#### Ejercicio 4

class test_puede_realizar_movimiento(unittest.TestCase):

    def test_mover_a_secas_ok(self):
        t = leer_tablero([
              '--eMr---', #7
              '--------', #6
              '-R----r-', #5
              '--------', #4
              '--mMd---', #3
              '---D----', #2
              '--------', #1
              '-mD--mDR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        m = Movimiento(MOVER_A_SECAS, Posicion(0, 1), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j, m))

#### Ejercicio 5

class test_activar_trampas(unittest.TestCase):

    def test_activar_trampas_ok(self):
        t0 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-r--E--', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-H--m--', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t1 = leer_tablero([
               '-eRD--rd', #7
               '--------', #6
               'H-------', #5
               '-H--r-Cr', #4
               'R-------', #3
               'R-------', #2
               'R-------', #1
               'c-D---R-', #0
               #01234567
             ])
        t2 = activar_trampas(t0)
        self.assertNotEqual(t0, t1)
        self.assertEqual(t2, t1)


    def test_tablero_vacio(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '--------', #2
               '--------', #1
               '--------', #0
               #01234567
             ])
        self.assertEqual(activar_trampas(t0), tablero_8x8_vacio())


    def test_pieza_sola_se_va(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '-----m--', #2
               '--------', #1
               '--------', #0
               #01234567
             ])
        self.assertEqual(activar_trampas(t0), tablero_8x8_vacio())


    def test_pieza_con_amiga_vecina_se_queda(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '-----me-', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        t1 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '-----me-', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        self.assertEqual(activar_trampas(t0), t1)


    def test_pieza_con_amiga_diagonal_no_cuenta(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '----e---', #3
               '-----m--', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        t1 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '----e---', #3
               '--------', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        self.assertEqual(activar_trampas(t0), t1)


    def test_pieza_con_enemiga_se_retira(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '-----mE-', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        t1 = leer_tablero([
               '--------', #7
               '--------', #6
               '--------', #5
               '--------', #4
               '--------', #3
               '------E-', #2
               '--------', #1
               '--------', #0
               #01234567
        ])
        self.assertEqual(activar_trampas(t0), t1)


    def test_cuatro_trampas_a_la_vez(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--c-Rd--', #5
               '--------', #4
               '--------', #3
               '--m--HE-', #2
               '--r-----', #1
               '--------', #0
               #01234567
        ])
        t1 = leer_tablero([
               '--------', #7
               '--------', #6
               '----R---', #5
               '--------', #4
               '--------', #3
               '--m--HE-', #2
               '--r-----', #1
               '--------', #0
               #01234567
        ])
        self.assertEqual(activar_trampas(t0), t1)


    def test_funcion_no_modifica_el_tablero_original(self):
        t0 = leer_tablero([
               '--------', #7
               '--------', #6
               '--c-Rd--', #5
               '--------', #4
               '--------', #3
               '--m--HE-', #2
               '--r-----', #1
               '--------', #0
               #01234567
        ])
        t0_original = leer_tablero([
               '--------', #7
               '--------', #6
               '--c-Rd--', #5
               '--------', #4
               '--------', #3
               '--m--HE-', #2
               '--r-----', #1
               '--------', #0
               #01234567
        ])
        activar_trampas(t0)
        self.assertEqual(t0, t0_original)

#### Ejercicio 6

class test_realizar_movimiento(unittest.TestCase):
 
    def test_mover_a_secas(self):
        t0 = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '--------', #5
               '---m----', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        tN = leer_tablero([
               'rrrrrrrr', #7
               'ccddhh-e', #6
               '---m----', #5
               '--------', #4
               '--------', #3
               '--------', #2
               'EMHHDDCC', #1
               'RRRRRRRR', #0
               #01234567
             ])
        j0 = Juego(t0, PLATEADO, 0) 
        jN = Juego(tN, PLATEADO, 1) 
        mN = Movimiento(MOVER_A_SECAS, Posicion(4, 3), [NORTE])
        self.assertTrue(puede_realizar_movimiento(j0, mN))
        self.assertEqual(realizar_movimiento(j0, mN), jN)

#### Ejercicio 7

class test_ganador_del_juego(unittest.TestCase):

    def test_promueve_conejo_dorado_turno_del_oponente(self):
        t = leer_tablero([
              'rr----Rr', #7
              'c-----me', #6
              '---Ed-R-', #5
              '-M---R--', #4
              '---R----', #3
              '-rrrr---', #2
              '-H---DCC', #1
              'R-----RR', #0
              #01234567
            ])
        j = Juego(t, PLATEADO, 0)
        self.assertTrue(hay_ganador_determinado(j))
        self.assertEqual(ganador_del_juego(j), DORADO)

if __name__ == "__main__":
    unittest.main(verbosity=2)
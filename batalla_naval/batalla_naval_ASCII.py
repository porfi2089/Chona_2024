import numpy as np # importamos la libreria np que cuenta con una multitud de 
import os # os es una libreria que tiene muchas funciones que permiten interactuar con el sistema, en este caso la vamos a usar para la simple funcion de limpiar la consola
from colorama import Fore, Back # colorama es una libreria de formateo de texto para la terminal, la vamos a usar para darle color a los mensajes
import time # time es una libreria que viene con un monton de librerias que tienen que ver con el tiempo, nosotros la vamos a usar para esperar una determinada cantidad de tiempo en ciertos lugares 

'''
    Este es un juego de batalla naval en el que dos jugadores se enfrentan en una batalla naval.
    Primero ambos jugadores se encargaran de poner sus barcos en el tablero, luego se turnaran para atacar al tablero del otro jugador.
    El juego termina cuando uno de los jugadores destruye todos los barcos del otro jugador.
    El tablero se mostrara en la consola y se mostrara de la siguiente manera:
    - 0: celda vacia (se mostrara en azul)
    - 1: celda ocupada por un barco (no se mostrara en el tablero)
    - 2: celda atacada con exito (se mostrara en rojo)
    - 3: celda atacada sin que alla un barco (se mostrara en blanco)
    El tablero sera mostrado al jugador mediante una representacion ASCII en la consola.

    Aclaraciones:
    - El tablero es customizable
    - Soporta barcos de cualquier tamaño, pero por arriba de 3 de largo estas a tu propio riesgo
    - La IA es vencible


    Juego por: Manuel Rao, Tobias Esteban Majic.

    GitHub:
    - https://github.com/porfi2089/Chona_2024

'''

tamano_tablero = 4 # tamaño del tablero
tablero_player1 = np.zeros([tamano_tablero, tamano_tablero]) # creo una array de 10x10 llena solo de ceros
tablero_player2 = tablero_player1.copy() # copiamos la primera array y la asignamos como el tablero de player 2
barcos = 0 # variable que va a almacenar la cantidad de barcos que van a haber en el tablero
frases_malvadas_epicas = [
    f"No sabes con quien te metiste, te voy a hundir como el titanic",
    f"Con lo que haz hecho, te voy a hacer lo mismo que blender a las nets de ORT... \n ¡¡¡¡¡arderas!!!!!!",
    f"Ahora si que te destruire!!!!!!",
    f"Haz firmado tu sentencia de muerte. \n ¡¡¡AHORA MORIRAS!!!",
    f"Prepárate para ser aniquilado por mi poderío naval!",
    f"Tu flota será reducida a polvo bajo mi implacable dominio!",
    f"Te hundiré hasta las profundidades más oscuras del abismo marino!",
    f"La destrucción yace en tu horizonte, como una tormenta imparable!",
    f"Tu derrota, inscrita en los anales de la historia naval, será inminente!",
    f"Seré la encarnación de tu peor pesadilla en los vastos océanos!",
    f"Tu naufragio será la sinfonía de mi triunfo supremo!",
    f"Ninguna embarcación escapará a la furia de mi estrategia sin piedad!",
    f"Mis cañones convertirán tus barcos en cenizas a la deriva!",
    f"El mar se tintará con la sangre de tu derrota, como un oscuro presagio!",
    f"Mis torpedos hallarán su blanco en el corazón mismo de tu armada!",
    f"Cada ola será un lamento por la inevitable pérdida que te espera!",
    f"Tu final se acerca con la solemnidad de un ocaso sin esperanza!",
    f"En el vasto abismo de los océanos, hallarás tu postrer descanso!",
    f"Tu flota, una vez orgullosa, se convertirá en un eco lejano en las profundidades!",
    f"Navegarás hacia tu perdición con la arrogancia de quien ignora su destino!",
    f"Los vientos de la fortuna soplan a mi favor, anunciando tu caída inevitable!",
    f"Mi navío es la guadaña que cortará tus esperanzas con implacable precisión!",
    f"Mis velas se hinchan con la fuerza de mil tormentas, mientras tu destino se sella!",
    f"Prepárate para ser aniquilado por mi poderío naval!",
    f"Tu flota será reducida a polvo bajo mi implacable dominio!",
    f"Te hundiré hasta las profundidades más oscuras del abismo marino!",
    f"La destrucción yace en tu horizonte, como una tormenta imparable!",
    f"Tu derrota, inscrita en los anales de la historia naval, será inminente!",
    f"Seré la encarnación de tu peor pesadilla en los vastos océanos!",
    f"Tu naufragio será la sinfonía de mi triunfo supremo!",
    f"te voy a hundir como el titanic",
    f"Te hare lo mismo que blender a las nets de ORT... \n ¡¡¡¡¡arderas!!!!!!",
    f"Te voy a hacer lo mismo que el 2020 a la humanidad",
    f"Te voy a hacer lo mismo que visual studio le hace a relpit \n te destruire!!!!!!",
    f"Ninguna embarcación escapará a la furia de mi estrategia sin piedad!",
    f"Mis cañones convertirán tus barcos en cenizas a la deriva!",
    f"El mar se tintará con la sangre de tu derrota, como un oscuro presagio!",
    f"Mis torpedos hallarán su blanco en el corazón mismo de tu armada!",
    f"Cada ola será un lamento por la inevitable pérdida que te espera!",
    f"Tu final se acerca con la solemnidad de un ocaso sin esperanza!",
    f"En el vasto abismo de los océanos, hallarás tu postrer descanso!",
    f"Tu flota, una vez orgullosa, se convertirá en un eco lejano en las profundidades!",
    f"Navegarás hacia tu perdición con la arrogancia de quien ignora su destino!",
    f"Los vientos de la fortuna soplan a mi favor, anunciando tu caída inevitable!",
    f"Mi navío es la guadaña que cortará tus esperanzas con implacable precisión!",
    f"Mis velas se hinchan con la fuerza de mil tormentas, mientras tu destino se sella!",
]

Fore.WHITE, Back.BLACK # setear el color de las letras y del fondo a defalult
os.system('cls') # limpia la consola


# pide las posiciones de cada celda ocupada y las transforma en una array de np
def ask_for_position(text: str, 
                     pos: int) -> int:
    '''pide y devuelve un numero entero'''	

    ask_flag = True # se crea una variable que va a ser la condicion de un while loop
    while ask_flag: # loop que se repite hasta que se de una respuesta valida
        inp = input(text) # pide la respuesta al usuario
        ask_flag = False # se asume que la respuesta es valida
        try: # utilizamos el metodo try por si llegan a pasar un valor que no sea un numero entero 
            inp = int(inp)-pos # se transforma la respuesta en un numero entero y se resta pos(indica si el valor pedido es una posicion en el tablero o un valor de barco)
        except:
            print(f"{Fore.RED}Mala respuesta, responder solo numeros enteros{Fore.WHITE}")
            ask_flag = True # si la respuesta no es un numero entero, se repite el loop
            continue # se salta el resto del loop
        if pos == 1:
            if 0 > inp or inp > tamano_tablero-1: # revisar si el valor esta dentro del tablero
                ask_flag = True # si no esta dentro del tablero, se repite el loop
                print(f"{Fore.RED}Mala respuesta, numero debe estar entre 1 y {tamano_tablero}{Fore.WHITE}")
    return inp


# definimos una funcion que se va a encargar de asignar valores a una tabla dada en posiciones especificas
def asaign_values(tabla: np.ndarray[np.ndarray[int]], 
                  valores: np.ndarray[int], 
                  posiciones: np.ndarray[np.ndarray[int, int]], 
                  rotaciones: np.ndarray[int], 
                  largo: int):
    '''genera los barcos en las posciciones y rotaciones especificadas en la tabla dada'''

    for value, enum in zip(valores, range(len(valores))): # unimos los valores pasados y el indice de los valores
        x_off = rotaciones[enum] % 2 # se calcula el offset en x
        y_off = (rotaciones[enum] + 1) % 2 # se calcula el offset en y
        # se asigna el valor dado a la posicion en la tabla establecida
        for i in range(largo): # crea un segmento del largo deseado, revisando si este va a colsionar con una pared y moviendolo acordemente
            i -= 1
            if posiciones[enum, 0] + i*x_off > tamano_tablero-1:
                i -= largo
            elif posiciones[enum, 0] + i*x_off < 0:
                i += largo
            if posiciones[enum, 1] + i*y_off > tamano_tablero-1:
                i -= largo
            elif posiciones[enum, 1] + i*y_off < 0:
                i += largo
            tabla[posiciones[enum, 0] + i*x_off, posiciones[enum, 1] + i*y_off] = value


def get_game_mode() -> bool: # pide el modo de juego
    '''pide el modo de juego y devuelve un booleano que indica si el juego es de dos jugadores o contra la computadora'''

    print("Bienvenido a \n",  
        " _           _   _   _           _     _       \n",
        "| |         | | | | | |         | |   (_)      \n",
        "| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  \n",
        "| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ \n",
        "| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) | \n",
        "|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ \n", 
        "                                        | |    \n "
        "                                        |_|    \n") # mensaje de bienvenida
    # menu de seleccion de modo de juego
    print(f"{Fore.WHITE}{Back.BLACK}Modo de juego \n {Fore.GREEN}1{Fore.WHITE}: Jugador vs Jugador \n {Fore.RED}2{Fore.WHITE}: Jugador vs Computadora \n -{Fore.WHITE}{Back.BLACK}") 
    game_mode = input() # pide la respuesta al usuario
    if game_mode == "1":
        return True
    elif game_mode == "2":
        return False
    else:
        print(f"{Fore.RED}Respuesta invalida{Fore.WHITE}")
        time.sleep(1) # espera un segundo para que el jugador pueda leer el mensaje
        os.system('cls') # limpia la consola
        get_game_mode()

def print_board(tablero: np.ndarray[np.ndarray[int]], mode: int = 0) -> None:
    '''imprime el tablero dado en la consola con un formateado a color'''

    tablero = tablero.copy() # crea una copia del tablero
    tablero = np.maximum(tablero - 1, np.zeros((tamano_tablero, tamano_tablero))) # remplazamos al 1 por 0 para que no se muestre en el tablero
    for i in enumerate(tablero): # itera por las filas de la tabla
        i = i[0] # nos aseguramos de solo tener el indice de la fila y no de las sub listas
        line = f"{Back.BLACK}{Fore.BLACK}-" # se crea una variable que va a almacernar la info de la lineay una barra negra
        for o in enumerate(tablero[i]): # itera por las columnas de la tabla
            n = ""
            o = o[0]
            if tablero[i, o] == 2: # si la celda es igual a 2, se le asigna el color rojo
                n = f"{Fore.RED}{Back.RED}2-"
            if tablero[i, o] == 3: # si la celda es igual a 3, se le asigna el color verde
                n = f"{Fore.WHITE}{Back.WHITE}3-"
            if tablero[i, o] == 0: # si la celda es igual a 0, se le asigna el color azul
                n = f"{Fore.BLUE}{Back.BLUE}0-"
            if tablero[i, o] == 1 and mode == 1: # si la celda es igual a 0, se le asigna el color azul
                n = f"{Fore.RED}{Back.RED}1-" 
            line = line + n # se añade la celda a la linea
        print(line+f"{Back.BLACK}{Fore.WHITE}") # se imprime la linea 

def get_new_board(single_player: bool) -> None: # pide las posiciones de los barcos a los jugadores y los asigna a los tableros
    '''pide las posiciones de los barcos a los jugadores y los asigna a los tableros'''

    global tablero_player1 # se asegura de que la variable este definida dentro de la funcion
    global tablero_player2 # se asegura de que la variable este definida dentro de la funcion
    global barcos # se asegura de que la variable este definida dentro de la funcion
    barcos = ask_for_position(f"Cantidad de barcos \n -", 0) # pedimos la cantidad de celdas que van a ocupar los barcos (igual para ambos jugadores)
    largo = 3
    for i in range(1 + np.bitwise_not(single_player)): # este for loop repite el codigo una vez por cada jugador
        print(f"{Fore.WHITE}{Back.BLACK}Player " + str(i+1)) # anunciamos que jugador debe completar los campos
        values = np.ones((barcos)) # transformamos la cantidad de celdas en una lista de unos de ese largo
        posiciones = np.zeros((barcos, 2), dtype=np.uint32) # crea la lista de posciones de los barcos
        rotaciones = np.zeros(barcos, dtype=np.uint32) # crea la lista de rotaciones de los barcos

        # pide cada picision de cada barco
        for b in range(barcos): 
            tablero = np.zeros([tamano_tablero, tamano_tablero]) # se crea una tabla vacia
            asaign_values(tablero, values, posiciones, rotaciones, largo) # asignamos valores para barcos 
            print_board(tablero, mode=1) # muestra el tablero para mostrar poscicion actual de los barcos
            for c in range(2):
                posiciones[b, c] = ask_for_position(f"Pase la posicion "+str(c)+" del barco "+str(b)+": \n -", 1) # pide las cordenadas de cada celda ocupada
            rotaciones[b] = ask_for_position(f"Rotaciones del barco "+str(b)+": \n -", 0) # pide la cantidad de rotaciones que va a tener el barco
            os.system('cls') # limpia la consola

        tablero = np.zeros([tamano_tablero, tamano_tablero]) # se crea una tabla vacia
        asaign_values(tablero, values, posiciones, rotaciones, largo) # asignamos valores para barcos TEST
        print_board(tablero, mode=1)
        time.sleep(1)
        
        # aplica los cambios al tablero correspondiendo creando una copia de tablero que es el que seedita directamente y aplicandola al talbero correspondiente
        if i == 0:
            tablero_player1 = tablero.copy()
        else:
            tablero_player2 = tablero.copy()
        os.system('cls') # limpia la consola

    if single_player: # crea un tablero para la computadora
        for b in range(barcos):
            for c in range(2):
                posiciones[b, c] = np.random.randint(0, tamano_tablero) # genera posiciones aleatorias para los barcos
            rotaciones[b] = np.random.randint(0, 4) # genera rotaciones aleatorias para los barcos
        tablero = np.zeros([tamano_tablero, tamano_tablero])
        asaign_values(tablero, values, posiciones, rotaciones, largo)
        global computer # se asegura de que la variable este definida dentro de la funcion
        computer = Computer(barcos, 3, tamano_tablero)
        tablero_player2 = tablero.copy()


def check_if_game_ended(tablero: np.ndarray[np.ndarray[int]]) -> bool: # checkear si alguno de los jugadores a ganado
    '''revisa si alguno de los jugadores a ganado el juego y devuelve un booleano que indica si el juego a terminado o no'''

    if 1 in tablero: # si sigue habiendo barcos en el tablero
        return False # el juego sige
    return True # el juego a terminado


def check_cell(list: np.ndarray, x: int, y: int, value: int) -> bool:
    '''revisa si la celda en la posicion x, y de la lista dada es igual al valor dado y devuelve un booleano'''

    if list[x, y] == value:
        return True
    return False


def two_player_game_loop() -> None:
    '''uno de los modos de juego en los que dos jugadores se turnan para atacar el tablero del otro jugador, el juego termina cuando uno de los jugadores destruye todos los barcos del otro jugador'''

    game_running = True
    while game_running: # loop principal del juego
        # JUGADOR 1
        os.system('cls') # limpia la consola
        print("player 1") # anuncia el turno del jugador 1
        print_board(tablero_player2) # muestra el tablero del jugador 2
        print("Su truno de atacar")

        # pide las dos pocisiones de ataque
        atx, aty = ask_for_position("Pase la posicion x de la celda: \n -", 1), ask_for_position("Pase la posicion y de la celda: \n -", 1) 
        
        os.system('cls') # limpia la consola
        # si la celda atacada es igual a 1, se muestra HIT, si no se muestra MISS
        if tablero_player2[atx, aty] == 1:
            print(f"{Fore.GREEN}HIT{Fore.WHITE}")
            tablero_player2[atx, aty] = 3  # se almacena el valor 3 en la celda atacada indicando que hay un barco
        elif tablero_player2[atx, aty] == 3: # revisa si la celda ya fue golpeada y solia haber un barco
            print(f"{Fore.GREEN}Already HIT{Fore.WHITE}")
        else: # si no habia un barco
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player2[atx, aty] = 4 # se almacena el valor 4 en la celda atacada indicando que no hay barco
        print_board(tablero_player2) # muestra el nuevo tablero del jugador 2

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = np.bitwise_not(check_if_game_ended(tablero_player2))
        if not game_running:
            os.system('cls') # limpia la consola
            print("FIN DEL JUEGO \n A gandado el jugador 1")
            break # termina el juego

        input("preciona enter cuando el jugador 2 tenga la computadora") # esperar al cambio de jugadores

        # JUGADOR 2
        os.system('cls') # limpia la consola
        print("player 2") # anuncia el turno del jugador 1
        print_board(tablero_player1) # muestra el tablero del jugador 2
        print("Su truno de atacar")

        # pide las dos pocisiones de ataque
        atx, aty = ask_for_position("Pase la posicion x de la celda: \n -", 1), ask_for_position("Pase la posicion y de la celda: \n -", 1) 
        
        os.system('cls') # limpia la consola
        # si la celda atacada es igual a 1, se muestra HIT, si no se muestra MISS
        if tablero_player1[atx, aty] == 1:
            print(f"{Fore.GREEN}HIT{Fore.WHITE}")
            tablero_player1[atx, aty] = 3 # se almacena el valor 3 en la celda atacada indicando que hay un barco
        elif tablero_player1[atx, aty] == 3: # revisa si la celda ya fue golpeada y solia haber un barco
            print(f"{Fore.GREEN}Already HIT{Fore.WHITE}")
        else: # si no habia un barco
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player1[atx, aty] = 4 # se almacena el valor 4 en la celda atacada indicando que no hay barco
        print_board(tablero_player1)

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = np.bitwise_not(check_if_game_ended(tablero_player1))
        if not game_running:
            os.system('cls') # limpia la consola
            print(f"{Back.WHITE}{Fore.GREEN}FIN DEL JUEGO \n A gandado el jugador 2 {Back.BLACK}{Fore.WHITE}")
            break # termina el juego

        input("preciona enter cuando el jugador 1 tenga la computadora") # esperar a que se pase la computadora

class Computer: # clase que representa a la IA de la computadora (no me mates chona, ya se que es un if tree)
    '''clase que representa a la IA de la computadora'''

    def __init__(self, barcos: int, largo: int, tamano_tablero: int):
        self.tablero = np.zeros([tamano_tablero, tamano_tablero])
        self.atacadas = np.zeros([tamano_tablero, tamano_tablero])
        self.barcoOrigen = np.zeros([barcos, 2, 2])
        self.barcosDireccion = np.zeros([barcos])
        self.posiblesDirecciones = np.zeros([4, 2], dtype=int)
        self.barcosNum = 0
        self._barcos = barcos
        self._largo = largo
        self._largoRestante = largo
        self._tamano_tablero = tamano_tablero
        self.mode = 1 # 1 = grid random, 2 = idntify, 3 = destroy

    def atacar(self) -> tuple[int, int]:
        '''ataca una celda en el tablero del jugador basandose en la informacion conseguida mediante ataques anteriores'''

        if self.mode == 1:
            atx = np.random.randint(0, self._tamano_tablero)
            if self._largo > 1:
                aty = np.random.randint(0, int(self._tamano_tablero/2))*2 + atx%2
            else:
                aty = np.random.randint(0, self._tamano_tablero)
            
            while self.atacadas[atx, aty] == 1:
                atx, aty = np.random.randint(0, int(self._tamano_tablero/2))*2, np.random.randint(0, int(self._tamano_tablero/2))*2 # busca en todos los numeros pares
            self.atacadas[atx, aty] = 1
            if tablero_player1[atx, aty] == 1:
                self.barcoOrigen[self.barcosNum, 0] = [atx, aty]
                self.barcoOrigen[self.barcosNum, 1] = [atx, aty]
                if self._largo != 1:
                    self.mode = 2
            return atx, aty
            
        if self.mode == 2:
            atx, aty = self.barcoOrigen[self.barcosNum, 0]

            self.posiblesDirecciones = np.array([[atx, aty+1],
                                                [atx, aty-1],
                                                [atx+1, aty],
                                                [atx-1, aty]], dtype=int)
            
            if self.barcoOrigen[self.barcosNum, 0][0] != self.barcoOrigen[self.barcosNum, 1][0]:
                if self.barcosDireccion[self.barcosNum] == 0:
                    self.posiblesDirecciones = np.delete(self.posiblesDirecciones, 1, 0)
                    self.posiblesDirecciones = np.delete(self.posiblesDirecciones, 0, 0)
                elif self.barcosDireccion[self.barcosNum] == 1:
                    self.posiblesDirecciones = np.delete(self.posiblesDirecciones, 3, 0)
                    self.posiblesDirecciones = np.delete(self.posiblesDirecciones, 2, 0)

            for i in range(len(self.posiblesDirecciones)-1, -1, -1):
                if self.posiblesDirecciones[i, 0] < 0 or self.posiblesDirecciones[i, 0] >= self._tamano_tablero or self.posiblesDirecciones[i, 1] < 0 or self.posiblesDirecciones[i, 1] >= self._tamano_tablero:
                    self.posiblesDirecciones = np.delete(self.posiblesDirecciones, i, 0)
            
            # lo de abajo no anda pero bueno :( es solo optimizacion, en algun momento lo voy a arreglar
            '''for i in self.posiblesDirecciones:
                if i[0] == self.barcoOrigen[self.barcosNum, 1][0]:
                    if i[0] < self.barcoOrigen[self.barcosNum, 0][0]:
                        for o in range(self._largoRestante):
                            if check_cell(self.atacadas, i[0], i[1]-o, 1):
                                np.delete(self.posiblesDirecciones, i, 0)
                                break
                    else:
                        for o in range(self._largoRestante):
                            if check_cell(self.atacadas, i[0], i[1]+o, 1):
                                np.delete(self.posiblesDirecciones, i, 0)
                                break
                elif i[1] == self.barcoOrigen[self.barcosNum, 1][1]:
                    if i[1] < self.barcoOrigen[self.barcosNum, 0][1]:
                        for o in range(self._largoRestante):
                            if check_cell(self.atacadas, i[0]-o, i[1], 1):
                                np.delete(self.posiblesDirecciones, i, 0)
                                break
                    else: 
                        for o in range(self._largoRestante):
                            if check_cell(self.atacadas, i[0]+o, i[1], 1):
                                np.delete(self.posiblesDirecciones, i, 0)
                                break'''

            deadEnd = True
            for i in self.posiblesDirecciones:
                if check_cell(self.atacadas, i[0], i[1], 0):
                    atx, aty = i
                    deadEnd = False
                    break
            if deadEnd:
                atx, aty = self.barcoOrigen[self.barcosNum, 1]
                self.posiblesDirecciones = np.array([[atx, aty+1],
                                                    [atx, aty-1],
                                                    [atx+1, aty],
                                                    [atx-1, aty]], dtype=int)
                deadEnd = True

                for i in range(len(self.posiblesDirecciones)-1, -1, -1):
                    if self.posiblesDirecciones[i, 0] < 0 or self.posiblesDirecciones[i, 0] >= self._tamano_tablero or self.posiblesDirecciones[i, 1] < 0 or self.posiblesDirecciones[i, 1] >= self._tamano_tablero:
                        self.posiblesDirecciones = np.delete(self.posiblesDirecciones, i, 0)
            
                for i in self.posiblesDirecciones:
                    if check_cell(self.atacadas, i[0], i[1], 0):
                        atx, aty = i
                        deadEnd = False
                        break
                if deadEnd:
                    self.mode = 1
                    self.barcosNum += 1
                    atx, aty = self.atacar()
                else:
                    self.barcoOrigen[self.barcosNum, 0] = [atx, aty]
            self.atacadas[atx, aty] = 1
            if tablero_player1[atx, aty] == 1:
                if atx == self.barcoOrigen[self.barcosNum, 0][0]:
                    self.barcosDireccion[self.barcosNum] = 0
                else:
                    self.barcosDireccion[self.barcosNum] = 1
                self.barcoOrigen[self.barcosNum, 0] = [atx, aty]
            return atx, aty
        
def single_player_game_loop():
    game_running = True
    while game_running: # loop principal del juego
        # JUGADOR 1
        os.system('cls') # limpia la consola
        print("player 1") # anuncia el turno del jugador 1
        print_board(tablero_player2) # muestra el tablero del jugador 2
        print("Su truno de atacar")

        # pide las dos pocisiones de ataque
        atx, aty = ask_for_position("Pase la posicion x de la celda: \n -", 1), ask_for_position("Pase la posicion y de la celda: \n -", 1) 
        
        os.system('cls') # limpia la consola
        # si la celda atacada es igual a 1, se muestra HIT, si no se muestra MISS
        if tablero_player2[atx, aty] == 1:
            print(f"{Fore.GREEN}HIT{Fore.WHITE}")
            tablero_player2[atx, aty] = 3  # se almacena el valor 3 en la celda atacada indicando que hay un barco
        elif tablero_player2[atx, aty] == 3: # revisa si la celda ya fue golpeada y solia haber un barco
            print(f"{Fore.GREEN}Already HIT{Fore.WHITE}")
        else: # si no habia un barco
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player2[atx, aty] = 4 # se almacena el valor 4 en la celda atacada indicando que no hay barco
        print_board(tablero_player2) # muestra el nuevo tablero del jugador 2

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = np.bitwise_not(check_if_game_ended(tablero_player2))
        if not game_running:
            os.system('cls') # limpia la consola
            print("FIN DEL JUEGO \n A gandado el jugador 1")
            break # termina el juego

        time.sleep(1.5) # espera un segundo para que el jugador pueda ver el ataque
        os.system('cls') # limpia la consola

        # COMPUTADORA
        print("Computadora") # anuncia el turno del jugador 1
        print_board(tablero_player1) # muestra el tablero del jugador 2
        print("Va a atacar")
        print(f"{Fore.GREEN}                  _______")
        print(f"               _/       \\_")
        print(f"              / |       | \\    ")
        print(f"             /  |__   __|  \\   ")
        print(f"            |__/((o| |o))\\__|   ")
        print(f"            |      | |      |")
        print(f"            |\\     |_|     /|")
        print(f"            | \\           / |")
        print(f"             \\| /  ___  \\ |/")
        print(f"              \\ | / _ \\ | /")
        print(f"               \\_________/")
        print(f"                _|_____|_")
        print(f"           ____|_________|____")
        print(f"          /                   \\")
        print(f"         /                     \\")
        print(f"        /         battle        \\")
        print(f"        |          robot        |")
        print(f"        |   _________________   |\n\n")
        inFrase = np.random.randint(3, len(frases_malvadas_epicas)) # selecciona una frase aleatoria normal
        if tablero_player2[atx, aty] == 3:
            inFrase = np.random.randint(0, len(frases_malvadas_epicas)) # selecciona una frase aleatoria de HIT
        print(f"Robot: ", frases_malvadas_epicas[inFrase], f"\n \n{Fore.WHITE}") # imprime la frase elegida

        time.sleep(1) # espera un segundo para que el jugador pueda ver el ataque
        # pide las dos pocisiones de ataque
        atx, aty = computer.atacar()
        print(f"Vot a atacar a {atx}, {aty}!!")
        time.sleep(3) # espera un segundo para que el jugador pueda ver el ataque
        os.system('cls') # limpia la consola
        # si la celda atacada es igual a 1, se muestra HIT, si no se muestra MISS
        if tablero_player1[atx, aty] == 1:
            print(f"{Fore.GREEN}HIT{Fore.WHITE}")
            tablero_player1[atx, aty] = 3 # se almacena el valor 3 en la celda atacada indicando que hay un barco
        elif tablero_player1[atx, aty] == 3: # revisa si la celda ya fue golpeada y solia haber un barco
            print(f"{Fore.GREEN}Already HIT{Fore.WHITE}")
        else: # si no habia un barco
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player1[atx, aty] = 4 # se almacena el valor 4 en la celda atacada indicando que no hay barco
        print_board(tablero_player1)

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = np.bitwise_not(check_if_game_ended(tablero_player1))
        if not game_running:
            os.system('cls') # limpia la consola
            print(f"{Back.WHITE}{Fore.GREEN}FIN DEL JUEGO \n A gandado la computadora {Back.BLACK}{Fore.WHITE}")
            break # termina el juego

        input("preciona enter para seguir") # esperar a que se pase la computadora

jugando = True
while jugando: # main loop
    game_mode = get_game_mode() # pide el modo de juego
    get_new_board(np.bitwise_not(game_mode)) # crea tableros nuevos y pide las posiciones a los jugadores

    if game_mode: # empieza el juego en el modo seleccionado
        two_player_game_loop()
    else:
        single_player_game_loop()

    volver_a_jugar = input(f"\n {Fore.WHITE}{Back.BLACK}volver a jugar? \n {Back.WHITE}{Fore.GREEN}y/{Fore.RED}n \n -{Fore.WHITE}{Back.BLACK}")
    Fore.WHITE, Back.BLACK # reestablece el color de letra y fondo
    # revisa la respuesta del usuario y acciona acordemente
    if volver_a_jugar == "n":
        jugando = False # termina el juego
        print("Chau :)\n",  
        " _           _   _   _           _     _       \n",
        "| |         | | | | | |         | |   (_)      \n",
        "| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  \n",
        "| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ \n",
        "| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) | \n",
        "|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ \n", 
        "                                        | |    \n "
        "                                        |_|    \n ") # mensaje de salida
        break
    elif volver_a_jugar == "y":
        pass # volver a jugar
    else: # la respuesta no es la esperada
        print(f"no entendi que dijiste... \n voy a asumir que queres jugar de nuveo porque mi juego es buenisimo :)") # el mensaje divertido
        time.sleep(1.5) # esperar para que se lea mensaje divertido
    os.system('cls') # limpia la consola

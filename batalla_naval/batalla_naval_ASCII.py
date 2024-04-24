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
    - El tablero es de 10x10
    - Los barcos ocupan una sola celda

    Juego por: Manuel Rao, Joaquin Blanco, Tobias Esteban Majic.

    GitHub:
    - https://github.com/porfi2089/Chona_2024

'''

tamano_tablero = 20
tablero_player1 = np.zeros([tamano_tablero, tamano_tablero]) # creo una array de 10x10 llena solo de ceros
tablero_player2 = tablero_player1.copy() # copiamos la primera array y la asignamos como el tablero de player 2
barcos = 0 # variable que va a almacenar la cantidad de barcos que van a haber en el tablero
Fore.WHITE, Back.BLACK # setear el color de las letras y del fondo a defalult
os.system('cls') # limpia la consola


# pide las posiciones de cada celda ocupada y las transforma en una array de np
def ask_for_position(text, pos):
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

        if 1>inp>tamano_tablero and pos == 1: # revisar si el valor esta dentro del tablero
            ask_flag = True # si no esta dentro del tablero, se repite el loop
            print(f"{Fore.RED}Mala respuesta, numero debe estar entre 1 y 10{Fore.WHITE}")
    return inp


# definimos una funcion que se va a encargar de asignar valores a una tabla dada en posiciones especificas
def asaign_values(tabla: np.ndarray, valores: np.ndarray, posiciones: np.ndarray, rotaciones: int, largo: int):
    '''asigna valores a una tabla en posiciones especificas'''
    for value, enum in zip(valores, range(len(valores))): # unimos los valores pasados y el indice de los valores
        x_off = rotaciones[enum] % 2 # se calcula el offset en x
        y_off = (rotaciones[enum] + 1) % 2 # se calcula el offset en y
        # se asigna el valor dado a la posicion en la tabla establecida
        for i in range(largo):
            i -= 1
            if posiciones[enum, 0] + i*x_off > tamano_tablero:
                i -= largo
            elif posiciones[enum, 0] + i*x_off < 0:
                i += largo
            if posiciones[enum, 1] + i*y_off > tamano_tablero:
                i -= largo
            elif posiciones[enum, 1] + i*y_off < 0:
                i += largo
            tabla[posiciones[enum, 0] + i*x_off, posiciones[enum, 1] + i*y_off] = value


def get_game_mode() -> bool: # pide el modo de juego
    '''pide el modo de juego y devuelve un booleano que indica si el juego es de dos jugadores o contra la computadora'''
    print("Bienvenido a la batalla naval \n",  
        " _           _   _   _           _     _       \n",
        "| |         | | | | | |         | |   (_)      \n",
        "| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  \n",
        "| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ \n",
        "| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) | \n",
        "|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ \n", 
        "                                       | |    \n"
        "                                       |_|    \n") # mensaje de bienvenida
    print(f"{Fore.WHITE}{Back.BLACK}Modo de juego \n {Fore.GREEN}1{Fore.WHITE}: Jugador vs Jugador \n {Fore.RED}2{Fore.WHITE}: Jugador vs Computadora \n -{Fore.WHITE}{Back.BLACK}")
    game_mode = input()
    if game_mode == "1":
        return True
    elif game_mode == "2":
        return False
    else:
        print(f"{Fore.RED}Respuesta invalida{Fore.WHITE}")
        get_game_mode()
        os.system('cls') # limpia la consola


def get_new_board(single_player: bool): # pide las posiciones de los barcos a los jugadores y los asigna a los tableros
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
            for c in range(2):
                posiciones[b, c] = ask_for_position(f"Pase la posicion "+str(c)+" del barco "+str(b)+": \n -", 1) # pide las cordenadas de cada celda ocupada
            rotaciones[b] = ask_for_position(f"Rotaciones del barco "+str(b)+": \n -", 0) # pide la cantidad de rotaciones que va a tener el barco
            os.system('cls') # limpia la consola

        tablero = np.zeros([tamano_tablero, tamano_tablero]) # se crea una tabla vacia
        asaign_values(tablero, values, posiciones, rotaciones, largo) # asignamos valores para barcos TEST
        
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
        tablero_player2 = tablero.copy()


def print_board(tablero):
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
            line = line + n # se añade la celda a la linea
        print(line+f"{Back.BLACK}{Fore.WHITE}") # se imprime la linea 


def check_if_game_ended(tablero): # checkear si alguno de los jugadores a ganado
    if 1 in tablero: # si sigue habiendo barcos en el tablero
        return False # el juego sige
    else: # sino
        return True # el juego a terminado

def check_cell(self,list, x, y, value):
        if list[x, y] == value:
            return True

def two_player_game_loop():
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


class Computer: # clase que representa a la IA de la computadora
    def __init__(self, barcos: int, largo: int, tamano_tablero: int):
        self.tablero = np.zeros([tamano_tablero, tamano_tablero])
        self.atacadas = np.zeros([tamano_tablero, tamano_tablero])
        self.barcosEncontrados = np.zeros([barcos, largo+2, 3]) # this list will contain the position of the ship and if it has been destroyed
        self.barcosNum = 0
        self._barcos = barcos
        self._largo = largo
        self._tamano_tablero = tamano_tablero
        self.mode = 1 # 1 = grid random, 2 = idntify, 3 = destroy
    def atacar(self):
        if self.mode == 1:
            atx, aty = np.random.randint(0, int(self._tamano_tablero/2))*2, np.random.randint(0, int(self._tamano_tablero/2))*2 # busca en todos los numeros pares
            while self.atacadas[atx, aty] == 1:
                atx, aty = np.random.randint(0, int(self._tamano_tablero/2))*2, np.random.randint(0, int(self._tamano_tablero/2))*2 # busca en todos los numeros pares

            self.atacadas[atx, aty] = 1
            if tablero_player1[atx, aty] == 1:
                self.barcosEncontrados[self.barcosNum, 2] = True, atx, aty
                self.barcosNum += 1
            return atx, aty
        elif self.mode == 2:
            b = self.barcosEncontrados[self.barcosNum-1]
            p = b[2:self._largo+2]

                
                    
            
    

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

        input("preciona enter cuando el jugador 2 tenga la computadora") # esperar al cambio de jugadores

        # COMPUTADORA
        os.system('cls') # limpia la consola
        print("Computadora") # anuncia el turno del jugador 1
        print_board(tablero_player1) # muestra el tablero del jugador 2
        print("Va a atacar")

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
        print("Chau :)") # mensaje de salida
        break
    elif volver_a_jugar == "y":
        pass # volver a jugar
    else: # la respuesta no es la esperada
        print(f"no entendi que dijiste... \n voy a asumir que queres jugar de nuveo porque mi juego es buenisimo :)") # el mensaje divertido
        time.sleep(1.5) # esperar para que se lea mensaje divertido
    os.system('cls') # limpia la consola
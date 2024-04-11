import numpy as np # importamos la libreria np que cuenta con una multitud de 
import os # os es una libreria que tiene muchas funciones que permiten interactuar con el sistema, en este caso la vamos a usar para la simple funcion de limpiar la consola
from colorama import Fore, Back # colorama es una libreria de formateo de texto para la terminal, la vamos a usar para darle color a los mensajes
import time # time es una libreria que viene con un monton de librerias que tienen que ver con el tiempo, nosotros la vamos a usar para esperar una determinada cantidad de tiempo en ciertos lugares 
# Por: Manuel Rao, Joaquin Blanco, Tobias Esteban Majic.

tablero_player1 = np.zeros([10, 10]) # creo una array de 10x10 llena solo de ceros
tablero_player2 = tablero_player1.copy() # copiamos la primera array y la asignamos como el tablero de player 2
Fore.WHITE, Back.BLACK # setear el color de las letras y del fondo a defalult

# pide las posiciones de cada celda ocupada y las transforma en una array de np
def ask_for_position(text, pos):
    ask_flag = True
    while ask_flag:
        inp = input(text)
        ask_flag = False 
        try: # utilizamos el metodo try por si llegan a pasar un valor que no sea un numero entero 
            inp = int(inp)-pos
        except:
            print(f"{Fore.RED}Mala respuesta, responder solo numeros enteros{Fore.WHITE}")
            ask_flag = True
            continue

        if 1>inp>10 and pos == 1: # revisar si el valor esta dentro del tablero
            ask_flag = True
            print(f"{Fore.RED}Mala respuesta, numero debe estar entre 1 y 10{Fore.WHITE}")
    return inp

# definimos una funcion que se va a encargar de asignar valores a una tabla dada en posiciones especificas
def asaign_values(tabla, valores, posiciones):
    for value, enum in zip(valores, range(len(valores))): # unimos los valores pasados y el indice de los valores 
        tabla[posiciones[enum, 0], posiciones[enum, 1]] = value # se asigna el valor dado a la posicion en la tabla establecida

def get_new_board():
    global tablero_player1 # se asegura de que la variable este definida dentro de la funcion
    global tablero_player2 # se asegura de que la variable este definida dentro de la funcion
    for i in range(2): # este for loop repite el codigo una vez por cada jugador
        print("Player " + str(i+1)) # anunciamos que jugador debe completar los campos
        barcos = ask_for_position(f"Cantidad de celdas ocupadas por barcos \n -", 0) # pedimos la cantidad de celdas que van a ocupar los barcos
        values = np.ones((barcos)) # transformamos la cantidad de celdas en una lista de unos de ese largo
        posiciones = np.zeros((barcos, 2), dtype=np.uint32) # crea la lista de posciones de los barcos
        # pide cada picision de cada barco
        for b in range(barcos): 
            for c in range(2):
                posiciones[b, c] = ask_for_position("Pase la posicion "+str(c)+" de la celda "+str(b)+": \n -", 1) # pide las cordenadas de cada celda ocupada
        tablero = np.zeros([10, 10]) # se crea una tabla vacia
        asaign_values(tablero, values, posiciones) # asignamos valores para barcos TEST
        if i == 0:
            tablero_player1 = tablero.copy()
        else:
            tablero_player2 = tablero.copy()

def print_board(tablero):
    tablero = tablero.copy() # crea una copia del tablero
    tablero = np.maximum(tablero - 1, np.zeros((10, 10))) # remplazamos al 1 por 0 para que no se muestre en el tablero
    for i in enumerate(tablero): # itera por las filas de la tabla
        i = i[0]
        line = f"{Back.BLUE}-" # se crea una variable que va a almacernar la info de la linea
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

def game_loop():
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
            tablero_player2[atx, aty] = 3
        else:
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player2[atx, aty] = 4
        print_board(tablero_player2) # muestra el nuevo tablero del jugador 2

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = -check_if_game_ended(tablero_player2)
        if not game_running:
            os.system('cls') # limpia la consola
            print("FIN DEL JUEGO \n A gandado el jugador 1")
            break

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
            tablero_player1[atx, aty] = 3
        else:
            print(f"{Fore.RED}MISS{Fore.WHITE}")
            tablero_player1[atx, aty] = 4
        print_board(tablero_player1)

        # revisar si a terminado el juego y dar el mensaje de FIN si es el caso
        game_running = -check_if_game_ended(tablero_player1)
        if not game_running:
            os.system('cls') # limpia la consola
            print(f"{Back.WHITE}{Fore.GREEN}FIN DEL JUEGO \n A gandado el jugador 2 {Back.BLACK}{Fore.WHITE}")
            break

        input("preciona enter cuando el jugador 2 tenga la computadora")

jugando = True
while jugando: # main loop
    get_new_board()
    game_loop()
    volver_a_jugar = input(f"\n {Back.WHITE}{Fore.BLUE}volver a jugar? \n {Back.WHITE}{Fore.GREEN}Y/{Fore.RED}N \n -").lower
    if volver_a_jugar == "n":
        jugando = False
        print("Chau :)")
    elif volver_a_jugar == "y":
        pass
    else:
        print("no entendi que dijiste... \n voy a asumir que queres jugar de nuveo porque mi juego es buenisimo :)")
        time.sleep(1000)
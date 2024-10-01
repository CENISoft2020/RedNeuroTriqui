import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Crear el tablero de triqui (9 posiciones)
def create_board():
    return np.zeros((3, 3))

# Verificar si hay un ganador
def check_winner(board):
    # Verificar filas, columnas y diagonales
    for i in range(3):
        if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
            return 1  # El jugador 1 gana
        if np.all(board[i, :] == -1) or np.all(board[:, i] == -1):
            return -1  # El jugador -1 gana

    # Diagonales
    if board[0, 0] == board[1, 1] == board[2, 2] != 0:
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] != 0:
        return board[0, 2]

    return 0  # No hay ganador

# Crear la red neuronal
def create_model():
    model = keras.Sequential()
    model.add(layers.Input(shape=(9,)))  # 9 neuronas de entrada (el tablero)
    model.add(layers.Dense(64, activation='relu'))  # Capa oculta con 64 neuronas
    model.add(layers.Dense(64, activation='relu'))  # Otra capa oculta
    model.add(layers.Dense(9, activation='softmax'))  # 9 neuronas de salida, una por cada movimiento posible
    model.compile(optimizer='adam', loss='mse')
    return model

# Preparar los datos para entrenamiento
def prepare_data():
    # Ejemplos de tableros (X, O) y sus movimientos correctos (jugadas óptimas)
    X_train = np.array([
        [1, 0, 0, 0, -1, 0, 0, 0, 0],  # Estado del tablero
        [1, 1, 0, 0, -1, 0, 0, -1, 0],
        [-1, 1, 1, 0, 0, 0, -1, 0, 0],
        [0, 0, 1, -1, 1, 0, 0, -1, 0],
    ])

    # Movimientos óptimos para esos tableros (uno por cada posición)
    y_train = np.array([
        [0, 1, 0, 0, 0, 0, 0, 0, 0],  # La mejor jugada es poner la ficha en la casilla 1
        [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Mejor jugada en la casilla 3
        [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Mejor jugada en la casilla 3
        [0, 0, 0, 0, 0, 1, 0, 0, 0],  # Mejor jugada en la casilla 5
    ])

    return X_train, y_train

# Entrenar el modelo
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=500)

# Predecir la mejor jugada en base al estado del tablero
def predict_move(model, board):
    board_flat = board.flatten().reshape(1, -1)
    prediction = model.predict(board_flat)
    move = np.argmax(prediction)
    return divmod(move, 3)  # Devolver la posición de la mejor jugada (fila, columna)

# Jugar una partida
def play_game(model):
    board = create_board()
    current_player = 1

    while check_winner(board) == 0 and np.any(board == 0):  # Continuar hasta que haya un ganador o empate
        print("Turno del jugador:", "X" if current_player == 1 else "O")
        print(board)

        if current_player == 1:
            row, col = predict_move(model, board)
        else:
            row, col = map(int, input("Introduce tu jugada (fila columna): ").split())

        if board[row, col] == 0:
            board[row, col] = current_player
            current_player *= -1  # Cambiar de jugador
        else:
            print("Movimiento inválido. Intenta de nuevo.")

    winner = check_winner(board)
    if winner == 1:
        print("Ganó X!")
    elif winner == -1:
        print("Ganó O!")
    else:
        print("Empate!")
    print(board)

# Main
if __name__ == "__main__":
    model = create_model()
    X_train, y_train = prepare_data()
    train_model(model, X_train, y_train)
    play_game(model)

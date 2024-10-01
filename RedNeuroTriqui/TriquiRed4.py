import random
import matplotlib.pyplot as plt

class TicTacToeGame:
    def __init__(self):
        self.trainings = []
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def read_training_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            current_move = None
            current_board = []
            for line in lines:
                line = line.strip()

                if line == '':
                    continue

                # Si la línea contiene coordenadas, guarda el movimiento
                if line[0].isdigit():  # Verifica si la línea comienza con un número
                    if current_board:
                        # Almacena el último movimiento junto con el tablero
                        self.trainings.append((current_move, current_board))
                        current_board = []  # Reinicia el tablero para el siguiente bloque

                    # Lee las coordenadas del movimiento
                    parts = line.split()
                    if len(parts) == 2:
                        current_move = (int(parts[0]), int(parts[1]))
                    else:
                        print(f"Error: formato incorrecto en la línea '{line}'")
                else:
                    # Almacena cada fila del tablero
                    current_board.append(list(line))

            # Asegúrate de que el último bloque sea agregado
            if current_move is not None and current_board:
                self.trainings.append((current_move, current_board))

        except FileNotFoundError:
            print(f"Error: No se puede encontrar el archivo '{filename}'")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    def print_trainings(self):
        if not self.trainings:
            print("No se encontraron datos de entrenamiento.")
            return

        for i, (move, board) in enumerate(self.trainings):
            print(f"\nEntrenamiento {i + 1}:")
            print(f"Siguiente movimiento: {move}")
            for row in board:
                print(' '.join(row))
        print(f"\nTotal de entrenamientos: {len(self.trainings)}")

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def check_winner(self):
        # Verifica filas, columnas y diagonales para un ganador
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != '-':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '-':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '-':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '-':
            return self.board[0][2]

        return None

    def play_game(self, player1, player2):
        players = [player1, player2]
        scores = {player1: 0, player2: 0, 'draw': 0}
        
        for _ in range(100):  # Jugar 100 partidas
            self.board = [['-' for _ in range(3)] for _ in range(3)]  # Reiniciar el tablero
            self.current_player = 'X'
            while True:
                self.print_board()

                # Generar movimiento aleatorio
                row, col = self.get_random_move()

                if self.board[row][col] == '-':
                    self.board[row][col] = self.current_player
                else:
                    print("Movimiento inválido. Intenta nuevamente.")
                    continue

                winner = self.check_winner()
                if winner:
                    self.print_board()
                    print(f"El ganador es: {winner}")
                    scores[winner] += 1
                    break

                if all(cell != '-' for row in self.board for cell in row):  # Empate
                    self.print_board()
                    print("¡Es un empate!")
                    scores['draw'] += 1
                    break

                # Cambiar de jugador
                self.current_player = player2 if self.current_player == player1 else player1
        
        return scores

    def get_random_move(self):
        # Método para obtener un movimiento aleatorio
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '-']
        return random.choice(empty_cells) if empty_cells else (0, 0)

    def plot_results(self, scores):
        # Graficar los resultados
        labels = list(scores.keys())
        values = list(scores.values())

        plt.bar(labels, values)
        plt.xlabel('Jugadores')
        plt.ylabel('Victorias')
        plt.title('Resultados del Juego de Tic Tac Toe')
        plt.show()


# Uso del código
game = TicTacToeGame()
game.read_training_file('C:/Users/utp/Documents/Class300924/RedNeuroTriqui/board_train_data.txt')
game.print_trainings()

# Jugadores automáticos
player1 = 'X'
player2 = 'O'

# Jugar el juego y obtener resultados
scores = game.play_game(player1, player2)

# Graficar los resultados
game.plot_results(scores)

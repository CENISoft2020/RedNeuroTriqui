class TicTacToeGame:
    def __init__(self):
        self.trainings = []

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


# Uso del código
game = TicTacToeGame()
game.read_training_file('C:/Users/utp/Documents/Class300924/RedNeuroTriqui/board_train_data.txt')  # Asegúrate de usar la ruta correcta
game.print_trainings()

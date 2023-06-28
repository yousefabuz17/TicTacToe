from random import randint
from time import sleep

BOARD_ROW: int = 3
BOARD_COL: int = 3
CHOICES: list = ['X', 'O']

class TicTacToe:
    stats: list = [0, 0]
    
    def __init__(self) -> None:
        self.board: list = ['-' for _ in range(BOARD_ROW * BOARD_COL)]
        self.last_move: list = [-1]
    
    def print_board(self) -> None:
        """
        Prints the current state of the game board.
        """
        print(
            f'''
                         {self.board[0]} | {self.board[1]} | {self.board[2]}
                        -----------
                         {self.board[3]} | {self.board[4]} | {self.board[5]}
                        -----------
                         {self.board[6]} | {self.board[7]} | {self.board[8]}
    Game Stats:
    AI: {self.stats[0]}   USER: {self.stats[-1]}
            ''')
    
    def set_board(self, char: str, place: int) -> bool:
        """
        Sets the given character at the specified place on the game board.
        Returns True if the move is valid, False otherwise.
        """
        if self.board[place] == '-':
            self.board[place] = char
            self.last_move[0] = place
            return True
        return False

    def check_win(self, char: str) -> bool:
        """
        Checks if the specified character has won the game.
        Returns True if the character has won, False otherwise.
        """
        full_board = list(map(''.join, 
                            [self.board[:3], self.board[3:6], self.board[6:9],  # Rows
                            self.board[::3], self.board[1::3], self.board[2::3], # Columns
                            self.board[::4], self.board[6::-2][:-1]]))              # Diagonals
        return any([char * 3 in full_board])
    
    def choose_char(self) -> tuple:
        """
        Allows the user to choose their character ('X' or 'O').
        Returns a tuple containing the chosen character for the user and the AI.
        """
        count: int = 0
        attempts: list = []
        while count < 5:
            user_char: str = input(f'Enter player character {CHOICES}: ').upper()
            attempts.append(user_char)
            if user_char in CHOICES:
                return (user_char, 'O' if user_char == 'X' else 'X')
            else:
                count += 1
                print(f'{user_char} is not an option, only {CHOICES}...   Fail Counter: {count}')
        print('\nFailed, your attempted tries:\t')
        print(dict(Attempts=attempts))
    
    def ai(self, ai_char: str, user_char: str) -> None:
        """
        Implements the AI's move on the game board.
        """
        for col in range(BOARD_COL*BOARD_ROW):
            if self.set_board(ai_char, col):
                if self.check_win(ai_char):
                    return
                self.board[col] = '-'
        
        for col in range(BOARD_COL*BOARD_ROW):
            if self.set_board(user_char, col):
                if self.check_win(user_char):
                    self.board[col] = '-'
                    self.set_board(ai_char, col)
                    return
                self.board[col] = '-'
        
        while True:
            col = randint(0, 8)
            if self.set_board(ai_char, col):
                return
    
    def player_stats(self, winner: str) -> None:
        """
        Updates the game statistics based on the winner.
        """
        self.stats[0] += 1 if winner == 'AI' else 0
        self.stats[-1] += 1 if winner == 'USER' else 0


def main() -> None:
    tic = TicTacToe()
    RUNNING: bool = True
    tic.print_board()
    try:
        user_char, ai_char = tic.choose_char()
        while RUNNING:
            user_col: int = int(input('Enter a place (0-8): '))
            while not tic.set_board(user_char, user_col):
                print('Invalid option, try again! ')
                user_col = int(input('Enter a place (0-8): '))
            
            tic.print_board()
            if all([x != '-' for x in tic.board]):
                    print('Draw! Good try though...')
                    RUNNING = False
                    break
            if not tic.check_win(user_char):
                tic.ai(ai_char, user_char)
                sleep(0.4)
                tic.print_board()
                if tic.check_win(ai_char):
                    print('\nAI wins!')
                    tic.player_stats('AI')
                    RUNNING = False
            else:
                print('Wow, you actually won!')
                tic.player_stats('USER')
                RUNNING = False
    except KeyboardInterrupt:
        print('\n\nKeyboardInterrupt detected, ending program...')
        print('Good Day!')
        quit()
    
    tic.print_board()
    play_again: str = input('\nPlay again (Y/N)? ')
    if play_again.upper() != 'N':
        main()
    print('Quitting program...')
    sleep(0.5)
    quit()

if __name__ == '__main__':
    main()
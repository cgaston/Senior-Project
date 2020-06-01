from Players import Player, HumanPlayer, CPUPlayer
from ChessBoard import ChessBoard
from Pieces import Color


# This module will have the main function

def main():
    board = ChessBoard()
    change_settings = 0
    while True:
        if change_settings == 0:
            num_player = get_user_response("How many players do you want (1-2)?: ", "012")
            if num_player == 0:
                p1 = CPUPlayer(Color.WHITE)
                p2 = CPUPlayer(Color.BLACK)
            elif num_player == 1:
                who_first = get_user_response("Do you want to be White(W) or Black(B)?: ", "WB")
                difficulty = get_user_response("How good do you want the computer to play (1-9): ", "123456789")
                if who_first == 0:
                    p1 = HumanPlayer(Color.WHITE)
                    p2 = CPUPlayer(Color.BLACK)
                else:
                    p1 = CPUPlayer(Color.WHITE)
                    p2 = HumanPlayer(Color.BLACK)
            else:
                p1 = HumanPlayer(Color.WHITE)
                p2 = HumanPlayer(Color.BLACK)
        board.init_board()
        play_game(p1, p2, board)
        pa_resp = get_user_response("Do you want to play again Y/N: ", "YN")
        if pa_resp == 1:  # break if user wanted to quit
            break
        change_settings = get_user_response("Do you want to change the settings Y/N: ", "YN")
    del board
    del p1
    del p2


def play_game(p1: Player, p2: Player, board: ChessBoard):
    p1.reset_game()
    p2.reset_game()
    cur_player = 0
    quit_game = False
    while True:
        board.display_board()
        if quit_game:
            break
        if cur_player == 0:
            quit_game = p1.move(board)
        else:
            quit_game = p2.move(board)
        cur_player = 1 - cur_player  # switch whose turn it is
        print("")


def get_user_response(question: str, acc_resp: str) -> int:
    while True:
        inp = input(question)
        resp = inp.upper()
        if resp in acc_resp:
            for i in range(len(acc_resp)):
                if resp == acc_resp[i]:
                    return i


# This is the code to be run
main()

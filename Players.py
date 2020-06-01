# This module will include the abstract class Player and the two derived Classes HumanPlayer and CPUPlayer
from abc import ABC, abstractmethod
from ChessBoard import ChessBoard, MoveType
from Pieces import Color
import re


class Player(ABC):

    # constructor
    def __init__(self, color: Color):
        self.player_score = 0
        self.player_color = color

    def reset_game(self):
        self.player_score = 0

    def add_to_score(self, num):
        self.player_score += num

    def color_to_string(self, oppo: bool = False) -> str:
        if self.player_color == Color.WHITE:
            if oppo:
                return "Black"
            else:
                return "White"
        elif self.player_color == Color.BLACK:
            if oppo:
                return "White"
            else:
                return "Black"
        else:
            return "Blank"

    @abstractmethod
    def move(self, board: ChessBoard):
        pass


# ==============================================================================#


class HumanPlayer(Player):

    # constructor
    def __init__(self, color: Color):
        super(HumanPlayer, self).__init__(color)

    # Override
    def move(self, board: ChessBoard) -> bool:
        while True:
            resp_string = self.ask_for_player_move()
            if resp_string == "q":
                return True
            # turn response into list of 4 ascii values
            resp = [ord(c) for c in resp_string]
            ord_string = "a1a1"
            origin = [ord(c) for c in ord_string]  # create list for origin ascii values
            diff = []

            # subtract inputted coordinates from origin to get coordinates as 0 based index in 2d list
            zip_object = zip(resp, origin)
            for resp_i, origin_i in zip_object:
                diff.append(resp_i - origin_i)

            if board.is_valid_move(diff[1], diff[0], diff[3], diff[2], self.player_color):
                # Have the board make the move and return True if checkmate was a achieved and false if it wasn't
                # if move failed then loop is continued and nothing is returned
                move_type = board.move_piece(diff[1], diff[0], diff[3], diff[2], self.color_to_string(True))
                if move_type == MoveType.CHECKMATE:
                    return True
                elif move_type == MoveType.MOVE_PASSED:
                    return False
            else:
                print("Error invalid move. Please try again!")

    def ask_for_player_move(self) -> str:
        while True:
            inp = input("Please enter {}'s move or q to quit: ".format(self.color_to_string()))
            resp = inp.lower()
            pattern = re.compile("([a-h][1-8]){2}")
            if pattern.match(resp) or resp == "q":
                return resp
            print("Invalid selection please enter a start space and a destination space.",
                  "For example: e2e4")


# ==============================================================================#


class CPUPlayer(Player):

    # constructor
    def __init__(self, color: Color):
        super(CPUPlayer, self).__init__(color)

    # Override
    def move(self, board: ChessBoard):
        x = 0

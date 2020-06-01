from enum import IntEnum


class Color(IntEnum):
    WHITE = 0
    BLACK = 1
    BLANK = 2


# ==============================================================================#


from abc import ABC, abstractmethod
import math


# abstract class Piece to be implemented by each type of Chess Piece
class Piece(ABC):

    # constructor
    def __init__(self, color=Color.BLANK, num: int = -1):
        self.piece_color = color  # data member piece color
        self.killed = False  # data member of if piece is "killed" or not
        self.has_moved = False  # represents if piece moved or not
        self.number = num  # represents

    def is_killed(self) -> bool:
        return self.killed == True

    def set_killed(self, is_killed: bool):
        killed = is_killed

    def piece_moved(self):
        self.has_moved = True

    def opp_color(self) -> Color:
        """
        this method returns the opposite color of the piece that called it
        if piece is white return black
        if piece is black return white
        if piece is blank return blank
        :return: Color type that is opposite of color of piece that called the method
        """
        if self.piece_color == Color.WHITE:
            return Color.BLACK
        elif self.piece_color == Color.BLACK:
            return Color.WHITE
        else:
            return Color.BLANK

    @abstractmethod
    def to_string(self):
        pass

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        pass


# ==============================================================================#


class King(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(King, self).__init__(color, num)
        self.can_castle = False

    def is_castling_done(self) -> bool:
        return self.castling_done == True

    def set_castling_done(self, castling_done: bool):
        self.castling_done = castling_done

    # def is_valid_castling(self, board: ChessBoard, start: Spot, end: Spot) -> bool:

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "K" if self.piece_color == Color.WHITE else "k"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a King can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture:
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the King can move to that position
        """
        row_diff = abs(r2 - r1)
        col_diff = abs(c2 - c1)

        # this code allows for castling by checking if king has moved yet and if the person is trying to castle
        if not self.has_moved:
            if row_diff == 0 and col_diff == 2:
                return True

        # return whether king tried to move more than 1 space in a specific direction
        return max(row_diff, col_diff) < 2


# ==============================================================================#

class Queen(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(Queen, self).__init__(color, num)

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "Q" if self.piece_color == Color.WHITE else "q"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a Queen can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture:
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the Queen can move to that position
        """

        row_diff = abs(r2 - r1)
        col_diff = abs(c2 - c1)

        # return whether change in row and column was the same(diagonal movement) or if
        # one of the changes was 0 (horizontal or vertical)
        return row_diff == col_diff or min(row_diff, col_diff) == 0


# ==============================================================================#

class Knight(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(Knight, self).__init__(color, num)

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "N" if self.piece_color == Color.WHITE else "n"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a Knight can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture:
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the Knight can move to that position
        """

        row_diff = abs(r2 - r1)
        col_diff = abs(c2 - c1)

        # return whether the sum of the absolute value of the differences in coordinates is 3 because
        # this means that the knight tried to move 3 spaces in the L shape like it should
        return max(row_diff, col_diff) < 3 and row_diff + col_diff == 3


# ==============================================================================#

class Bishop(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(Bishop, self).__init__(color, num)

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "B" if self.piece_color == Color.WHITE else "b"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a Bishop can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture:
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the Bishop can move to that position
        """

        row_diff = abs(r2 - r1)
        col_diff = abs(c2 - c1)

        # return whether the absolute value of the changes in row and column were the same
        # shows whether the bishop tried to move diagonally or not
        return row_diff == col_diff


# ==============================================================================#

class Rook(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(Rook, self).__init__(color, num)

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "R" if self.piece_color == Color.WHITE else "r"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a Rook can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture:
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the Rook can move to that position
        """

        row_diff = abs(r2 - r1)
        col_diff = abs(c2 - c1)

        # return whether at least one of the changes was 0
        # shows whether the rook tried to move horizontally/vertically or not
        return min(row_diff, col_diff) == 0


# ==============================================================================#

class Pawn(Piece):

    # constructor
    def __init__(self, color: Color, num: int):
        super(Pawn, self).__init__(color, num)

    # converts piece to string depending on color
    def to_string(self) -> str:
        return "P" if self.piece_color == Color.WHITE else "p"

    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        """
        This function tests whether a Pawn can move from starting to ending coordinates regardless of other pieces
        on the board: Other functionality handles pieces being in the way
        :param is_capture: bool of if the move is trying to capture a piece or not
        :param r1: start row
        :param c1: start column
        :param r2: destination row
        :param c2: destination column
        :return: boolean of whether the Pawn can move to that position
        """

        row_diff = r2 - r1
        col_diff = abs(c2 - c1)

        direct = 1 if self.piece_color == Color.WHITE else -1

        # if pawn is trying to capture then test whether it is moving in the right direction vertically or horizontally
        if is_capture:
            return row_diff == direct and col_diff == 1
        else:
            # if pawn tried to move horizontally then return false
            if col_diff > 0:
                return False
            # return whether pawn can make a move based on if it has previously moved or not
            if not self.has_moved:
                return (row_diff / abs(row_diff)) == direct and abs(row_diff) <= 2
            else:
                return row_diff == direct and abs(row_diff) <= 1


# ==============================================================================#

class Blank(Piece):

    # constructor
    def __init__(self):
        super(Blank, self).__init__()

    # converts blank piece to string
    def to_string(self) -> str:
        return " "

    # can move method doesn't do anything
    def is_possible_move(self, r1: int, c1: int, r2: int, c2: int, is_capture: bool) -> bool:
        pass

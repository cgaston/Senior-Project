from Pieces import Piece, Knight, Blank, Rook, Queen, Pawn, Bishop, King, Color
import numpy
import copy
from enum import IntEnum


class MoveType(IntEnum):
    MOVE_PASSED = 0
    MOVE_FAILED = 1
    CHECKMATE = 2


# The three functions below are helper functions for the init_board method in the ChessBoard class

def first_row(color: Color) -> list:
    return [Rook(color, 0), Knight(color, 1), Bishop(color, 2), Queen(color, 3), King(color, 4),
            Bishop(color, 5), Knight(color, 6), Rook(color, 7)]


def pawns(color: Color) -> list:
    row = []
    for i in range(8):
        row.append(Pawn(color, i + 8))
    return row


def blank_row() -> list:
    row = []
    for r in range(8):
        row.append(Blank())
    return row


# This Class will represent a chess board
class ChessBoard:

    def __init__(self):
        self.board = []
        self.init_board()
        self.coord = []
        self.init_coord()

    def init_board(self):
        self.board = [first_row(Color.WHITE), pawns(Color.WHITE)]
        for i in range(4):
            self.board.append(blank_row())
        self.board += [pawns(Color.BLACK), first_row(Color.BLACK)]

    def init_coord(self):
        white_coord = []
        black_coord = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if r < 2:
                    white_coord.append([r, c])
                if r > 5:
                    black_coord.insert(0, [r, 7 - c])
        self.coord = [white_coord, black_coord]

    def display_board(self):
        """
        displays the chess board with text
        :return: void method
        """

        print("   ", end="")
        columns = "ABCDEFGH"
        for char in columns:
            print("  {} ".format(char), end="")
        print("")

        for r in range(8):
            print("  ", 8 * "+---", end="+\n")
            print("{:2d} ".format(8 - r), end="")
            for c in range(8):
                print("| {} ".format(self.board[7 - r][c].to_string()), end="")
            print("|")
        print("  ", 8 * "+---", end="+\n\n")

    def is_valid_move(self, r1: int, c1: int, r2: int, c2: int, color: Color) -> bool:
        """
        Method has the board determine if the move trying to be made is valid or not
        :param r1: start row
        :param c1: start col
        :param r2: dest row
        :param c2: dest col
        :param color: color of player making the move
        :return: boolean stating whether move was valid or not
        """
        # make sure piece trying to be picked up belongs to player and
        # make sure player is moving piece to available square
        if self.board[r1][c1].piece_color != color or self.board[r2][c2].piece_color == color:
            return False

        is_capture = self.board[r1][c1].opp_color() == self.board[r2][c2].piece_color

        # make sure piece is able to move to space
        if not self.board[r1][c1].is_possible_move(r1, c1, r2, c2, is_capture):
            return False
        if isinstance(self.board[r1][c1], Knight):  # if piece is Knight then move is valid
            return True

        row_diff = r2 - r1
        col_diff = c2 - c1

        # get the signs of the change of direction between start and end coord
        signs = numpy.sign([row_diff, col_diff])

        # this code handles whether castling is a valid move
        if isinstance(self.board[r1][c1], King):
            if row_diff == 0 and abs(col_diff) == 2:
                if castle_possible(self, r1, c1, r2, c2, signs[1], color):
                    rook_coord = self.coord[color][0] if signs[1] == -1 else self.coord[color][7]
                    self.board[r1][c1].can_castle = True
                    return True
                else:
                    return False

        temp_r, temp_c = r1, c1
        # traverse the board starting at the current piece and check for any spots in the path that are not blank
        # if spot is not blank then return false saying the move was illegal
        for i in range(max(abs(row_diff), abs(col_diff)) - 1):
            temp_r += signs[0]
            temp_c += signs[1]
            if not isinstance(self.board[temp_r][temp_c], Blank):
                return False
        else:
            return True

    def move_piece(self, r1: int, c1: int, r2: int, c2: int, color: str = "blank") -> MoveType:
        """
        method that moves the piece on the board
        :param color: string of the color of the piece being moved
        :param r1: start row
        :param c1: start col
        :param r2: dest row
        :param c2: dest col
        :return: enumeration of move type to determine if move passed/failed or if there was checkmate
        """

        is_capture = self.board[r2][c2].piece_color != Color.BLANK
        oppo_col = self.board[r1][c1].opp_color()

        # move piece to desired location on the board
        temp = self.board[r2][c2]
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = Blank()

        self.update_coord([r2, c2], self.board[r2][c2].piece_color)  # make initial update for piece coordinates

        # This code handles moving the rook if king tried to castle
        if isinstance(self.board[r2][c2], King) and self.board[r2][c2].can_castle:
            row_diff = r2 - r1
            col_diff = c2 - c1
            piece_color = self.board[r2][c2].piece_color
            # get the signs of the change of direction between start and end coord
            signs = numpy.sign([row_diff, col_diff])

            rook_coord = self.coord[piece_color][0] if signs[1] == -1 else self.coord[piece_color][7]
            self.board[r2][c2 - signs[1]] = self.board[rook_coord[0]][rook_coord[1]]
            self.board[rook_coord[0]][rook_coord[1]] = Blank()

            self.update_coord([r2, c2 - signs[1]], piece_color)  # make initial update for piece coordinates

        # if moved caused your king to be in check then pieces are put back to where they were before and
        # player will be asked to make a different move
        if self.is_check(self.board[r2][c2].piece_color):
            self.board[r1][c1] = self.board[r2][c2]  # put original piece back where it was
            self.board[r2][c2] = temp  # set destination square to piece that was there before
            self.update_coord([r1, c1], self.board[r1][c1].piece_color)
            if color != "blank":
                print("Can't make that move, your King is in check")
            return MoveType.MOVE_FAILED

        # check if player move caused opponent to be in check
        if self.is_check(oppo_col):
            if self.is_checkmate(oppo_col):
                print("Checkmate!")
                return MoveType.CHECKMATE
            else:
                print("{} King is in check".format(color))

        # update coordinates for piece that is captured if move is completed
        if is_capture:
            self.coord[temp.piece_color][temp.number] = [-1, -1]

        self.board[r2][c2].piece_moved()  # indicate piece has moved

        return MoveType.MOVE_PASSED

    def update_coord(self, dest: list, color: Color):
        """
        update coordinates list if piece has moved
        :param dest: list that contains the coordinates of the updated location
        :param color: color of piece that is being updated
        :return: void
        """
        self.coord[color][self.board[int(dest[0])][int(dest[1])].number] = dest  # ### take a look at this function

    def is_check(self, color: Color) -> bool:
        """
        This method checks to see if a king of the color passed in is in check
        :param color: color
        :return: boolean stating whether the king is in check (True) or not (False)
        """
        king_coord = self.coord[color][4]
        oppo_col = self.board[int(king_coord[0])][int(king_coord[1])].opp_color()

        for i in range(16):
            temp_coord = self.coord[oppo_col][i]
            if temp_coord[0] == -1 and temp_coord[1] == -1:
                continue
            if self.is_valid_move(temp_coord[0], temp_coord[1], king_coord[0], king_coord[1], oppo_col):
                return True
        else:
            return False

    def is_checkmate(self, color: Color) -> bool:
        king_moves = get_king_moves(self, color)  # get a list of possible moves the king can make
        attackers = get_attackers(self, color)  # get a list of the coordinates of any attackers to the king
        
        # run this code only if there is exactly 1 attacker
        if len(attackers) == 1:
            # return false if the attacker can be captured proving king is not in checkmate
            if capture_or_block_attacker(self, color, attackers[0]):
                return False
        # if attackers cannot be captured or blocked and the King has no moves then return True
        if len(king_moves) == 0:
            return True


# ======================================================================#

def castle_possible(b1: ChessBoard, r1: int, c1: int, r2: int, c2: int, direct: int, color: Color) -> bool:
    """
    this function will determine if King can castle
    :param b1: Chessboard
    :param r1: start row
    :param c1: start col
    :param r2: end row
    :param c2: end col
    :param direct: int that gives the direction the King moved -1 (king moved left) or 1 (king moved right)
    :param color: color of king
    :return: boolean stating whether castling is possible
    """
    if b1.is_check(color):
        return False
    rook_coord = b1.coord[color][0] if direct == -1 else b1.coord[color][7]
    if b1.board[rook_coord[0]][rook_coord[1]].has_moved:  # if rook has moved then return false
        return False
    if not b1.is_valid_move(rook_coord[0], rook_coord[1], r2, c2 - direct, color):
        return False

    temp = c1
    temp_board = copy.deepcopy(b1)
    # return false if pieces of different color are in the way
    for i in range(abs(rook_coord[1] - c1) - 1):
        temp += direct
        if temp_board.board[r1][temp].piece_color != Color.BLANK:
            return False
    # return false if there were pieces of the same color in the way
    if temp_board.move_piece(r1, c1, r2, c2) != MoveType.MOVE_PASSED:
        return False
    del temp_board

    # all conditions for castling have been met so return true
    return True


def get_king_moves(board1: ChessBoard, color: Color) -> list:  # add -> list
    """
    This function creates and returns a list of moves that the king of the color passed in can make
    :param board1: chess board
    :param color: color of king whose moves are being checked for
    :return: a list of coordinates for the king to potentially move to
    """
    king_coord = board1.coord[color][4]
    move_list = []
    for r in range(-1, 2):
        if (king_coord[0] + r) < 0 or (king_coord[0] + r) > 7:
            continue
        for c in range(-1, 2):
            if r == 0 and c == 0:
                continue
            if (king_coord[1] + c) < 0 or (king_coord[1] + c) > 7:
                continue
            temp1, temp2, temp3, temp4 = king_coord[0], king_coord[1], king_coord[0] + r, king_coord[1] + c
            if board1.is_valid_move(temp1, temp2, temp3, temp4, color):
                temp_board = copy.deepcopy(board1)  # have temp board be a copy of the board passed in
                move_type = temp_board.move_piece(temp1, temp2, temp3, temp4)
                if move_type == MoveType.MOVE_PASSED:
                    move_list.append(temp_board.coord[color][4])
                del temp_board

    return move_list


def get_attackers(board1: ChessBoard, color: Color) -> list:
    """
    gets a list of attackers to the king of the color passed
    :param board1: chess board
    :param color: color of king that has potential attackers
    :return: list of coordinates for the attackers
    """
    king_coord = board1.coord[color][4]
    oppo_color: Color = 1 - color
    # traverse opposite color pieces and find any attacking the king of the passed in color
    return [piece for piece in board1.coord[oppo_color] if
            board1.is_valid_move(piece[0], piece[1], king_coord[0], king_coord[1], oppo_color)]


def capture_or_block_attacker(board1: ChessBoard, color: Color, attacker: list) -> bool:
    """
    This function determines if any piece of the color in check can capture the attacker
    :param board1: chess board
    :param color: color of player in check
    :param attacker: list that contains the coordinates of the attacker
    :return: boolean stating whether attacker can be captured (True) or not (False)
    """
    king_coord = board1.coord[color][4]
    for piece in board1.coord[color]:
        temp1, temp2, temp3, temp4 = king_coord[0], king_coord[1], attacker[0], attacker[1]
        row_diff = temp3 - temp1
        col_diff = temp4 - temp2

        # get the signs of the change of direction between start and end coord
        signs = numpy.sign([row_diff, col_diff])

        # traverse the board starting at the current piece and check for any spots in the path that are not blank
        # if spot is not blank then return false saying the move was illegal
        for i in range(max(abs(row_diff), abs(col_diff))):
            temp1 += signs[0]
            temp2 += signs[1]
            if board1.is_valid_move(piece[0], piece[1], temp1, temp2, color):
                temp_board = copy.deepcopy(board1)  # have temp board be a copy of the board passed in
                move_type = temp_board.move_piece(piece[0], piece[1], temp1, temp2)
                if move_type == MoveType.MOVE_PASSED:
                    return True
                del temp_board
    return False


b = ChessBoard()
b.display_board()

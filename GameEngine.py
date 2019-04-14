class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Player:
    cross = 0
    circle = 1


class Winner:
    cross = 0
    circle = 1
    draw = 2
    none = 3

    def winner_as_string(self, winner: int):
        if winner == self.cross:
            return 'X'
        elif winner == self.circle:
            return 'O'
        elif winner == self.draw:
            return '-'
        else:
            return '.'


# TODO: Convert to real enums?
class TileValue:
    cross = 0
    circle = 1
    empty = 2
    destroyed = 3

    def value_as_string(self, value: int):
        if value == self.cross:
            return 'X'
        elif value == self.circle:
            return 'O'
        elif value == self.destroyed:
            return '-'
        else:
            return '.'


class Move:
    board_position: Point
    tile_position: Point

    def __init__(self, board_position: Point, tile_position: Point):
        self.board_position = board_position
        self.tile_position = tile_position


class SmallTileInformation:
    board_position: Point
    position: Point
    value: int

    def __init__(self, board_position: Point, position: Point, value: int):
        self.board_position = board_position
        self.position = position
        self.value = value


class SmallBoardInformation:
    position: Point
    value: int
    tiles: [SmallTileInformation]

    def __init__(self, position: Point, value: int, tiles: [SmallTileInformation]):
        self.position = position
        self.value = value
        self.tiles = tiles


class TicTacToeGame:
    moves: [Move]
    board: [SmallBoardInformation]
    current_player: int

    def __init__(self, moves):
        self.moves = []
        self.current_player = Player.cross
        self.board = self.__get_initial_smallboards()

        self.apply_moves(moves)

    def apply_moves(self, moves):
        for move in moves:
            self.apply_move(move)

    def apply_move(self, move):
        self.moves.append(move)

        board_to_change = next(board for board in self.board if board.position == move.board_position)
        tile_to_change = next(tile for tile in board_to_change.tiles if tile.position == move.tile_position)
        tile_to_change.value = self.current_player

        # TODO calculate win result
        # TODO change player

    def print_game(self):
        smallboard_size = 3
        rows = []
        for board in self.board:
            for tile in board.tiles:
                value = TileValue().value_as_string(tile.value)
                row_number = board.position.x * smallboard_size + tile.position.x
                if row_number >= len(rows):
                    rows.append([])
                rows[row_number].append(value)

        row_index = 0
        for row in rows:
            element_index = 0

            for element in row:
                divided_by_size = (element_index + 1) / smallboard_size
                separator = '  ' if divided_by_size > 0 and divided_by_size.is_integer() else ''
                print(element, end=separator)
                element_index += 1

            divided_by_size = (row_index + 1) / smallboard_size
            separator = '\n\n' if divided_by_size > 0 and divided_by_size.is_integer() else '\n'
            print(end=separator)

            row_index += 1

    def __get_initial_smallboards(self):
        smallboards: [SmallBoardInformation] = []
        for x in range(0, 3):
            for y in range(0, 3):
                board_position = Point(x, y)
                tiles = self.__get_initial_tiles_of_smallboard(board_position)
                smallboard = SmallBoardInformation(board_position, TileValue.empty, tiles)
                smallboards.append(smallboard)
        return smallboards

    def __get_initial_tiles_of_smallboard(self, board_position: Point):
        tiles: [SmallTileInformation] = []
        for x in range(0, 3):
            for y in range(0, 3):
                tile = SmallTileInformation(board_position, Point(x, y), TileValue.empty)
                tiles.append(tile)
        return tiles

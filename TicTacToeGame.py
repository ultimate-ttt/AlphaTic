class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Player:
    cross = 0
    circle = 1


class Winner:
    cross = 0
    circle = 1
    draw = 2
    none = 3


class TileValue:
    cross = 0
    circle = 1
    empty = 2
    destroyed = 3


class Move:
    board_position: Point
    tile_position: Point

    def __init__(self, board_position: Point, tile_position: Point):
        self.boardPosition = board_position
        self.tilePosition = tile_position


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

    def applyMove(self, move):
        self.moves.append(move)
        # TODO

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




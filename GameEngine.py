class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return str(self.x) + '/' + str(self.y)


class Player:
    cross = 0
    circle = 1


class Winner:
    cross = 0
    circle = 1
    none = 2
    draw = 3

    def winner_as_string(self, winner: int):
        if winner == self.cross:
            return 'X'
        elif winner == self.circle:
            return 'O'
        elif winner == self.draw:
            return '-'
        else:
            return '.'


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


class TileInformation:
    position: Point
    value: int

    def __init__(self, position: Point, value: int):
        self.position = position
        self.value = value


class SmallTileInformation(TileInformation):
    board_position: Point

    def __init__(self, board_position: Point, position: Point, value: int):
        TileInformation.__init__(self, position, value)
        self.board_position = board_position


class SmallBoardInformation(TileInformation):
    tiles: [SmallTileInformation]

    def __init__(self, position: Point, value: int, tiles: [SmallTileInformation]):
        TileInformation.__init__(self, position, value)
        self.tiles = tiles


class LineWinResult:
    line: str
    won: bool

    def __init__(self, line: str, won: bool):
        self.line = line
        self.won = won


class WinResult:
    finished: bool
    winner: int

    def __init__(self, finished: bool, winner: int):
        self.finished = finished
        self.winner = winner

    def __repr__(self):
        return 'Finished: ' + str(self.finished) + '\nWinner: ' + Winner().winner_as_string(self.winner)


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
        board_to_change = next(board for board in self.board if board.position == move.board_position)
        tile_to_change = next(tile for tile in board_to_change.tiles if tile.position == move.tile_position)
        tile_to_change.value = self.current_player

        win_result = self.__get_winresult_for_board(board_to_change.tiles)
        if win_result.finished:
            board_to_change.value = win_result.winner

        self.moves.append(move)
        self.__change_player()

    def get_winresult(self):
        return self.__get_winresult_for_board(self.board)

    def get_current_active_boards(self):
        if len(self.moves) == 0:
            all_boards: [Point] = []
            for x in range(0, 3):
                for y in range(0, 3):
                    all_boards.append(Point(x, y))
            return all_boards

        if self.get_winresult().finished:
            return []

        last_move = self.moves[-1].tile_position
        active_boards = [last_move]

        pointed_at_board = next(board for board in self.board if board.position == last_move)
        board_finished = pointed_at_board.value != TileValue.empty
        if board_finished:
            all_unfinished_boards = filter(lambda board: board.value == TileValue.empty, self.board)
            active_boards = map(lambda board: board.position, all_unfinished_boards)

        return active_boards

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

    def __change_player(self):
        if self.current_player == Player.cross:
            self.current_player = Player.circle
        else:
            self.current_player = Player.cross

    def __get_winresult_for_board(self, board: [TileInformation]):
        cross_won = self.__get_win_result_for_player(Player.cross, board)
        circle_won = self.__get_win_result_for_player(Player.circle, board)
        draw = all(element.value != TileValue.empty for element in board)

        if cross_won:
            return WinResult(True, Winner.cross)
        elif circle_won:
            return WinResult(True, Winner.circle)
        elif draw:
            return WinResult(True, Winner.draw)
        else:
            return WinResult(False, Winner.none)

    def __get_win_result_for_player(self, player: int, board: [TileInformation]):
        row0 = filter(lambda el: el.position.x == 0, board)
        row1 = filter(lambda el: el.position.x == 1, board)
        row2 = filter(lambda el: el.position.x == 2, board)
        column0 = filter(lambda el: el.position.y == 0, board)
        column1 = filter(lambda el: el.position.y == 1, board)
        column2 = filter(lambda el: el.position.y == 2, board)
        leftslant = filter(lambda el: el.position.x == el.position.y, board)
        rightslant = filter(lambda el: el.position.x + el.position.y == 2, board)

        possible_win_positions = [
            LineWinResult('row0', self.__has_won_line(player, row0)),
            LineWinResult('row1', self.__has_won_line(player, row1)),
            LineWinResult('row2', self.__has_won_line(player, row2)),
            LineWinResult('column0', self.__has_won_line(player, column0)),
            LineWinResult('column1', self.__has_won_line(player, column1)),
            LineWinResult('column2', self.__has_won_line(player, column2)),
            LineWinResult('leftSlant', self.__has_won_line(player, leftslant)),
            LineWinResult('rightSlant', self.__has_won_line(player, rightslant)),
        ]

        for possible_win in possible_win_positions:
            if possible_win.won:
                return True
        return False

    def __has_won_line(self, player: int, row: [TileInformation]):
        return self.__count_in_line(player, row) == 3

    def __count_in_line(self, player: int, row: [TileInformation]):
        return len(list(filter(lambda el: el.value == player, row)))

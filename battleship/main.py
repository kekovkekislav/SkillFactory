from random import *


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы выстрелили за пределы доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"


class Ship:
    def __init__(self, front, length, direct):

        self.length = length
        self.front = front
        self.direct = direct
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.front.x
            dot_y = self.front.y

            if self.direct == 0:
                dot_x += i

            elif self.direct == 1:
                dot_y += i

            ship_dots.append(Dot(dot_x, dot_y))
        return ship_dots

    def hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.hit(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True

        self.field[d.x][d.y] = "•"
        print("Промах!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                position = self.ask()
                again = self.enemy_board.shot(position)
                return again
            except BoardException as er:
                print(er)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход комьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cord = input("Ваш ход: ").split()
            if len(cord) != 2:
                print("Введите две координаты! ")
                continue

            x, y = cord

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player_board = self.make_board()
        ai_board = self.make_board()
        ai_board.hid = True

        self.player = User(player_board, ai_board)
        self.ai = AI(ai_board, player_board)

    def make_board(self):
        board = None
        while board is None:
            board = self.random_board()
        return board

    def random_board(self):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        tries = 0
        for l in ship_lengths:
            while True:
                tries += 1
                if tries > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def greet(self):
        print("------------------------------------")
        print("Добро пожаловать в игру Морской бой!")
        print("------------------------------------")
        print("        Формат ввода: x,y           ")
        print("        x- номер столбца            ")
        print("        y- номер строки             ")
        print("------------------------------------")
        print("ПРИЯТНОЙ ИГРЫ!!!                    ")
        print("------------------------------------")

    def show_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.player.board)
        print("-" * 20)
        print("Доска компьютера:")
        print("-" * 20)
        print(self.ai.board)
        print("-" * 20)

    def loop(self):
        num = 0
        while True:
            self.show_boards()
            if num % 2 == 0:
                print("Ходит пользователь: ")
                again = self.player.move()
            else:
                print("Ходит компьютер: ")
                again = self.ai.move()

            if again:
                num -= 1

            if self.player.board.count == 7:
                print("Игрок победил!")

            if self.ai.board.count == 7:
                print("Победил компьютер!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()




g = Game()
g.start()

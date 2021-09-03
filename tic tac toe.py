board = [["·"] * 3 for i in range(3)]


def hello():
    print("————————————————————")
    print("Добро пожаловать!  ")
    print("Правила ввода: x y")
    print("x- номер строки")
    print("y- номер столбца")
    print("————————————————————")
    print("")
    print("")


def show_board():
    print(f"     0     1     2")
    print(f"————————————————————")
    for i in range(3):
        print(f"{i} |  {board[i][0]}  |  {board[i][1]}  |  {board[i][2]} |")

    print(f"————————————————————")


def turn():
    while True:
        place = input("               Сделайте ход: ").split(" ")
        if len(place) != 2:
            print("                 Введите две координаты!")
            continue

        x, y = place

        if not (x.isdigit()) or not (y.isdigit()):
            print("                 Введите числовые значения!")
            continue

        x = int(x)
        y = int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print("                 Координаты выходят за диапазон допустимых значений!")
            continue

        if board[x][y] != "·":
            print("                 Клетка занята")
            continue

        return x, y


def check():
    for i in range(3):
        win = []

        for j in range(3):
            win.append(board[i][j])
            if win == ["X", "X", "X"]:
                print("Победил крестик")
                return True
            if win == ["0", "0", "0"]:
                print("Победил нолик")
                return True

    for i in range(3):
        win = []

        for j in range(3):
            win.append(board[j][i])
            if win == ["X", "X", "X"]:
                print("Победил крестик")
                return True
            if win == ["0", "0", "0"]:
                print("Победил нолик")
                return True

    win = []
    for i in range(3):
        win.append(board[i][i])
    if win == ["X", "X", "X"]:
        print("Победил крестик")
        return True
    if win == ["0", "0", "0"]:
        print("Победил нолик")
        return True

    for i in range(3):
        win.append(board[i][2 - i])
    if win == ["X", "X", "X"]:
        print("Победил крестик")
        return True
    if win == ["0", "0", "0"]:
        print("Победил нолик")
        return True

    return False


hello()
count = 0
while True:
    count += 1
    show_board()
    if count % 2 == 1:
        print("        Ходит крестик: ")
    else:
        print("        Ходит нолик: ")

    x, y = turn()

    if count % 2 == 1:
        board[x][y] = "X"
    else:
        board[x][y] = "0"

    if check():
        show_board()
        break

    if count == 9:
        print("Ничья")
        break

check()

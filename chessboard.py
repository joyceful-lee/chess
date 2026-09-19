import turtle

LIGHT_SQUARE = "tan"
DARK_SQUARE = "brown"


def board(size):
    turtle.speed(0)
    headers = "abcdefgh"
    square_size = size / 8
    left = -size / 2
    top = size / 2

    turtle.penup()
    turtle.goto(left + square_size / 2, top)
    for header in headers:
        turtle.write(header, align="center", font=("Arial", 12, "normal"))
        turtle.forward(square_size)

    turtle.goto(left, top)
    turtle.backward(10)
    turtle.setheading(270)
    turtle.forward(square_size / 2)
    for rank in range(8, 0, -1):
        turtle.write(str(rank), align="center", font=("Arial", 12, "normal"))
        turtle.forward(square_size)

    turtle.setheading(0)
    turtle.penup()
    turtle.goto(left, top)
    turtle.pendown()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    board_fill(size)

def board_fill(size):
    square_size = size / 8
    left = -size / 2
    top = size / 2

    for row in range(8):
        for column in range(8):
            turtle.penup()
            turtle.goto(left + column * square_size, top - row * square_size)
            turtle.setheading(0)
            turtle.pendown()
            color = LIGHT_SQUARE if (row + column) % 2 == 0 else DARK_SQUARE
            turtle.color(color)
            turtle.begin_fill()
            for _ in range(4):
                turtle.forward(square_size)
                turtle.right(90)
            turtle.end_fill()
    turtle.penup()

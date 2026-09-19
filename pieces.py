import turtle
board_size = 480

LIGHT_SQUARE = "tan"
DARK_SQUARE = "brown"

def set_board_size(size):
    global board_size
    board_size = size

def clear_square(location):
    location_reader(location)
    turtle.penup()

def location_reader(location):
    turtle.setheading(0)
    header = 'abcdefgh'
    column = header.index(location[0].lower())
    row = int(location[1])
    x = (int(board_size/2)*-1) + (column * (board_size/8))
    y = int(board_size/2) - ((8-row) * (board_size/8))
    turtle.penup()
    turtle.goto(x, y)
    turtle.color(check_color(location))
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(board_size/8)
        turtle.right(90)
    turtle.end_fill()
    turtle.goto(x+(board_size/16), y-(board_size/16))
    turtle.pendown()

def check_color(location):
    header = 'abcdefgh'
    column = header.index(location[0].lower())+1
    row = int(location[1])

    if (column + row) % 2 == 0:
        return DARK_SQUARE
    else:
        return LIGHT_SQUARE

def draw_pawn(color, location):
    location_reader(location)
    turtle.color(color)
    turtle.dot(20)

def draw_rook(color, location):
    location_reader(location)
    turtle.color(color)
    turtle.penup()
    turtle.setheading(90)
    turtle.forward(10)
    turtle.pendown()
    turtle.setheading(0)
    # body
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(15)
        turtle.right(90)
        turtle.forward(25)
        turtle.right(90)
        turtle.forward(15)
    turtle.end_fill()
    # top
    turtle.backward(14)
    for i in range(3):
        turtle.begin_fill()
        for j in range(4):
            turtle.forward(6)
            turtle.left(90)
        turtle.end_fill()
        if i == 2:
            continue
        turtle.forward(11)

def draw_knight(color, location):
    location_reader(location)
    turtle.color(color)

    turtle.penup()
    turtle.right(90)
    turtle.forward(15)
    turtle.setheading(0)
    turtle.pendown()

    turtle.begin_fill()
    turtle.forward(10)
    turtle.left(120)
    turtle.forward(20)
    eye_position = (turtle.xcor(), turtle.ycor() + 4)
    turtle.left(120)
    turtle.forward(20)
    turtle.left(120)
    turtle.forward(10)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(*eye_position)
    turtle.pendown()
    turtle.begin_fill()
    turtle.circle(4)
    turtle.end_fill()

def draw_bishop(color, location):
    location_reader(location)
    turtle.color(color)

    turtle.penup()
    turtle.setheading(90)
    turtle.forward(5)
    turtle.setheading(0)

    turtle.begin_fill()
    turtle.circle(6)
    turtle.end_fill()

    turtle.penup()
    turtle.forward(20)
    turtle.right(90)
    turtle.forward(20)
    turtle.setheading(90)
    turtle.pendown()

    turtle.begin_fill()
    turtle.circle(20, 180)
    turtle.end_fill()

def draw_royalty(color, location, queen):
    location_reader(location)
    turtle.color(color)

    dots = []

    turtle.penup()
    turtle.setheading(270)
    turtle.forward(15)
    turtle.setheading(0)
    turtle.pendown()

    turtle.begin_fill()
    turtle.forward(10)
    turtle.left(117)
    turtle.forward(22)
    dots.append([turtle.xcor(), turtle.ycor()+ 6])
    turtle.left(126)
    turtle.forward(22)
    turtle.setheading(0)
    turtle.forward(10)
    turtle.end_fill()

    turtle.forward(10)
    turtle.begin_fill()
    turtle.left(60)
    turtle.forward(10)
    dots.append([turtle.xcor()+3, turtle.ycor()+4])
    turtle.right(40)
    turtle.backward(15)
    turtle.end_fill()

    turtle.forward(15)
    turtle.left(40)
    turtle.backward(10)
    turtle.right(60)
    turtle.backward(20)

    turtle.setheading(180)
    turtle.begin_fill()
    turtle.right(60)
    turtle.forward(10)
    dots.append([turtle.xcor()-3, turtle.ycor()+4])
    turtle.left(40)
    turtle.backward(15)
    turtle.end_fill()

    if queen:
        for dot_x, dot_y in dots:
            turtle.penup()
            turtle.goto(dot_x, dot_y)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(1)
            turtle.end_fill()
    else:
        turtle.penup()
        turtle.goto(dots[0][0], dots[0][1])
        turtle.pendown()
        turtle.setheading(90)
        turtle.backward(2)
        turtle.forward(7)
        turtle.backward(2)
        turtle.right(90)
        turtle.forward(2)
        turtle.backward(5)
    turtle.penup()

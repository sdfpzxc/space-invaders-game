import turtle
import os
import math
import random

# Устанавливаем рабочую директорию в папку со скриптом
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Наш экран
wn = turtle.Screen()
wn.bgcolor('black')
wn.title("zip zap zop oh no aliens")

# Проверяем существование файлов перед загрузкой
try:
    wn.bgpic("cosmic_bg.gif")
except turtle.TurtleGraphicsError:
    print("Предупреждение: Файл cosmic_bg.gif не найден, используем черный фон")

try:
    wn.register_shape("enemy.gif")
    wn.register_shape("hero.gif")
    wn.register_shape("ball.gif")
except turtle.TurtleGraphicsError as e:
    print(f"Предупреждение: Не удалось загрузить изображения: {e}")
    print("Используем стандартные формы")

# Граница
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Счет
score = 0

# Рисуем счет
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 270)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "bold"))
score_pen.hideturtle()

# Игрок
player = turtle.Turtle()
player.color("blue")
try:
    player.shape("hero.gif")
except:
    player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -200)
player.setheading(90)

playerspeed = 15

# Количество врагов
number_of_enemies = 5
enemies = []

# Добавляем врагов
for i in range(number_of_enemies):
    enemy = turtle.Turtle()
    enemy.color("red")
    try:
        enemy.shape("enemy.gif")
    except:
        enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 210)
    y = random.randint(100, 270)
    enemy.setposition(x, y)
    enemies.append(enemy)

enemyspeed = 2

# Пуля игрока
bullet = turtle.Turtle()
bullet.color("yellow")
try:
    bullet.shape("ball.gif")
except:
    bullet.shape("circle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

# Состояние пули
bulletstate = "ready"

# Движение влево и вправо
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -270:
        x = -270
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 270:
        x = 270
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y + 10)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    return False

# Привязка клавиш
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Флаг для завершения игры
game_over = False

# Главный игровой цикл
while not game_over:
    for enemy in enemies:
        # Движение врага
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Движение врага вниз и смена направления
        if enemy.xcor() > 270:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        if enemy.xcor() < -270:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        # Проверка столкновения пули и врага
        if isCollision(bullet, enemy):
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            x = random.randint(-200, 210)
            y = random.randint(100, 270)
            enemy.setposition(x, y)
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "bold"))

        # Проверка столкновения игрока и врага
        if isCollision(player, enemy):
            player.hideturtle()
            print("Game Over")
            game_over = True
            break  # Выходим из цикла по врагам

    if game_over:
        break  # Выходим из главного цикла

    # Движение пули
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Проверка, ушла ли пуля наверх
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

# Выводим финальный счет
score_pen.clear()
score_pen.goto(0, 0)
score_pen.write(f"GAME OVER! Final Score: {score}", False, align="center", font=("Arial", 24, "bold"))

turtle.done()  # Чтобы окно не закрылось сразу
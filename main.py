import os
import turtle
import random
import time

window = turtle.Screen()
window.setup(1000 + 3, 599 + 3)
window.screensize(1000, 599)


PLAYER_X, PLAYER_Y = -335, -50
ENEMY_X, ENEMY_Y = 510, -200
GROUND_Y = -200
BASE_X = -360


class Arrow:
    def __init__(self, x1, y1, x2, y2, color):
        arrow = turtle.Turtle(visible=False)
        arrow.turtlesize(0.25, 3, 2)
        arrow.speed(0)
        arrow.color(color)
        arrow.penup()
        arrow.setpos(x=x1, y=y1)
        heading = arrow.towards(x2, y2)
        arrow.setheading(heading)
        arrow.showturtle()
        self.arrow = arrow
        self.state = 'launched'

    def fly(self):
        if self.state == 'launched':
            self.arrow.forward(8)
            if (self.arrow.ycor() < GROUND_Y or self.arrow.ycor() > 300
                    or self.arrow.xcor() < -500 or self.arrow.xcor() > 500):
                self.state = 'dead'
                self.arrow.hideturtle()

    def distance(self, x, y):
        return self.arrow.distance(x=x, y=y)

    def hideturtle(self):
        self.arrow.hideturtle()

    @property
    def x(self):
        return self.arrow.xcor()

    @property
    def y(self):
        return self.arrow.ycor()


class Enemy:
    def __init__(self, gif, x, y):
        self.time_dead = 7
        enemy = turtle.Turtle(visible=False)
        enemy.speed(0)
        enemy.penup()
        enemy.setpos(x=x, y=y)
        enemy.setheading(180)
        pic_path = os.path.join("images", gif)
        window.register_shape(pic_path)
        enemy.shape(pic_path)
        enemy.showturtle()
        self.enemy = enemy
        self.state = 'launched'

    def step(self):
        if self.state == 'launched':
            self.step_launched()
        elif self.state == 'bum':
            self.time_dead -= 1
            if self.time_dead == 4:
                pic_path = os.path.join("images", "distroy.gif")
                window.register_shape(pic_path)
                self.enemy.shape(pic_path)
            if self.time_dead == 0:
                self.state = 'dead'
                self.hideturtle()

    def step_launched(self):
        self.enemy.forward(6)

    def position(self):
        pass

    def hideturtle(self):
        self.enemy.hideturtle()

    def distance(self, x, y):
        return self.enemy.distance(x=x, y=y)

    @property
    def x(self):
        return self.enemy.xcor()

    @property
    def y(self):
        return self.enemy.ycor()


class Up_enemy(Enemy):
    def step_launched(self):
        self.enemy.left(0.3)
        self.enemy.forward(6)


class Archer(Enemy):
    def step(self):
        if self.state == 'launched':
            self.enemy.forward(4)
            if self.enemy.xcor() < BASE_X + 300:
                self.state = 'fire'
        elif self.state == 'fire':
            if random.randint(1, 100) == 1:
                info = Arrow(x1=self.x - 20, y1=self.y, x2=BASE_X, y2=GROUND_Y + 60, color="purple")
                arrows.append(info)
        elif self.state == 'bum':
            self.time_dead -= 1
            if self.time_dead == 4:
                pic_path = os.path.join("images", "distroy.gif")
                window.register_shape(pic_path)
                self.enemy.shape(pic_path)
            if self.time_dead == 0:
                self.state = 'dead'
                self.hideturtle()


class Object:
    def __init__(self, x, y, name_img):
        object = turtle.Turtle(visible=False)
        object.speed(0)
        object.penup()
        object.setpos(x=x, y=y)
        pic_path = os.path.join("images", name_img)
        window.register_shape(pic_path)
        object.shape(pic_path)
        object.showturtle()
        self.object = object

    def hideturtle(self):
        self.object.hideturtle()


def fire_prayer(x, y):
    global start, press_start
    if not start:
        press_start.hideturtle()
        start = True
    else:
        info = Arrow(x1=PLAYER_X, y1=PLAYER_Y, x2=x, y2=y, color="green")
        arrows.append(info)


def move_arrows(arrows):
    for arrow in arrows:
        arrow.fly()

    dead_arrows = [arrow for arrow in arrows if arrow.state == 'dead']
    for dead in dead_arrows:
        arrows.remove(dead)


def create_and_move_enemies(enemies):
    global spawn
    global count
    if start:
        if count > 0 and spawn == 0:
            rand = random.random()
            if rand > 0.66:
                enemies.append(Archer(gif="archer.gif", x=480, y=-180))
            elif rand > 0.33:
                enemies.append(Enemy(gif="enemy.gif", x=480, y=-180))
            else:
                enemies.append(Up_enemy(gif="enemy.gif", x=480, y=200))
            spawn += random.randint(30, 100)
            count -= 1
        if spawn != 0:
            spawn -= 1
        for enemy in enemies:
            enemy.step()
        dead_enemies = [enemy for enemy in enemies if enemy.state == 'dead']
        for dead in dead_enemies:
            enemies.remove(dead)


def check_shot():
    global score
    for arrow in arrows:
        if arrow.state != 'launched':
            continue
        for enemy in enemies:
            if enemy.distance(arrow.x, arrow.y) < 25:
                arrow.state = 'dead'
                arrow.hideturtle()
                enemy.state = 'bum'
                score += 1


def check_attack():
    global base_health
    for enemy in enemies:
        if enemy.distance(BASE_X, GROUND_Y) < 25 and enemy.state == "launched":
            base_health -= 100
            enemy.state = 'bum'
    for arrow in arrows:
        if arrow.distance(BASE_X-5, GROUND_Y+50) < 20:
            base_health -= 50
            arrow.state = 'dead'
            arrow.hideturtle()


def health_line_update():
    width = base_health / 150
    if width < 1:
        base_health_line.hideturtle()
    else:
        base_health_line.turtlesize(width, 1)


def score_bar_update():
    global tmp_score
    if tmp_score != score:
        tmp_score = score
        label.clear()
        label.write(score, align="center", font=("Arial", 20, "bold"))


def check_game_over():
    if base_health < 1:
        window.clear()
        window.bgpic("images/game_over.png")
        label.setpos(x=0, y=150)
        label.write(score, align="center", font=("Arial", 40, "bold"))
        return True
    return False


def win():
     global start
     start = False
     base.hideturtle()
     score_bar.hideturtle()
     label.clear()
     base_health_line.hideturtle()
     for arrow in arrows:
         arrow.state = "dead"
         arrow.hideturtle()
     for i in range(1,10):
         win = Object(x=0, y=0, name_img="win_"+str(i)+".gif")
         time.sleep(0.04)
         win2 = Object(x=0, y=0, name_img="win_"+str(i+1)+".gif")
         win.hideturtle()
         win2.hideturtle()
     time.sleep(0.5)
     window.clear()
     window.bgpic("images/win_bg.png")
     label.setpos(x=0, y=-150)
     label.write(score, align="center", font=("Arial", 40, "bold"))

def game():
    global base, score_bar, base_health, label, base_health_line, enemies, arrows, start, count, spawn, score, tmp_score, press_start
    start = False
    count = 100
    spawn = 0
    score = 0
    tmp_score = 0
    window.tracer(n=2)
    window.bgpic("images/bgimage.png")
    window.onclick(fire_prayer)
    arrows = []
    enemies = []

    base = Object(x=BASE_X - 50, y=GROUND_Y / 2, name_img="Rocket.gif")
    score_bar = Object(x=375, y=250, name_img="score.gif")

    press_start = turtle.Turtle()
    pic_path = os.path.join("images", "press_to_start.gif")
    window.register_shape(pic_path)
    press_start.shape(pic_path)

    base_health = 2000

    base_health_line = turtle.Turtle(visible=False)
    base_health_line.color("red")
    base_health_line.speed(0)
    base_health_line.setheading(-90)
    base_health_line.turtlesize(10, 1)
    base_health_line.penup()
    base_health_line.setpos(x=BASE_X - 50, y=GROUND_Y / 2 + 200)
    base_health_line.showturtle()

    label = turtle.Turtle(visible=False)
    label.color("white")
    label.speed(0)
    label.penup()
    label.setpos(x=375, y=233)
    label.write(score, align="center", font=("Arial", 20, "bold"))

    while True:
        window.update()
        health_line_update()
        score_bar_update()
        if check_game_over():
            break
        if count <= 0 and len(enemies) == 0:
            time.sleep(1)
            win()
            break
        check_shot()
        check_attack()

        create_and_move_enemies(enemies=enemies)
        move_arrows(arrows=arrows)
        time.sleep(0.010)


while True:
    game()
    strng = window.textinput("Continue?", "If yes then write yes:")
    if strng is None or strng.lower() not in ("yes", "ye", "y", "yep") :
        break
    window.clear()

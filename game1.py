# nativ, ido.s and richard

import turtle
import random
import math
import time

#####################
### PHOTO SETTING ###
#####################

BACK_PIC = 'back.gif'
BACK2_PIC = 'back4.gif'
BACK3_PIC = 'back3.gif'
BACK4_PIC = 'back5.gif'
SALSELA_PIC = 'salsela.gif'
APPLE_PIC = 'apple1.gif'

########################
### GLOBAL VARIABLES ###
########################

_HP = 100
_Score = 0
_Speed = 100
_Basket_Speed = 500
_Level = 0
_Score = 0
N = 5
_Highestscore = 0

_Current_xposa = []
_Current_yposa = []
_Target_yposa = []

_Current_xposb = 0
_Current_yposb = 0
_Target_xposb = 0
_EndScreenShowing = False

x = 0
y = 0

FPS = 30  # constant: refresh about 30 times per second
TIMER_VALUE = 1000 // FPS  # the timer value in milliseconds for timer events

_Should_draw = False
_Apples = []  # list of apples turtles

_Basket = turtle.Turtle()

#################
### FUNCTIONS ###
#################

def initialize_score():
  global _Speed, _HP, _Score, _Basket_Speed , _Level
  _HP = 100
  _Score = 0
  _Speed = 100
  _Basket_Speed = 500
  _Level = 0


def initialze_basket():
    global _Basket, _Current_xposb, _Current_yposb, _Target_xposb, _Target_yposb

    _Basket = turtle.Turtle(shape=SALSELA_PIC)
    _Basket.penup()
    _Basket.speed(_Basket_Speed)
    _Basket.goto(0, -250)
    _Basket.speed(0)
    _Basket.showturtle()


    _Current_xposb = 0  # Let them go anywhere on screen
    _Current_yposb = -250
    _Target_xposb = 0


def initialze_apples():
    global _Apples, _Current_xposa, _Current_yposa, _Target_yposa, _Target_xposa, x, y
    for i in range(N):
        t = turtle.Turtle(shape=APPLE_PIC)
        t.penup()
        t.hideturtle()
        _Apples.append(t)  # Add a turtle to the apples turtle list
        x = random.randint(-350, 450)
        y = random.randint(150, 300)
        _Current_xposa.append(x)  # Let them go anywhere on screen
        _Current_yposa.append(y)
        _Target_yposa.append(y)


def initialize():
    #print ("initializing")
    myScreen.bgpic(BACK_PIC)
    initialize_score()
    initialze_basket()
    initialze_apples()


def restart_initialize():
    myScreen.bgpic(BACK_PIC)
    initialize_score()
    for i in range(N):
        x = random.randint(-350, 450)
        y = random.randint(150, 300)
        _Current_xposa[i] = x  # Let them go anywhere on screen
        _Current_yposa[i] = y
        _Target_yposa[i] = y

    _Current_xposb = 0  # Let them go anywhere on screen
    _Current_yposb = -250
    _Target_xposb = 0


def setNextLevel():
    global _Level, _Speed, _Score

    _Level = _Score // 10 // 15

    _Speed = _Level // 3 * 100 + 100
    if _Speed > 900:
        _Speed = 900
    #("speed=", _Speed, "Level=", _Level, "Score=", _Score)


def update_apples():
    global _Apples, _Current_yposa, x, y, _Current_xposa, _Score, _Highestscore, _HP
    for i in range(N):
        x = random.randint(-350, 450)
        y = random.randint(150, 300)
        if abs(_Current_xposa[i] - _Current_xposb) < 70 and abs(_Current_yposa[i] - _Current_yposb) < 20:
            _Current_xposa[i] = x
            _Current_yposa[i] = y
            _Score = _Score + 10
            # print(_Score)
            if _Score >= _Highestscore:
                _Highestscore = _Score
            setNextLevel()
        elif _Current_yposa[i] <= -280:
            _HP = _HP - 1
            #print(_Speed)
            # print(_HP)
            _Current_xposa[i] = x
            _Current_yposa[i] = y
        else:
            # print("y=", _Current_yposa[i], "speed=", _Speed)
            _Current_yposa[i] -= _Speed / FPS


def update_basket():
    global _Basket, _Current_xposb

    if _Current_xposb > _Target_xposb:
        _Current_xposb -= _Basket_Speed / FPS
        if _Current_xposb < _Target_xposb:
            _Current_xposb = _Target_xposb
    elif _Current_xposb < _Target_xposb:
        _Current_xposb += _Basket_Speed / FPS
        if _Current_xposb > _Target_xposb:
            _Current_xposb = _Target_xposb


def update_states():
    #print("checking update state")
    #print(_EndScreenShowing)
    if _EndScreenShowing:
        return
    #print("Updating state")

    global _Should_draw
    update_apples()
    update_basket()

    _Should_draw = True

    myScreen.ontimer(update_states, TIMER_VALUE)


def draw():
    global _Apples, _Should_draw, _Current_xposa, _Current_yposa, _Basket
    if _Should_draw == False:  # There is no change. Don't draw and return immediately
        return

    #print("drawing")

    for i in range(N):
        xa = _Current_xposa[i]
        ya = _Current_yposa[i]
        _Apples[i].goto(xa, ya)
        _Apples[i].showturtle()

    xb = _Current_xposb
    yb = _Current_yposb
    _Basket.goto(xb, yb)
    _Basket.showturtle()

    # for i in range(N):
    # fireflies[i].clear()  # clear the current drawing
    # color = colorsys.hsv_to_rgb(H_YELLOWGREEN, 1, v[i])  # use colorsys to convert HSV to RGB color
    # fireflies[i].color(color)
    # fireflies[i].goto(current_xpos[i], current_ypos[i])
    # fireflies[i].dot(50)
    _Should_draw = False  # just finished drawing, set should_draw to False


def showLevel():
    global _Level
    lvlTurtle.clear()
    lvlTurtle.penup()
    lvlTurtle.goto(-420, 250)
    lvlTurtle.write("level:", False, "left", ("arial", 20, "normal"))
    lvlTurtle.goto(-343.75, 250)
    lvlTurtle.write(_Level, False, "left", ("arial", 20, "bold"))


def showScore():
    global _Score
    scrTurtle.clear()
    scrTurtle.penup()
    scrTurtle.goto(-420, 220)
    scrTurtle.write("score:", False, "left", ("arial", 20, "normal"))
    scrTurtle.goto(-343.75, 217)
    scrTurtle.write(_Score, False, "left", ("arial", 20, "bold"))


def showRecord():
    global _Highestscore
    hscrTurtle.clear()
    hscrTurtle.penup()
    hscrTurtle.goto(-420, 190)
    hscrTurtle.write("highest score:", False, "left", ("arial", 20, "normal"))
    hscrTurtle.goto(-243.75, 187)
    hscrTurtle.write(_Highestscore, False, "left", ("arial", 20, "bold"))


def showHP():
    global _HP
    HPTurtle.clear()
    HPTurtle.penup()
    HPTurtle.goto(-420, 155)
    HPTurtle.write("lifes:", False, "left", ("arial", 20, "normal"))
    HPTurtle.goto(-355.75, 152)
    HPTurtle.write(_HP, False, "left", ("arial", 20, "bold"))


def endscreen():
    global _EndScreenShowing, _Apples, _Basket, _Current_xposb
    if _EndScreenShowing:
        return
    _EndScreenShowing = True
    for i in range(N):
        _Apples[i].hideturtle()
    _Basket.hideturtle()
    myScreen.bgpic(BACK2_PIC)
    scrTurtle.pencolor("white")
    hscrTurtle.pencolor("white")
    lvlTurtle.pencolor("white")
    HPTurtle.pencolor("white")
    showScore()
    showLevel()
    showRecord()
    myScreen.update()
    myScreen.onkeypress(on_restart, "space")


def right():
    global _Target_xposb

    if _Target_xposb <= _Current_xposb:
        _Target_xposb = _Target_xposb + 20
    if _Target_xposb > 450:
        _Target_xposb = 450


def left():
    global _Target_xposb
    if _Target_xposb >= _Current_xposb:
        _Target_xposb = _Target_xposb - 20
    if _Target_xposb < -450:
        _Target_xposb = -450


def run():
    while 0 == 0:
        if _HP > 0:
            scrTurtle.pencolor("black")
            hscrTurtle.pencolor("black")
            lvlTurtle.pencolor("black")
            HPTurtle.pencolor("black")
            showLevel()
            showScore()
            showRecord()
            showHP()

            # while True:
            draw()  # draw forever
            myScreen.update()
        else:
            endscreen()
            myScreen.bgpic(BACK4_PIC)
            return


def on_restart():
    global _EndScreenShowing
    #print("restarting")
    myScreen.onkeypress(None, "space")
    _EndScreenShowing = False
    restart_initialize()
    update_states()
    run()



#################
### MAIN CODE ###
#################

myScreen = turtle.Screen()
myScreen.setup(width=900, height=600)
myScreen.title("catch the apples")
myScreen.tracer(0, 0)

myScreen.addshape(SALSELA_PIC)
myScreen.addshape(APPLE_PIC)

lvlTurtle = turtle.Turtle()
scrTurtle = turtle.Turtle()
hscrTurtle = turtle.Turtle()
HPTurtle = turtle.Turtle()



myScreen.listen()
myScreen.onkeypress(right, "Right")
myScreen.onkeypress(left, "Left")
# myScreen.exitonclick()
# myScreen.onclick(on_screen_click, 1)

initialize()
update_states()
run()

myScreen.onkeypress(on_restart, "space")
myScreen.listen()
myScreen.mainloop()
# כדי שיהיה 350 שורות
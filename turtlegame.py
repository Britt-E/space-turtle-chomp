# Turtle Graphics Game – Space Turtle Chomp
import turtle
import math
import random
import winsound
import time

# Set up screen
turtle.setup(800,800)
wn = turtle.Screen()
wn.bgcolor('black')
wn.bgpic('kbgame-bg.gif')
wn.tracer(3)

# Draw border
mypen = turtle.Turtle()
mypen.color("white")
mypen.penup()
mypen.setposition(-300,-300)
mypen.pendown()
mypen.pensize(3)
for side in range(4):
    mypen.forward(600)
    mypen.left(90)
mypen.hideturtle()

# Create player turtle
player = turtle.Turtle()
player.color('darkorange')
player.shape('turtle')
player.penup()
player.speed(0)

# Create opponent turtle
comp = turtle.Turtle()
comp.color('red')
comp.shape('turtle')
comp.penup()
comp.setposition(random.randint(-290, 290), random.randint(-290, 290))

# Create competition score
mypen2 = turtle.Turtle()
mypen2.color('red')
mypen2.hideturtle()

# Create variable score
score = 0
compscore = 0

# Create food
maxFoods = 10
foods = []

for count in range(maxFoods):
    new_food = turtle.Turtle()
    new_food.color("lightgreen")
    new_food.shape("circle")
    new_food.shapesize(.5)
    new_food.penup()
    new_food.speed(0)
    new_food.setposition(random.randint(-290, 290), random.randint(-290, 290))
    foods.append(new_food)

# Set speed variable
speed = 1
max_speed = 6  

# Create timer display turtle
timer_turtle = turtle.Turtle()
timer_turtle.color('white')
timer_turtle.hideturtle()
timer_turtle.penup()
timer_turtle.setposition(0, 310)  

# Set game time limit for 1 minute (60 seconds)
timeout = time.time() + 60  

# Sound cooldown tracking
sound_cooldown = {"bounce": 0, "chomp": 0}
cooldown_time = 0.5  

# Define functions
def turn_left():
    player.left(30)

def turn_right():
    player.right(30)

def increase_speed():
    global speed
    if speed < max_speed:  
        speed += 1

def isCollision(t1, t2):
       d = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()-t2.ycor(),2))
       if d < 20:
           return True
       else:
           return False
       
def play_sound(sound):
    current_time = time.time()
    if current_time - sound_cooldown[sound] > cooldown_time:
        winsound.PlaySound(f"{sound}.wav", winsound.SND_ASYNC)
        sound_cooldown[sound] = current_time

# Set keyboard binding
turtle.listen()
turtle.onkey(turn_left, 'Left')
turtle.onkey(turn_right, 'Right')
turtle.onkey(increase_speed, 'Up')

start_time = time.time()
last_displayed_time = 60  

while True:
    elapsed_time = time.time() - start_time  
    remaining_time = int(60 - elapsed_time)  

    if remaining_time != last_displayed_time:
        timer_turtle.clear()  
        timer_turtle.write(f"Time Left: {remaining_time}", align="center", font=("Arial", 14, "normal"))  # Display remaining time
        last_displayed_time = remaining_time 

    if elapsed_time >= 60:  
        break

    player.forward(speed)
    comp.forward(6)

    # Boundary Player Checking x coordinate
    if player.xcor() > 290 or player.xcor() < -290:
        player.right(180)
        # Reset position slightly away from the boundary
        if player.xcor() > 290:
            player.setx(290)
        elif player.xcor() < -290:
            player.setx(-290)
        play_sound("bounce")

    # Boundary Player Checking y coordinate
    if player.ycor() > 290 or player.ycor() < -290:
        player.right(180)
        # Reset position slightly away from the boundary
        if player.ycor() > 290:
            player.sety(290)
        elif player.ycor() < -290:
            player.sety(-290)
        play_sound("bounce")

    # Check if the player is stuck in the corner (both x and y boundaries)
    if (player.xcor() > 290 and player.ycor() > 290) or (player.xcor() < -290 and player.ycor() > 290) or (player.xcor() > 290 and player.ycor() < -290) or (player.xcor() < -290 and player.ycor() < -290):
        player.setx(player.xcor() - 10)  
        player.sety(player.ycor() - 10)  
        player.right(180)  
        play_sound("bounce")

    # Check if the opponent is stuck in the corner (both x and y boundaries)
    if (comp.xcor() > 280 and comp.ycor() > 280) or (comp.xcor() < -280 and comp.ycor() > 280) or (comp.xcor() > 280 and comp.ycor() < -280) or (comp.xcor() < -280 and comp.ycor() < -280):
        comp.setx(comp.xcor() - 10)  
        comp.sety(comp.ycor() - 10)  
        comp.right(180)  
        play_sound("bounce")

    #Boundary Comp Checking x coordinate
    if comp.xcor() > 280 or comp.xcor() <-280:
        # If near boundary, move them back into bounds
        if comp.xcor() > 280:
            comp.setx(280)
        if comp.xcor() < -280:
            comp.setx(-280)
        # Change direction slightly
        comp.right(random.randint(30, 155))
        play_sound("bounce")

    #Boundary Comp Checking y coordinate
    if comp.ycor() > 280 or comp.ycor() <-280:
    # If near boundary, move them back into bounds
        if comp.ycor() > 280:
            comp.sety(280)
        if comp.ycor() < -280:
            comp.sety(-280)
        # Change direction slightly
        comp.right(random.randint(30, 155))
        play_sound("bounce")

    # Move food around
    for food in foods:
        food.forward(3)

        # Boundary Food Checking x coordinate
        if food.xcor() > 290 or food.xcor() <- 290:
            food.right(180)
            play_sound("bounce")

        # Boundary Food Checking y coordinate
        if food.ycor() > 290 or food.ycor() <- 290:
            food.right(180)
            play_sound("bounce")
        
        # Player Collision checking
        if isCollision(player, food):
            food.setposition(random.randint(-290, 290), random.randint(-290, 290))
            food.right(random.randint(0, 360))
            play_sound("chomp")
            score +=1
            # Draw the score on the screen
            mypen.undo()
            mypen.penup()
            mypen.hideturtle()
            mypen.setposition(-290, 310)
            scorestring ="Score: %s" % score
            mypen.write(scorestring, False, align='left', font=('Arial', 14, 'normal'))

        # Comp Collision checking
        if isCollision(comp, food):
           food.setposition(random.randint(-290, 290), random.randint(-290, 290))
           food.right(random.randint(0,360))
           play_sound("chomp")
           compscore+=1
           #Draw the Comp score on the screen
           mypen2.undo()
           mypen2.penup()
           mypen2.hideturtle()
           mypen2.setposition(200, 310)
           scorestring ="Score: %s" %compscore
           mypen2.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

if (int(score) > int(compscore)):
    mypen.setposition(0, 0)
    mypen.color("yellow")
    mypen.write("Game Over: You WIN", False, align="center", font=("Arial", 28, "normal"))
else:
    mypen.setposition(0, 0)
    mypen.color("yellow")
    mypen.write("Game Over: You LOSE", False, align="center", font=("Arial", 28, "normal"))

delay = input("Press Enter to finish.")    


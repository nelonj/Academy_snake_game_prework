import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

#Set up screen
cell_size = 20
cell_number = 40 #creating grid
SCREEN_SIZE = cell_number * cell_size
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) #creates screen parameters (width, height)

#Colours (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
pink = (255, 192, 203)
green = (0, 100, 0)

#Set up display style
pygame.display.set_caption('Snake game by HBB & ONJ')
font_style = pygame.font.SysFont("Comic Sans MS", 30) #Creates font name and size

#VARIABLES
running = True #For while loop
score = 0 #Keeping track of the score
round = 1 #Keeping track of rounds (game starts new round each time you die)
clock = pygame.time.Clock() #Controls snake speed

# Variables for snake setup
x1 = SCREEN_SIZE / 2 #Starting point of snake (middle of screen)
y1 = SCREEN_SIZE / 2
x1_change = 0 #Changes as snake moves
y1_change = 0

snake_length = 1 #Snake starts as single block and increases as eats food
snake_coordinates = [] #Empty list (updated with snake coordinates as snake moves)
snake_speed = 8 #Sets snake speed

#Food setup
x2 = random.randrange(cell_size, SCREEN_SIZE, cell_size) #randomly generates food position - (start, stop, step)
y2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)

#Define function for score message - creating a surface - blit (overlap) new surface on screen
def score_message(msg_score, color):
    font = font_style.render(msg_score + str(score), True, color)
    screen.blit(font, [SCREEN_SIZE/4, SCREEN_SIZE/4]) #parameters (suface, surfacerect)

#Define function for 'round' number message
def round_message(msg_round, color):
    font = font_style.render(msg_round + str(round), True, color)
    screen.blit(font, [SCREEN_SIZE/4, SCREEN_SIZE/4])

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            running = False
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            #Did they hit left arrow?
            if event.key == pygame.K_LEFT:
                x1_change = -cell_size
                y1_change = 0
            # Did they hit right arrow?
            elif event.key == pygame.K_RIGHT:
                x1_change = cell_size
                y1_change = 0
            # Did they hit up arrow?
            elif event.key == pygame.K_UP:
                x1_change = 0
                y1_change = -cell_size
            # Did they hit down arrow?
            elif event.key == pygame.K_DOWN:
                x1_change = 0
                y1_change = cell_size

    #Updating snake head coordinates and redrawing snake
    x1 += x1_change
    y1 += y1_change
    screen.fill(black)
    pygame.draw.rect(screen, green, [x1, y1, cell_size, cell_size])

    # Makes food appear & stops food from appearing within snake tail
    if not [x2, y2] in snake_coordinates:
        pygame.draw.rect(screen, red, [x2, y2, cell_size, cell_size])
    else:
        x2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)
        y2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)

    #keep track of coordinates of head of snake
    head_snake = []
    head_snake.append(x1)  # adding current x and y coordinates of snake head to list
    head_snake.append(y1)
    print(head_snake)

    snake_coordinates.append(head_snake)  # adding head coordinates to main snake list (placed as list of x,y within list e.g. [[200, 340], [200, 340]])
        # when head added - remove the first item of list (oldest coordinates) so doesnt continue to grow when not eating food

    # Makes sure the snake coordinates are always as many as needed for the current length of the snake
    if len(snake_coordinates) > snake_length:
        del snake_coordinates[0]
    print(snake_coordinates)

    # Draws the snake tail
    for s in snake_coordinates:  # iterates through snake_coordinates list, as lists within lists so deals with each set of x and y coordinates at a time
        pygame.draw.rect(screen, green, [s[0], s[1], cell_size, cell_size])
    pygame.display.update()

    #When snake collides with food it grows in length
    if x1 == x2 and y1 == y2:
        x2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)
        y2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)
        snake_length += 1
        score += 1

    #When snake hits screen edge OR hits itself, then game over
    if x1 >= SCREEN_SIZE or x1 < 0 or y1 >= SCREEN_SIZE or y1 < 0 or [x1, y1] in snake_coordinates[0:-1]:
        score_message('You Lose! Your score = ', red)
        pygame.display.update()
        pygame.time.delay(2000)

        screen.fill(black)

        round += 1
        round_message('Round ', pink)
        pygame.display.update()
        pygame.time.delay(2000)

        #Resets game so can play again immediately
        head_snake *= 0
        snake_coordinates *= 0
        snake_length = 1
        score = 0
        x1 = SCREEN_SIZE / 2
        y1 = SCREEN_SIZE / 2
        x2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)
        y2 = random.randrange(cell_size, SCREEN_SIZE, cell_size)
        pygame.draw.rect(screen, green, [x1, y1, cell_size, cell_size])
        pygame.display.update()

    #Controls speed of snake
    clock.tick(snake_speed)

# Done! Time to quit.
pygame.quit()
import pygame
import random

pygame.init()

# Colour Library - defined by RGB values, use of tuples
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Imported Images
# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame - Link used to develop understanding of how to add an image to background
BackGround = pygame.image.load('BG.jpg')
SnakeFood = pygame.image.load('Apple2.png')

# Screen Dimensions
ScreenWidth = 500
ScreenHeight = 500
Screen = pygame.display.set_mode([ScreenWidth, ScreenHeight])

fps = pygame.time.Clock()


# https://www.pygame.org/docs/tut/tom_games4.html - Link used to develop understanding of classes
# Classes for each type of object in the game
class Player(pygame.sprite.Sprite):
    # Setting up the initial characteristics of the player
    def __init__(self, SnakePos, SnakeBod, SnakeDir, SnakeSpeed):
        super().__init__()
        self.position = SnakePos
        self.Snake = SnakeBod
        self.direction = SnakeDir
        self.MoveDirection = SnakeDir
        self.Speed = SnakeSpeed

    # Function assigning labels to direction changes
    def directionChange(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    # Move function, constantly extends player by 5 coordinates.
    # The .pop function stops the player from constantly 'extending'
    def move(self, Block):
        if self.direction == "RIGHT":
            self.position[0] += self.Speed
        if self.direction == "LEFT":
            self.position[0] -= self.Speed
        if self.direction == "UP":
            self.position[1] -= self.Speed
        if self.direction == "DOWN":
            self.position[1] += self.Speed
        # This inserts the position to the snakes body (list) when snake hits the block
        # If snake doesnt hit food, the last element of the body is removed with the pop() function. This stops the snake getting constantly longer
        self.Snake.insert(0, list(self.position))
        # This translates the apples position from one point in the middle to the whole imagine
        # abs = absolute value of the x and y distances
        if abs(self.position[0] -Block[0]) < 15 and abs(self.position[1] -Block[1]) < 15:
            return 1
        else:
            self.Snake.pop()
            return 0

    # Game ending moves i.e collisions with the walls or itself
    # If player runs out of the dimensions of the screen or if the head of the snakes connects with the body
    def Collisions(self):
        if self.position[0] > 485 or self.position[0] < 0:
            return 1
        elif self.position[1] > 485 or self.position[1] < 0:
            return 1
        for SnakeSection in self.Snake[1:]:
            if self.position == SnakeSection:
                return 1
        return 0

    def SnakeHead(self):
        return self.position

    def SnakeBody(self):
        return self.Snake


# Class for creating the snake food
class Apple:
    # Initial characteristics of the food. Use random function to place object somewhere on the screen dimensions.
    def __init__(self):
        self.position = [random.randrange(10, 450), random.randrange(10, 450)]
        self.BlocksInScreen = True

    # Whenever blocks are run into, a new one is randomly sent to screen
    def GenerateBlock(self):
        if not self.BlocksInScreen:
            self.position = [random.randrange(10, 450), random.randrange(10, 450)]
            self.BlocksInScreen = True
        return self.position

    def Blocks(self, b):
        self.BlocksInScreen = b


def GameEnd():
    pygame.quit()


def EndStatement():
    # Closing Statement for single player Game.
    # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/ - Link used for understanding on displaying text in pygame.
    # .blit adds text and defines where it is on the screen with a tuple
    # Had to implement a time delay so message is displayed for prolonged period.

    pygame.font.init()
    MyFont = pygame.font.SysFont("Helvetica", 50)
    EndText = MyFont.render("GAME OVER", 1, BLUE)
    Screen.blit(EndText, (100, 100))
    pygame.display.flip()
    pygame.time.delay(1000)


# assigning the initial characteristics of each sprite in the game
player = Player([250, 400], [[100, 50], [90, 50], [80, 50]], "UP", 6)
player1 = Player([250, 100], [[100, 50], [90, 50], [80, 50]], "DOWN", 6)
Food = Apple()


# Function to allow game to be paused
def Pause(ReturnToGame):
    while True:
        Screen.blit(BackGround, (0, 0))
        PauseFont = pygame.font.SysFont("comicsansms", 20)
        PauseFont1 = pygame.font.SysFont("comicsansms", 40)
        msg1 = PauseFont1.render("Game Paused", 1, WHITE)
        msg2 = PauseFont.render("Press C to Continue", 1, WHITE)
        msg3 = PauseFont.render("Press Q to Quit", 1, WHITE)

        Screen.blit(msg1, (130, 100))
        Screen.blit(msg2, (155, 200))
        Screen.blit(msg3, (165, 250))
        pygame.display.update()

        # for loop allowing user to quit or continue game by pressing a corresponding button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameEnd()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return
                if event.key == pygame.K_q:
                    GameEnd()


# Generating the start (Intro) page of the game
# Two elements - adding text to screen and advancing to game with for loop.
def Intro():
    while True:
        Screen.blit(BackGround, (0, 0))
        IntroFont = pygame.font.SysFont("comicsansms", 20)
        IntroFont1 = pygame.font.SysFont("comicsansms", 40)
        msg1 = IntroFont1.render("WELCOME TO SNAKES", 1, WHITE)
        msg2 = IntroFont.render("To Win - Collect The Apples", 1, WHITE)
        msg3 = IntroFont.render("Press 2 to Play 2 Player Game", 1, WHITE)
        msg4 = IntroFont.render("Press 1 to Play Single Player Game", 1, WHITE)

        Screen.blit(msg1, (25, 100))
        Screen.blit(msg2, (125, 150))
        Screen.blit(msg3, (120, 250))
        Screen.blit(msg4, (100, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameEnd()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    TwoPlayer()
                if event.key == pygame.K_1:
                    SinglePlayer()


# 1 Player Game - Main Loop
def SinglePlayer():
    score = 0
    while True:
        # for loop defining all the user actions with the event.get() function
        # All actions involving pressing a key are within a KEYDOWN loop
        # https://stackoverflow.com/questions/33537959/continuous-movement-of-a-box-in-pygame - Code used to help understanding of moving the player.
        # Class = items with same attributes and characteristics

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameEnd()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.directionChange("RIGHT")
                elif event.key == pygame.K_LEFT:
                    player.directionChange("LEFT")
                elif event.key == pygame.K_UP:
                    player.directionChange("UP")
                elif event.key == pygame.K_DOWN:
                    player.directionChange('DOWN')
                elif event.key == pygame.K_p:
                    Pause(SinglePlay)
        FoodBlocks = Food.GenerateBlock()
        # When Player collides with Foodblocks, score increases
        if player.move(FoodBlocks):
            Food.Blocks(False)
            score += 1
        # Adding the background and apple to the screen
        Screen.blit(BackGround, (0, 0))
        Screen.blit(SnakeFood, Food.position)

        # Drawing the player to the screen
        for section in player.SnakeBody():
            pygame.draw.rect(Screen, WHITE, pygame.Rect(section[0], section[1], 15, 15))


        # If statement triggered after a 'Game ending collision'. Player score is displayed on Screen
        # Screen updated and time delay added to display score for 2 seconds.
        if player.Collisions():
            EndStatement()
            MyFont = pygame.font.SysFont("Helvetica", 40)
            YourScore = MyFont.render("Your Score: " + str(score), 1, WHITE)
            Screen.blit(YourScore, (120, 250))

            pygame.display.flip()
            pygame.time.delay(2000)
            GameEnd()

        # Messages displayed on the screen all the way through the game.
        MyFont1 = pygame.font.SysFont("Helvetica", 15)
        ScoreBoard1 = MyFont1.render("Score: " + str(score), 1, BLACK)
        PauseMessage = MyFont1.render("Press P to Pause", 1, BLACK)
        Screen.blit(ScoreBoard1, (200, 10))
        Screen.blit(PauseMessage, (10, 10))
        pygame.display.set_caption('Callums Game')
        pygame.display.update()
        pygame.display.flip()
        # Determining Frame Rate and thus speed of players on the screen
        x = 30
        # if score % 5:
            # player.Speed += 1
        fps.tick(x)




# Repeated Code for 2 players with addition of WASD keys for movement.
def TwoPlayer():
    Pscore = 0
    P1score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameEnd()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.directionChange("RIGHT")
                elif event.key == pygame.K_LEFT:
                    player.directionChange("LEFT")
                elif event.key == pygame.K_UP:
                    player.directionChange("UP")
                elif event.key == pygame.K_DOWN:
                    player.directionChange('DOWN')
                elif event.key == pygame.K_d:
                    player1.directionChange("RIGHT")
                elif event.key == pygame.K_a:
                    player1.directionChange("LEFT")
                elif event.key == pygame.K_w:
                    player1.directionChange("UP")
                elif event.key == pygame.K_s:
                    player1.directionChange('DOWN')
                elif event.key == pygame.K_p:
                    Pause(TwoPlayer)
        FoodBlocks = Food.GenerateBlock()
        if player.move(FoodBlocks):
            Pscore += 1
            Food.Blocks(False)
        if player1.move(FoodBlocks):
            P1score += 1
            Food.Blocks(False)

        Screen.blit(BackGround, (0, 0))
        Screen.blit(SnakeFood, Food.position)
        for section in player.SnakeBody():
            pygame.draw.rect(Screen, BLACK, pygame.Rect(section[0], section[1], 15, 15))
        for section in player1.SnakeBody():
            pygame.draw.rect(Screen, WHITE, pygame.Rect(section[0], section[1], 15, 15))

        if player.Collisions() == 1 or player1.Collisions() == 1:
            if player.Collisions() ==1:
                Pscore -= 5
            if player1.Collisions() ==1:
                P1score -= 5
            EndStatement()
            MyFont = pygame.font.SysFont("Helvetica", 40)
            WhiteScore = MyFont.render("White Score: " + str(P1score), 1, WHITE)
            BlackScore = MyFont.render("Black Score: " + str(Pscore), 1, WHITE)
            Screen.blit(WhiteScore, (120, 250))
            Screen.blit(BlackScore, (120, 300))
            pygame.display.flip()
            pygame.time.delay(2000)
            GameEnd()

        MyFont1 = pygame.font.SysFont("Helvetica", 20)
        ScoreBoard1 = MyFont1.render("Black: " + str(Pscore), 1, BLACK)
        ScoreBoard2 = MyFont1.render("White: " + str(P1score), 1, BLACK)
        PauseMessage = MyFont1.render("Press P to Pause", 1, BLACK)
        Instructions = MyFont1.render("Die and you lose 5 points!", 1, BLACK)
        Screen.blit(ScoreBoard1, (10, 10))
        Screen.blit(ScoreBoard2, (300, 10))
        Screen.blit(PauseMessage, (10, 470))
        Screen.blit(Instructions, (260, 470))
        pygame.display.set_caption('Callums Game')
        pygame.display.flip()
        fps.tick(30)


Intro()

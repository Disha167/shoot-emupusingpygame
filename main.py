import pygame
import random
import math
from pygame import mixer

# Initialise all the pygame modules
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

# background image
backgroundimg = pygame.image.load('background.png')

#music
#MUSIC IS USED AS WE WANT TO PLAY IT CONTINOUSLY
mixer.music.load('background.wav')
#to play it in a loop, not just once. Load only makes it play once.
mixer.music.play(-1)

#score
score_value =0
font_score=pygame.font.Font("freesansbold.ttf",25)
text_X = 10
text_Y = 10

#game over
over_score=pygame.font.Font("freesansbold.ttf",90)

# title and icon
pygame.display.set_caption("Shoot'EM UP!!")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# shooter image load
shooterimg = pygame.image.load('space-ship.png')
shooterimg_X = 350
shooterimg_Y = 500
X_change = 0

#creating a list of all ufos
ufoimg=[]
ufoimg_X=[]
ufoimg_Y=[]
ufoX_change=[]
ufoY_change=[]


# ufo image load
no_of_ufo = 10
for i in range(no_of_ufo):
    ufoimg.append(pygame.image.load('ufo.png'))
    ufoimg_X.append(random.randint(10, 725))
    ufoimg_Y.append(random.randint(50, 150))
    ufoX_change.append(5)
    ufoY_change.append(40)

# bullet image load
bulletimg = pygame.image.load('bullet.png')
bulletimg_X = shooterimg_X
bulletimg_Y = shooterimg_Y
# When ready is false, it means that bullet is not visible on screen
ready = False


def shooter(X, Y):
    screen.blit(shooterimg, (X, Y))


def ufo(ufoimg_X, ufoimg_Y ,i):
    screen.blit(ufoimg[i] , (ufoimg_X, ufoimg_Y))


def bullet(X, Y):
    global ready
    ready = True
    screen.blit(bulletimg, (X + 16, Y + 10))


def collision(bulletimg_X, bulletimg_Y, ufoimg_X, ufoimg_Y):
    distance = math.sqrt((math.pow(bulletimg_X - ufoimg_X, 2)) + (math.pow(bulletimg_Y - ufoimg_Y, 2)))
    if distance < 27:
        return True
    return False

#show score
def show_score(text_X,text_Y):
    score=font_score.render("Score : "+str(score_value), True , (255,255,255))
    screen.blit(score, (text_X,text_Y))

#show GAME OVER
def show_gameover():
    gameover=over_score.render("GAME OVER", True , (255,255,255))
    screen.blit(gameover, (140,230))



running = True
while running:
    # we fill the screen before as we draw all the stuffs above it
    screen.fill((0, 0, 0))
    screen.blit(backgroundimg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change = -5
                # print(shooterimg_X)
            if event.key == pygame.K_RIGHT:
                X_change = 5

            if event.key == pygame.K_SPACE:
                # We need to put if not ready condition here as we don't want to change the direction of the bullet according
                # to the shooter co-ordinate every time we press spacebar. USE OF THIS IF SIMILAR TO CALLING BULLET FUNCTION
                # BELOW THE IF NOT READY CONDITION
                if not ready:
                    bulletimg_X = shooterimg_X
                    # we need to call the bullet function here once as we don't want to change the bullet Y co-ordinate with respect to
                    # the gun. Once, the bullet gets the shooter_X coordinate , then it should go in that direction only, it should not
                    # change it's direction according to the shooter.
                    bullet(bulletimg_X, bulletimg_Y)
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            X_change = 0
    if ready:
        # It is necessary to call bullet function here as we have to draw the bullet again and again continously on
        # changing it's y co-ordinate by 2 i.e MAKE IT PERSISTENT
        bullet(bulletimg_X, bulletimg_Y)
        bulletimg_Y -= 14
    shooterimg_X += X_change

    # set boundaries for shooter
    if shooterimg_X < 0:
        shooterimg_X = 0
    if shooterimg_X > 730:
        shooterimg_X = 730

    # UFO MOVEMENT & when ufo hits the boundary
    for i in range(no_of_ufo):
        #game over
        if ufoimg_Y[i] > 440:
            for j in range(no_of_ufo):
                ufoimg_Y[j]=1000
                show_gameover()
            break

        if ufoimg_X[i] <= 0:
            ufoimg_Y[i] += ufoY_change[i]
            ufoX_change[i] = 5
        if ufoimg_X [i]>= 730:
            ufoimg_Y[i] += ufoY_change[i]
            ufoX_change[i] = -5

        ufoimg_X[i] += ufoX_change[i]

        collision_condition = collision(bulletimg_X, bulletimg_Y, ufoimg_X[i], ufoimg_Y[i])

        if collision_condition:
            bulletimg_Y=480
            ready= False
            #10 to 725 as we move the enemy down at 730
            ufoimg_X [i]= random.randint(10, 725)
            ufoimg_Y[i] = random.randint(50, 150)
            score_value += 1
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()

        #we pass here i so as to blit the ith image in ufo function
        ufo(ufoimg_X[i], ufoimg_Y[i],i)

    # to make sure that shooter appears everytime on screen
    shooter(shooterimg_X, shooterimg_Y)

    #score
    show_score(text_X,text_Y)

    if bulletimg_Y < 0:
        bulletimg_Y = shooterimg_Y
        # So that we go inside the space event again
        ready = False

    pygame.display.update()



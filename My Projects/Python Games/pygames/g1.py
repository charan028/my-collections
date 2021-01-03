import pygame
import math
import random
from pygame import mixer

#intialize pygame
pygame.init()
# create screen
screen=pygame.display.set_mode((800, 600))
#background
bg=pygame.image.load('b2.jpg')
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)
#title  and Icon
pygame.display.set_caption("space invader")
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
#player image

playerimg=pygame.image.load('1.png')

playerx= 370
playery=480
playerx_change=0

#mutiple enemies
enemyimg=[]
ex=[]
ey=[]
ex_change=[]
ey_change=[]
no_of_enemies=6
#enemy image
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('e2.png'))

    ex.append( random.randint(0,800))
    ey.append(random.randint(40,160))
    ex_change.append(1)
    ey_change.append(20)

#bullet
bulletimg=pygame.image.load('bu.png')
bx= 0
by=480
bx_change=0
by_change=10
#ready you can't see the bulet
# #fire bullet is currently moving 
b_state ="ready"
#score
score=0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10
#game over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def showscore(x,y):
    s=font.render("Score:" + str(score),True,(255,255,255))
    screen.blit(s,(x,y))
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))


def player(x,y):
    #draw img to screen
    screen.blit(playerimg,(playerx,playery))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global b_state
    b_state="fire"
    screen.blit(bulletimg,(x+16,y+10))
def iscollison(ex,ey,bx,by):
    dis=math.sqrt((math.pow(ex-bx,2)+ math.pow(ey-by,2)))
    if dis<27:
        return True
    else:
        return False
#game loop
run=True
while run:
    #red,green,blue(0-255)
    screen.fill((0,0,0))
    #backgroung 
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    #check key stroke
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerx_change =-1
                print("left arrow pressed")
            if event.key==pygame.K_RIGHT:
                playerx_change=1
                print("right arrow pressed")
            if event.key==pygame.K_SPACE:
                if b_state is "ready":
                    b_s=mixer.Sound("laser.wav")
                    b_s.play()
                    #get spceship x,y coordinate
                    bx=playerx
                    fire_bullet(bx,by)
                print("space pressed")

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerx_change=0.0
                print("Keystroke released")
    #player boundary
    playerx+=playerx_change
    if playerx<=0:
        playerx=0
    elif playerx>=736:
        playerx=736
    #enemy boundary
    for i in range(no_of_enemies):
        #game over
        if ey[i]>420:
            for j in range(no_of_enemies):
                ey[j]=2000
            game_over_text()
            break

        ex[i]+=ex_change[i]
        if ex[i]<=0:
            ex_change[i]=0.8
            ey[i]+=ey_change[i]
        elif ex[i]>=736:
            ex_change[i]=-0.8
            ey[i]+=ey_change[i]
        #collison
        collison=iscollison(ex[i],ey[i],bx,by)
        if collison:
            explosion_s=mixer.Sound('explosion.wav')
            explosion_s.play()
            by=480
            b_state="ready"
            score+=1
            print(score)
            ex[i]= random.randint(0,735)
            ey[i]=random.randint(40,160)
        enemy(ex[i],ey[i],i)


    #bullet Movement
    if by<=0:
        by=480
        b_state="ready"

    if b_state is "fire":
        fire_bullet(bx,by)
        by-=by_change
    

    

    player(playerx,playery)
    showscore(textx,texty)
    pygame.display.update()

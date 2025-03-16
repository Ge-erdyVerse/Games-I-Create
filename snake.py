import pygame
import math
import random
import time
pygame.init()
pygame.display.set_caption("Snake")
pygame.event.set_grab(True)
WIDTH,HEIGHT=600,400
size=20
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
frame_count=0
score=0
move_delay=max(1,int(5-math.log1p(score)/2))
last_eat_time=time.time()
shrink_interval=5
shrink_enabled=False
font=pygame.font.Font(None,36)
snake_body=[(300,200),(280,200),(260,200)]
direction="RIGHT"
change_to=direction
food_x=random.randint(0,(WIDTH-size)//size)*size
food_y=random.randint(0,(HEIGHT-size)//size)*size
GREEN=(0,255,0)
DARK_GREEN=(0,200,0)
RED=(255,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
def draw_snake(screen,snake_body,direction,frame_count):
    for i,block in enumerate(snake_body):
        x,y=block
        if i==0:
            pygame.draw.circle(screen,GREEN,(x+size//2,y+size//2),size//2)
            eye_offset_x=size//4 if direction in ["LEFT","RIGHT"] else 0
            eye_offset_y=size//4 if direction in ["UP","DOWN"] else 0
            eye1=(x+size//3+eye_offset_x,y+size//3+eye_offset_y)
            eye2=(x+2*size//3-eye_offset_x,y+size//3+eye_offset_y)
            pygame.draw.circle(screen,BLACK,eye1,size//8)
            pygame.draw.circle(screen,BLACK,eye2,size//8)
            if frame_count%20<10:
                tongue_length=7
                if direction=="RIGHT":
                    tongue=[(x+size,y+size//2),(x+size+tongue_length,y+size//2)]
                elif direction=="LEFT":
                    tongue=[(x,y+size//2),(x-tongue_length,y+size//2)]
                elif direction=="UP":
                    tongue=[(x+size//2,y),(x+size//2,y-tongue_length)]
                else:
                    tongue=[(x+size//2,y+size),(x+size//2,y+size+tongue_length)]
                pygame.draw.line(screen,RED,tongue[0],tongue[1],2)
        else:
            wiggle=int(math.sin(i*0.5+frame_count*0.1)*3)
            pygame.draw.rect(screen,DARK_GREEN,(x+wiggle,y,size,size))
def draw_food():
    pygame.draw.circle(screen,YELLOW,(food_x+size//2,food_y+size//2),size//2)
def move_snake():
    global snake_body,direction,change_to,food_x,food_y,score,move_delay,last_eat_time,shrink_enabled
    if change_to=="UP" and direction!="DOWN":
        direction="UP"
    if change_to=="DOWN" and direction!="UP":
        direction="DOWN"
    if change_to=="LEFT" and direction!="RIGHT":
        direction="LEFT"
    if change_to=="RIGHT" and direction!="LEFT":
        direction="RIGHT"
    (head_x,head_y)=snake_body[0]
    if direction=="UP":
        head_y-=size
    elif direction=="DOWN":
        head_y+=size
    elif direction=="LEFT":
        head_x-=size
    elif direction=="RIGHT":
        head_x+=size
    if head_x<0:
        head_x=WIDTH-size
    elif head_x>=WIDTH:
        head_x=0
    if head_y<0:
        head_y=HEIGHT-size
    elif head_y>=HEIGHT:
        head_y=0
    new_head=(head_x,head_y)
    if new_head in snake_body:
        game_over_screen()
        return
    snake_body.insert(0,new_head)
    if new_head==(food_x,food_y):
        score+=10
        move_delay=max(1,int(5-score/50))
        last_eat_time=time.time()
        if score>=100:
            shrink_enabled=True
        food_x=random.randint(0,(WIDTH-size)//size)*size
        food_y=random.randint(0,(HEIGHT-size)//size)*size
    else:
        snake_body.pop()
def reset_game():
    global snake_body,direction,change_to,food_x,food_y,score
    snake_body=[(300,200),(280,200),(260,200)]
    direction="RIGHT"
    change_to=direction
    score=0
    food_x=random.randint(0,(WIDTH-size)//size)*size
    food_y=random.randint(0,(HEIGHT-size)//size)*size
def draw_score():
    score_text=font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(10,10))
def game_over_screen():
    game_over_text=font.render("Game Over!",True,RED)
    restart_text=font.render("Press any key to restart",True,WHITE)
    screen.fill((0,0,0))
    game_over_rect=game_over_text.get_rect(center=(WIDTH//2,HEIGHT//2-20))
    restart_rect=restart_text.get_rect(center=(WIDTH//2,HEIGHT//2+20))
    screen.blit(game_over_text,game_over_rect)
    screen.blit(restart_text,restart_rect)
    pygame.display.flip()
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                waiting=False
            elif event.type==pygame.QUIT:
                pygame.quit()
                exit()
    reset_game()
running=True
while running:
    screen.fill((30,30,30))
    frame_count+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP and direction!="DOWN":
                change_to="UP"
            if event.key==pygame.K_DOWN and direction!="UP":
                change_to="DOWN"
            if event.key==pygame.K_LEFT and direction!="RIGHT":
                change_to="LEFT"
            if event.key==pygame.K_RIGHT and direction!="LEFT":
                change_to="RIGHT"
    if frame_count%move_delay==0:
        move_snake()
    if shrink_enabled and time.time()-last_eat_time>shrink_interval and len(snake_body)>2:
        snake_body.pop()
        last_eat_time=time.time()
    if len(snake_body)<=2:
        game_over_screen()
    draw_snake(screen,snake_body,direction,frame_count)
    draw_food()
    draw_score()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()

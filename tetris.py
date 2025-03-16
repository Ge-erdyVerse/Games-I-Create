import pygame
import sys
import random
pygame.init()
WIDTH,HEIGHT=600,600
ROWS,COLS=20,20
CELL_SIZE=30
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tetris")
BLACK=(0,0,0)
GRAY=(50,50,50)
WHITE=(255,255,255)
RED=(255,0,0)
COLORS={"I":(0,255,255),"O":(255,255,0),"T":(128,0,128),"L":(255,165,0),"J":(0,0,255),"S":(0,255,0),"Z":(255,0,0)}
SHAPES={"I":[[1,1,1,1]],"O":[[1,1],[1,1]],"T":[[0,1,0],[1,1,1]],"L":[[0,0,1],[1,1,1]],"J":[[1,0,0],[1,1,1]],"S":[[0,1,1],[1,1,0]],"Z":[[1,1,0],[0,1,1]]}
grid=[[None for _ in range(COLS)] for _ in range(ROWS)]
score=0
font=pygame.font.Font(None,36)
game_over=False
last_rotation_time=pygame.time.get_ticks()
def rotate_grid():
    global grid
    grid=[list(row) for row in zip(*grid[::-1])]
    apply_gravity()
def apply_gravity():
    global grid
    for col in range(COLS):
        empty_rows=[]
        for row in range(ROWS-1,-1,-1):
            if grid[row][col] is None:
                empty_rows.append(row)
            elif empty_rows:
                new_row=empty_rows.pop(0)
                grid[new_row][col]=grid[row][col]
                grid[row][col]=None
                empty_rows.append(row)
def reset_game():
    global grid,score,game_over,tetromino,last_rotation_time
    grid=[[None for _ in range(COLS)] for _ in range(ROWS)]
    score=0
    game_over=False
    last_rotation_time=pygame.time.get_ticks()
    tetromino=Tetromino()
class Tetromino:
    def __init__(self):
        self.type=random.choice(list(SHAPES.keys()))
        self.shape=SHAPES[self.type]
        self.color=COLORS[self.type]
        self.x=COLS//2-len(self.shape[0])//2
        self.y=0
        self.last_move_time = pygame.time.get_ticks()
    def draw(self):
        for row_idx,row in enumerate(self.shape):
            for col_idx,cell in enumerate(row):
                if cell:
                    pygame.draw.rect(SCREEN,self.color,((self.x+col_idx)*CELL_SIZE,(self.y+row_idx)*CELL_SIZE,CELL_SIZE,CELL_SIZE))
    def check_collision(self,dx=0,dy=0,rotated_shape=None):
        shape=rotated_shape if rotated_shape else self.shape
        for row_idx,row in enumerate(shape):
            for col_idx,cell in enumerate(row):
                if cell:
                    new_x=self.x+col_idx+dx
                    new_y=self.y+row_idx+dy
                    if new_x<0 or new_x>=COLS or new_y>=ROWS or (new_y>=0 and grid[new_y][new_x] is not None):
                        return True
        return False
    def move_down(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.last_move_time>300 and not game_over:
            if not self.check_collision(dy=1):
                self.y+=1
            else:
                self.lock_piece()
            self.last_move_time=current_time
    def move_horizontal(self,direction):
        if not self.check_collision(dx=direction):
            self.x+=direction
    def rotate(self):
        rotated_shape=[list(row) for row in zip(*self.shape[::-1])]
        if not self.check_collision(rotated_shape=rotated_shape):
            self.shape=rotated_shape
    def lock_piece(self):
        global game_over
        for row_idx,row in enumerate(self.shape):
            for col_idx,cell in enumerate(row):
                if cell:
                    if grid[self.y+row_idx][self.x+col_idx] is not None:
                        game_over=True
                        pygame.display.update()
                        return
                    grid[self.y+row_idx][self.x+col_idx]=self.color
        clear_rows()
        global tetromino
        tetromino=Tetromino()
def clear_rows():
    global grid,score
    new_grid=[row for row in grid if any(cell is None for cell in row)]
    rows_cleared=ROWS-len(new_grid)
    grid=[[None for _ in range(COLS)] for _ in range(rows_cleared)]+new_grid
    score+=rows_cleared*100
def draw_game_over():
    text=font.render("GAME OVER - Press R to restart",True, RED)
    SCREEN.blit(text,(WIDTH//2-200,HEIGHT//2))
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(SCREEN,GRAY,(col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE),1)
            if grid[row][col]:
                pygame.draw.rect(SCREEN,grid[row][col],(col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE))
def draw_score():
    score_text=font.render(f"Score: {score}",True,WHITE)
    SCREEN.blit(score_text,(10,10))
clock=pygame.time.Clock()
tetromino=Tetromino()
running=True
while running:
    SCREEN.fill(BLACK)
    draw_score()
    if game_over:
        draw_game_over()
    else:
        draw_grid()
        tetromino.move_down()
        tetromino.draw()
    current_time=pygame.time.get_ticks()
    if current_time-last_rotation_time>10000:
        rotate_grid()
        last_rotation_time=current_time
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if game_over and event.key==pygame.K_r:
                reset_game()
            elif event.key==pygame.K_LEFT:
                tetromino.move_horizontal(-1)
            elif event.key==pygame.K_RIGHT:
                tetromino.move_horizontal(1)
            elif event.key==pygame.K_UP:
                tetromino.rotate()
    pygame.display.update()
    clock.tick(30)
pygame.quit()
sys.exit()

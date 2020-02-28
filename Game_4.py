import pygame
import random

pygame.font.init()

#GLOBALS VARS
s_width=800
s_height=700
play_width=300
play_height=600
block_size=30

top_left_x=(s_width-play_width)//2
top_left_y=s_height-play_height
#Shape Formats
S=[['.....',
    '.....',
    '..00.',
    '.00..',
    '.....',],
   ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....',]]
Z=[['.....',
    '.....',
    '.00..',
    '..00.',
    '.....',],
   ['.....',
    '..0..',
    '.00.',
    '.0...',
    '.....',]]
I=[['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....',],
   ['.....',
    '0000.',
    '.....',
    '.....',
    '.....',]]
D=[['.....',
    '.....',
    '.00..',
    '.00..',
    '.....',]]
J=[['.....',
    '.0...',
    '.000.',
    '.....',
    '.....',],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....',],
   ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....',],
   ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....',]]
L=[['.....',
    '...0.',
    '.000.',
    '.....',
    '.....',],
   ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....',],
   ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....',],
   ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....',]]
T=[['.....',
    '..0..',
    '.000.',
    '.....',
    '.....',],
   ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....',],
   ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....',],
   ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....',]]
shapes=[S,Z,I,D,J,L,T]
shape_colors=[(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,255),(120,0,120)]
class Piece(object):
    rows = 20  # y
    columns = 10  # x
    def __init__(self,column,row,shape):
        self.x=column
        self.y=row
        self.shape=shape
        self.color=shape_colors[shapes.index(shape)]
        self.rotation=0   # number from 0-3
        

def create_grid(locked_pos={}):
    grid=[[(0,0,0) for x in range (10)] for x in range(20)] # a sub list for each row 
    
    for i in range (len(grid)):
        for j in range (len(grid[i])):
            if (j,i) in locked_pos:
                c= locked_pos[(j,i)]
                grid[i][j]=c
    return grid
                
def convert_shape_format(shape):
    positions=[]
    format = shape.shape[shape.rotation % len(shape.shape)]#current shape
    for i ,line in enumerate(format):#shapes
        row=list(line) # sub shapes 
        for j,colums in enumerate(row):
            if colums  == '0':
                positions.append((shape.x+j ,shape.y+i))
    for i, pos in enumerate (positions): #offest
        positions[i]=(pos[0]-2,pos[1]-4)

    return positions
            
        
    

def valid_space(shape,grid):
    accepted_pos=[[(j,i) for j in range (10) if grid [i][j]==(0,0,0)] for i in range(20)] #empty space 
    accepted_pos=[j for sub in accepted_pos for j in sub]  # convert to 1D array
    formatted=convert_shape_format(shape)
    for pos in   formatted:
        if pos not  in accepted_pos:
            if pos[1]>-1:
                return False
    return True
            
def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

def check_lost(positions):
    for pos  in positions :
        x,y=pos
        if y<1 :
            return True
    return False

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface,row, col):
    sx=top_left_x
    sy=top_left_y
    for  i in range (row):
        pygame.draw.line(surface,(128,128,128),(sx, sy + i* block_size),(sx+play_width,sy+ i* 30))# horizontal lines
        for j in range (col):
            pygame.draw.line(surface,(128,128,128),(sx+ j* block_size,sy),(sx+ j* block_size,sy+play_height)) # vertical lines



def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
#shift row
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
 
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))

def draw_window(surface,score=0,last_score=0):
    
    surface.fill((0,0,0))
    pygame.font.init()
    font=pygame.font.SysFont('comicsans',60)
    label =font.render('Tetris',1,(255,255,255))
    surface.blit(  label ,(top_left_x+ play_width/2 -(label.get_width()/2) ,30))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score :  '+str(score), 1, (255,255,255))
    surface.blit(label ,(sx+ 20 ,sy+150))

    sx = top_left_x -200
    sy = top_left_y +200
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Top Score :  '+str(last_score), 1, (255,255,255))
    surface.blit(label ,(sx+ 20 ,sy+150))


    for i in range (len(grid)):                
        for j in range (len(grid[i])):
           pygame.draw.rect(surface,grid[i][j], (top_left_x+ j*block_size,top_left_y+ i *block_size,block_size,block_size),0)
    draw_grid(surface,20,10)
    
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)                 
    #pygame.display.update()
def update_score(score): #should write  to file else app crush 
    nscore=max_score()
    with open('score.txt','w') as f:
        if int(score)>int(nscore) :
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('score.txt','r') as f:
        lines=f.readlines()
        print(lines)
        score=lines[0].strip()
    return score
    
        
        
def main():
    
    global grid ,win
    
    locked_pos={}
    grid =create_grid(locked_pos)
    change_piece=False
    run=True
    
    current_piece=get_shape()
    next_piece=get_shape()
    
    clock=pygame.time.Clock()
    
    fall_time=0
    fall_speed=0.27
    level_time=0

    last_score=max_score()
    score=0
    
    while run:
        grid =create_grid(locked_pos)
        level_time+=clock.get_rawtime() #ms 
        fall_time+=clock.get_rawtime() #ms 
        clock.tick()
        if level_time/1000 > 5:#s
            level_time=0
            if level_time>0.12:
                level_time-=0.005
            
        if fall_time/1000 > fall_speed:
            fall_time=0
            current_piece.y+=1
            if not (valid_space(current_piece,grid)) and current_piece.y>0 :
                current_piece.y-=1
                change_piece=True
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT :
                pygame.display.quit()
                run=False
                quit()
            #key event
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT :
                    current_piece.x-=1
                    if not (valid_space(current_piece,grid)) :
                        current_piece.x+=1
                if event.key == pygame.K_RIGHT:
                    current_piece.x+=1
                    if not (valid_space(current_piece,grid)) :
                        current_piece.x-=1
                if event.key == pygame.K_DOWN:
                    current_piece.y+=1
                    if not (valid_space(current_piece,grid)) :
                        current_piece.y-=1

                if event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not (valid_space(current_piece,grid)) :
                        current_piece.rotation-=1
                if event.key == pygame.K_SPACE:
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
        shape_pos=convert_shape_format(current_piece)
        for i in range (len(shape_pos)):
            x,y=shape_pos[i]
            if y>-1:
                grid[y][x]=current_piece.color

        if change_piece:
            for pos in shape_pos:
                p=(pos[0],pos[1])
                locked_pos[p]=current_piece.color
            current_piece=next_piece
            next_piece=get_shape()
            change_piece=False
            score+=clear_rows(grid, locked_pos) *10
               
        draw_window(win,score,last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost( locked_pos):
            
            run=False
    update_score(score)       
    draw_text_middle('You lost', 60, (255, 255, 255), win)  
    pygame.display.update()
    pygame.time.delay(2000)
                
                
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption("Tetris")
main_menu()




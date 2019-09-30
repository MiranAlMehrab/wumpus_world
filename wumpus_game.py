import os
import time
import pygame
from pygame.locals import *
from random import randrange

###########Global variable ##################
list_of_caves = []
cave_color = (240,255,255)  
bg_color = [166,214,8]


agent_right_image = pygame.image.load('images/agent_right.jpg')
agent_left_image = pygame.image.load('images/agent_left.jpg') 
agent_image = agent_right_image
wumpus_image = pygame.image.load('images/wumpus.jpg')
gold_image = pygame.image.load('images/gold.jpg')
pit_image = pygame.image.load('images/pit.jpg')
breeze_image = pygame.image.load('images/breeze.png')
stench_image = pygame.image.load('images/stench.jpg')
agent_previous_position = [1,1]
interval_time = 1

path_cost_so_far = 0

###################Map elemnts list #######################
def print_list(list_name):
        for i in range(0,len(list_name)):
                for j in range(0,len(list_name[i])):
                        print(pit_in_cave[i][j])
                print()



def create_list(row_size,column_size):
        new_list = [[0 for x in range(column_size)] for x in range(row_size)] 
        return new_list


pit_in_cave = create_list(10,10)
wumpus_in_cave = create_list(10,10)
glitter_in_cave = create_list(10,10)
agent_in_cave = create_list(10,10)
breeze_in_cave = create_list(10,10)
strench_in_cave = create_list(10,10)

######Initialize screen of game window ####################

game_window_width = 1000 
game_window_height = 700

pygame.init()
screen = pygame.display.set_mode((game_window_width, game_window_height))
pygame.display.set_caption('Wumpus World')
screen.fill(bg_color)

label_font = pygame.font.SysFont("Comic Sans MS", 25)
label = label_font.render("Agent's Mind", True, [230,230,240])
screen.blit(label, (720, 20))      

def event_handler():    
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):    
            pygame.quit() #quit from pygame
            quit() #quit from py system


text_x = 720
text_y = 50
def update_agent_mind(perception):
        font_name = pygame.font.match_font('arial')
        font_size = 20

        mind_font = pygame.font.Font(font_name, font_size)
        perception_surface = mind_font.render(perception, True, [0,0,0])
        perception_rect = perception_surface.get_rect()
        
        global text_x,text_y  
        perception_rect.midtop = (text_x,text_y)
        screen.blit(perception_surface,perception_rect)
        if(text_y+20<680):
                text_y += 20
        else:
                text_x += 40
                text_y = 50
       

def draw_map():

        rect_width = 60
        rect_height = 60
                      
        left_padding = 25
        top_padding = 25

        for j in range(0,10):
                for i in range(0,10):

                        pos_x = (i*65)+left_padding
                        pos_y = (j*65)+top_padding
                        pygame.draw.rect(screen,cave_color,pygame.Rect(pos_x, pos_y, rect_width, rect_height))

                        cave_index = [pos_x,pos_y]
                        list_of_caves.append(cave_index)


def get_adjacent_caves(i,j):
        adjacent_caves = []
        
        if((i-1)>=0):
                adjacent_caves.append([i-1,j])
        if((i+1)<=9):
                adjacent_caves.append([i+1,j])
        if((j-1)>=0):
                adjacent_caves.append([i,j-1])
        if((j+1)<=9):
                adjacent_caves.append([i,j+1])
        
        return adjacent_caves


def get_image(name):
        global agent_image
        global wumpus_image
        global gold_image
        global pit_image

        if name == 'agent_image':
                return agent_image
        elif name == 'wumpus_image':
                return wumpus_image
        elif name == 'gold_image':
                return gold_image
        elif name == 'pit_image':
                return pit_image
        elif name == 'breeze_image':
                return breeze_image
        elif name == 'stench_image':
                return stench_image
        


def update_map_insights(element_type,index):
        
        str_index = str(index-1)
        str_index = str_index.rjust(2, '0')
        i = int(str_index[0])
        j = int(str_index[1])
        
        if element_type == agent_image:
                agent_in_cave[i][j] = 1
        elif element_type == gold_image:
                glitter_in_cave[i][j] = 1
        
        elif element_type == wumpus_image:
                wumpus_in_cave[i][j] = 1
                adjacent_caves = get_adjacent_caves(i,j)
                image_add_list = []
                
                for neighbour in adjacent_caves:
                        neighbour_i = int(neighbour[0])
                        neighbour_j = int(neighbour[1])
                        
                        print('i,j ::',i,' ',j)
                        strench_in_cave[neighbour_i][neighbour_j] = 1
                        
                        cave_number = str(neighbour_i)+str(neighbour_j)
                        str_cave_number = str(int(cave_number)+1) #add_image_to_map will decrease the cave number again by 1
                        image_add_list.append(['stench_image',str_cave_number])
                
                add_image_to_map(image_add_list)                       
                        
        elif element_type == pit_image:
                pit_in_cave[i][j] = 1
                adjacent_caves = get_adjacent_caves(i,j)
                image_add_list = []
                
                for neighbour in adjacent_caves:
                        neighbour_i = int(neighbour[0])
                        neighbour_j = int(neighbour[1])
                        breeze_in_cave[neighbour_i][neighbour_j] = 1
                        cave_number = str(neighbour_i)+str(neighbour_j)
                        str_cave_number = str(int(cave_number)+1) #add_image_to_map will decrease the cave number again by 1
                        image_add_list.append(['breeze_image',str_cave_number]) 
                
                add_image_to_map(image_add_list)


def add_image_to_map(all_cave_item):
        image_left_padding = 5
        image_top_padding = 5

        for cave in all_cave_item:
                image = get_image(cave[0])
                cave_number = int(cave[1].rjust(2, '0'))
                index_x = list_of_caves[cave_number-1][0] + image_left_padding #cave number starts from 1
                index_y = list_of_caves[cave_number-1][1] + image_top_padding  #cave number starts from 
                
                screen.blit(image,(index_x,index_y))
                update_map_insights(image,cave_number)


def get_cave_description(file_name):
        all_cave_item = []
        
        environemnt_description_file = open(file_name, "r")
        line = environemnt_description_file.readline()
        while line:
                parsed_line =  line.split(',')
                single_cave = [x.strip() for x in parsed_line] 
                all_cave_item.append(single_cave)

                line = environemnt_description_file.readline()
                
        environemnt_description_file.close()
        return all_cave_item
            


def add_environments_elements(file_name):
        
        all_cave_item = get_cave_description(file_name)
        add_image_to_map(all_cave_item)
        #print(all_cave_item)
        

def create_map_file(file_name):
        image_list = ['pit_image','wumpus_image','gold_image']
        map_file = open(file_name,"w")
        selected_cave = []
        for i in range(1,5):
                random_image = image_list[randrange(0,3)]
                random_cave = randrange(2,99)

                not_congested = True
                for cave_number in selected_cave:
                        if(abs(random_cave - cave_number) < 3 or abs(random_cave - cave_number) == 10):
                                not_congested = False
                                break

                if(random_cave > 1 and not_congested):
                        cave_str = str(random_image+','+str(random_cave)+'\n')
                        map_file.write(cave_str)
                        selected_cave.append(random_cave)

        map_file.close()
        

def get_random_map(file_name):
        create_map_file(file_name)
        


def update_total_cost():
        global path_cost_so_far
        path_cost_so_far = path_cost_so_far + 1
                
                
def keep_map_alive_and_update():
        
        random_file_name = "random_map_environemnt.txt"
        static_file_name = "environment.txt"
        get_random_map(random_file_name)
                
        while True:

                draw_map()
                #add_environments_elements(random_file_name) #random world
                add_environments_elements(static_file_name) #random world
                
                event_handler()
                move_agent(list_of_caves[randrange(100)][0],list_of_caves[randrange(100)][1])
                update_agent_mind(str(randrange(1,100)))
                        
                pygame.display.update()
                
                print_list(wumpus_in_cave)
                update_total_cost()
                global interval_time
                time.sleep(interval_time) #just to make agent move more visible !
                




################agent movement ##################
def move_agent(x,y):
        
        global agent_previous_position
        previous_x = agent_previous_position[0]
        if( previous_x >= x):
                agent_image = agent_left_image
        else:
                agent_image = agent_right_image

        screen.blit(agent_image,(x,y))
        agent_previous_position = [x,y]
 




########################main function from where the prgram starts#############################
def main():
        keep_map_alive_and_update()
        

if __name__ == '__main__':
        main()
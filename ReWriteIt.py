import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time as t
from sys import argv



def time_list_to_wpm(tl):
    wpm_list = []
    for i in range(len(tl) - 1):
        wpm = round((i+1)*60 / (tl[i+1] - tl[0]), 2)
        wpm_list.append(wpm)
    return wpm_list


def time_list_to_wpm1(tl):
    wpm_list = []
    for i in range(len(tl) - 1):
        wpm = round(60 / (tl[i+1] - tl[i]), 2)
        wpm_list.append(wpm)
    return wpm_list


def time_list_to_wpm10(tl):
    wpm_list = []
    for i in range(len(tl) - 1):
        if i < 8:
            wpm = round((i+1)*60 / (tl[i+1] - tl[0]), 2)
        else:
            wpm = round(600 / (tl[i+1] - tl[i-8]), 2)
        wpm_list.append(wpm)
    return wpm_list


def map_range(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def graph_it(x, y, width, height, color, color2,  line_width, name=None):
    total_time= round(x[-1] - x[0], 2)
    x = x[1:]
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    for i in range(len(x)):
        x[i] = int(map_range(x[i], x_min, x_max, 0, width))
    for i in range(len(y)):
        y[i] = int(map_range(y[i], y_min, y_max, 1, height-1))
        
    graph_surf = pygame.Surface((width, height))
    
    points = []
    for i in range(len(y)):
        points.append((x[i], height - y[i]))
        
    if name != None:
        name_surf = font80. render(name, True, color2)
        graph_surf.blit(name_surf, name_surf.get_rect(center = (width/2, height/2)))
    
    pygame.draw.line(graph_surf, color2, (0, 0), (width, 0), int(line_width/2))
    pygame.draw.line(graph_surf, color2, (0, height-int(line_width/2)), (width, height-int(line_width/2)), int(line_width/2))
    
    pygame.draw.lines(graph_surf, color, False, points, line_width)
    
    wpm_max_surf = font30.render(str(y_max), True, color2)
    wpm_min_surf = font30.render(str(y_min), True, color2)
    time_surf = font30.render(str(total_time)+"s", True, color2)
    graph_surf.blit(wpm_max_surf, wpm_max_surf.get_rect(topleft=(5,5)))
    graph_surf.blit(wpm_min_surf, wpm_min_surf.get_rect(bottomleft=(5,height-5)))
    graph_surf.blit(time_surf, time_surf.get_rect(bottomright=(width-5,height-5)))
    return graph_surf


def render_progress_bar(progress, color, bar_width):
    bar = pygame.Surface((screen.get_width(), bar_width))
    length = int(map_range(progress, 0, 1, 0, screen.get_width()))
    pygame.draw.rect(bar, color, pygame.Rect(0, 0, length, bar_width))
    return bar
    



pygame.init()
screen = pygame.display.set_mode([800, 450])

pygame.font.init()
pygame.display.set_caption("ReWriteIt")
pygame.display.set_icon(pygame.image.load("icon.ico"))
clock = pygame.time.Clock()
font100 = pygame.font.SysFont("Arial", 100)
font80 = pygame.font.SysFont("Arial", 80)
font30 = pygame.font.SysFont("Arial", 30)


try:
    if len(argv) > 1:
        with open(argv[1], "r") as f:
            text = f.read().replace("\n", " ").replace("\r", " ").replace("  ", " ").split(" ")
    else:
        with open("ToReWrite.txt", "r") as f:
            text = f.read().replace("\n", " ").replace("\r", " ").replace("  ", " ").split(" ")
    print("Data loaded")
except Exception as e:
    print(f"An error occurred while loading data:\n{e}")
    exit()

# print(len(text))

word_index = 0

word_to_write = text[word_index]
next_word = font80.render(text[word_index + 1], True, (150, 150, 150))

user_written = ""

wpm = 0

graph_wpm_surf = None
finished = False
time_started = False
time_list = []

while True:
    clock.tick(60)   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if finished:
                pygame.quit()
                quit()
            else:
                finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if finished:
                    pygame.quit()
                    quit()
                else:
                    finished = True
                
            if event.key == pygame.K_BACKSPACE:
                user_written =  user_written[:-1]
                
            elif not finished:
                key = event.unicode
                
                if user_written == word_to_write and (key == " " or key == "\r"):
                    time_list.append(t.time())
                    word_index += 1

                    if word_index < len(text):
                        word_to_write = text[word_index]
                        user_written = ""
                    else:
                        finished = True
                        word_to_write = "\n"
                        user_written = ""
                        break
                        
                    if word_index + 1 < len(text):
                        next_word = font80.render(text[word_index + 1], True, (150, 150, 150))
                    else:
                        next_word = font80.render("", True, (150, 150, 150))
                
                else:
                    if key == " " or key == "\r":
                        key = "☐"
                    if not time_started:
                        time_list.append(t.time())
                        time_started = True
                    user_written += key
    
    if len(time_list) >= 2:
        wpm = round((len(time_list)-1)*60 / (time_list[-1] - time_list[0]), 2)
        
    if len(time_list) >= 10:
        wpm10 = round(600 / (time_list[-1] - time_list[-10]), 2)
        
    if not finished:
        if user_written == word_to_write:
            word_surf = font80.render(word_to_write, True, (0, 255, 0))

        elif user_written == word_to_write[:-(len(word_to_write) - len(user_written))]:
            written_word_surf = font80.render(user_written, True, (0, 255, 0))
            to_write_word_surf = font80.render(word_to_write[len(user_written):], True, (150, 150, 150))
            
            word_surf = pygame.Surface((written_word_surf.get_width() + to_write_word_surf.get_width(), written_word_surf.get_height()), pygame.SRCALPHA)
            word_surf.blit(written_word_surf, (0, 0))
            word_surf.blit(to_write_word_surf, (written_word_surf.get_width(), 0))
        
        else:
            written_word_surf = font80.render(user_written, True, (255, 0, 0))
            to_write_word_surf = font80.render(word_to_write[len(user_written):], True, (150, 150, 150))
        
            word_surf = pygame.Surface((written_word_surf.get_width() + to_write_word_surf.get_width(), written_word_surf.get_height()), pygame.SRCALPHA)
            word_surf.blit(written_word_surf, (0, 0))
            word_surf.blit(to_write_word_surf, (written_word_surf.get_width(), 0))
            
    
    
    screen.fill([0,0,0])
    if not finished:
        screen.blit(word_surf, word_surf.get_rect(center = (400, 275)))
        screen.blit(next_word, next_word.get_rect(center = (400, 375)))
        wpm_surf = font100.render(f"WPM: {wpm}", True, (200, 200, 200))
        screen.blit(wpm_surf, wpm_surf.get_rect(center = (400, 75)))
        if len(time_list) > 10:
            if wpm10 >= wpm:
                wpm10_surf = font30.render(f"WPM10: {wpm10}", True, (150, 255, 150))
            else:
                wpm10_surf = font30.render(f"WPM10: {wpm10}", True, (255, 150, 150))
            screen.blit(wpm10_surf, wpm10_surf.get_rect(center = (400, 150)))
        preogress_bar_surf = render_progress_bar(word_index/len(text), (200,200,200), 10)
        screen.blit(preogress_bar_surf, preogress_bar_surf.get_rect(topleft = (0,0)))
        
    else:
        wpm_surf = font100.render(f"WPM: {wpm}", True, (255, 255, 255))
        screen.blit(wpm_surf, wpm_surf.get_rect(center = (400, 50)))
        if graph_wpm_surf == None:
            graph_wpm_surf = graph_it(time_list, time_list_to_wpm(time_list), 700, 150, (0,255,0), (0,100,200), 2, "WPM")
            graph_wpm10_surf = graph_it(time_list, time_list_to_wpm10(time_list), 350, 150, (255,255,0), (0,100,200), 2, "WPM10")
            graph_wpm1_surf = graph_it(time_list, time_list_to_wpm1(time_list), 350, 150, (255,0,0), (0,100,200), 2, "WPM1")
        screen.blit(graph_wpm_surf, graph_wpm_surf.get_rect(midtop = (400, 290)))
        screen.blit(graph_wpm10_surf, graph_wpm10_surf.get_rect(bottomleft = (410, 280)))
        screen.blit(graph_wpm1_surf, graph_wpm1_surf.get_rect(bottomright = (390, 280)))
        
    pygame.display.update()
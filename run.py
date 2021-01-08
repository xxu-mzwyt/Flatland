import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((720,600))

edges_list = [((-1, 2), (0, 1)),\
         ((0, 1), (1, 3)),\
         ((1, 3), (-1, 2))]

tot_display = []

c_node = [0., 0.]  # place of viewer

fov_start = 720  # the current visual field (degree * 4)
# e.g., 720 means an arc 180° -> 90° -> 0°

def cal_len(vec):  # return the length of a vector
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])

def cal_angle(vec):  # return the angle of a vector (degree * 4)
    angle_cos = vec[0] / cal_len(vec)
    angle = math.acos(angle_cos) * 180 / math.pi
    angle = int(angle * 4)
    if vec[1] < 0:
        angle = 1440 - angle
    return angle

def cal_dis(vec1, vec2, angle): # return the distance of a certain point
    len1 = cal_len(vec1)
    len2 = cal_len(vec2)
    ang1 = cal_angle(vec1)
    ang2 = cal_angle(vec2)

    dif = (angle - ang1) / (ang2 - ang1)
    rslt = len1 + (len2 - len1) * dif

    return rslt 

def swap(item1, item2):
    return item2, item1

def update():
    global tot_display, c_node
    # curr_ang: current angle in degree * 4
    # curr_dis: current minimum distance to the edges
    # tot_display = []
    for curr_ang in range(1440):
        curr_dis = float("inf")
        for edge in edges_list:
            node1 = (edge[0][0] - c_node[0], edge[0][1] - c_node[1])
            node2 = (edge[1][0] - c_node[0], edge[1][1] - c_node[1])
            ang1 = cal_angle(node1)
            ang2 = cal_angle(node2)
            if ang1 > ang2:
                node1, node2 = swap(node1, node2)
                ang1, ang2 = swap(ang1, ang2)

            if curr_ang >= ang1 and curr_ang <= ang2:
                curr_dis = min(curr_dis, cal_dis(node1, node2, curr_ang))
        tot_display.append(curr_dis) 

running = True

update()

while running:
    fov_scale = 0
    fov_scale = pygame.surface.Surface((720, 30))
    for i in range(fov_start, fov_start-720, -1):
        if i < 0:
            deg = i + 1440
        else:
            deg = i
        color_value = int(255 / (tot_display[deg] + 1))
        color = (color_value, color_value, color_value)
        line_rect = Rect(deg, 0, 1, 30)
        pygame.draw.rect(fov_scale, color, line_rect)

    screen.blit(fov_scale, (0, 0))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    key_list = pygame.key.get_pressed()  
    if key_list[pygame.K_RIGHT]: 
        c_node[0] += 0.01
        # fov_start -= 1
        print(c_node)
        update()
    elif key_list[pygame.K_LEFT]:
        c_node[0] -= 0.01
        # fov_start += 1
        update()
        print(c_node)








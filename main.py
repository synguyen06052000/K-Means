

import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def create_text_render(string):
    font = pygame.font.SysFont('san', 40)
    return font.render(string, True, WHITE)
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]-p2[1]) * (p1[1]-p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("K-Means")

running=True

clock = pygame.time.Clock()


font = pygame.font.SysFont('san', 40)
font_small = pygame.font.SysFont('san', 15)

BACKGROUND = (214,214,214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249,255,230)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

K = 0
error = 0
points = []
clusters = []
labels = []


while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #vẽ panel

    pygame.draw.rect(screen, BLACK, (50,50,700,500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))

    # Nút điều khiển K

    pygame.draw.rect(screen, BLACK, (850,50,50,50))
    screen.blit(create_text_render("+"), (865,60))

    pygame.draw.rect(screen, BLACK, (950,50,50,50))
    screen.blit(create_text_render("-"), (965,60))

    #Bien K
    font = pygame.font.SysFont('san', 40)
    text_k = font.render("K = " + str(K), True, BLACK )
    screen.blit(text_k, (1050,60))


    # Nut Run

    pygame.draw.rect(screen, BLACK, (850,150,150,50))
    screen.blit(create_text_render("Run"), (900,160))

    # Nut Random
    pygame.draw.rect(screen, BLACK, (850,250,150,50))
    screen.blit(create_text_render("Random"), (880,260))

    # Nut Algorithm

    pygame.draw.rect(screen, BLACK, (850,450,150,50))
    screen.blit(create_text_render("Algorithm"), (860,460))

    #Bien Error
    # font = pygame.font.SysFont('san', 40)
    # text_error = font.render("Error = " + str(int(error)), True, BLACK )
    # screen.blit(text_error, (850,350))

    # Nut Reset

    pygame.draw.rect(screen, BLACK, (850,550,150,50))
    screen.blit(create_text_render("Reset"), (880,560))

    #Xử lý nút bấm

    #Ve toa do chuot khi chuot o pannel

    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            #Vẽ diem vao giao dien:
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x-50, mouse_y-50]
                points.append(point)
 
            #Nhan K+
            if 850 < mouse_x <900 and 50 < mouse_y <100:
                if K < 8:
                    K += 1

            #Nhan K-
            if 950 < mouse_x <1000 and 50 < mouse_y <100:
                if K>0:
                    K -=1
                
            #Nut Run
            if 850 < mouse_x <1000 and 150 < mouse_y <200:
                labels = []
                if clusters == []:
                    continue
                #Gan diem vao cluster gan nhat 
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        distance_pc = distance(p,c)
                        distances_to_cluster.append(distance_pc)

                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance)
                    labels.append(label)

                #Thay doi vi tri cluster
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    
                    if count != 0:
                        new_cluster_x = sum_x / count
                        new_cluster_y = sum_y / count
                        clusters[i] = [new_cluster_x, new_cluster_y]
                            

            #Nut ramdom
            if 850 < mouse_x <1000 and 250 < mouse_y <300:
                labels = []
                clusters = []
                for i in range(K):
                    random_point = [randint(0, 700), randint(0, 500)]
                    clusters.append(random_point)
            #Nut Reset
            if 850 < mouse_x <1000 and 550 < mouse_y < 600:
                K = 0
                error = 0
                points = []
                clusters = []
                labels = []

            # Nut Algorithm
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters=K).fit(points)
                labels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_
                print("Algorithm")
    #Ve cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)
    #Ve diem
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 50, points[i][1] +50), 6)

        if labels == []:
            pygame.draw.circle(screen, WHITE, (points[i][0] + 50, points[i][1] +50), 5)
        else :
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] +50), 5)
    
    # Tinh error:
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])
    text_error = font.render("Error = " + str(int(error)), True, BLACK)
    screen.blit(text_error, (850,350))

    pygame.display.flip()
    
pygame.quit()
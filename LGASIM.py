import pygame
import random
from sys import exit
from collections import defaultdict

# Funkcja do obsługi kolizji
def collision(particles, p_m, cell_size):
    # Zbudowanie siatki bez modyfikacji w trakcie iteracji
    grid = defaultdict(list)
    for i, (x, y) in enumerate(particles):
        grid[(x // cell_size, y // cell_size)].append(i)

    # Iteracja przez komórki siatki
    for cell, indices in grid.items():
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                idx1, idx2 = indices[i], indices[j]
                # Sprawdzanie kolizji cząstek w tej samej komórce
                if (particles[idx1][0] // cell_size == particles[idx2][0] // cell_size and
                        particles[idx1][1] // cell_size == particles[idx2][1] // cell_size):
                    # Zderzenie czołowe
                    if (p_m[idx1] == [1, 0] and p_m[idx2] == [-1, 0]) or (p_m[idx1] == [-1, 0] and p_m[idx2] == [1, 0]):
                        p_m[idx1], p_m[idx2] = [0, 1], [0, -1]  # Zmiana na dół/góra
                    elif (p_m[idx1] == [0, 1] and p_m[idx2] == [0, -1]) or (p_m[idx1] == [0, -1] and p_m[idx2] == [0, 1]):
                        p_m[idx1], p_m[idx2] = [1, 0], [-1, 0]  # Zmiana na prawo/lewo

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Lattice Gas Automaton')
clock = pygame.time.Clock()

# możliwe ruchy (góra, lewo, dół, prawo)
streaming = [[1, 0], [0, -1], [-1, 0], [0, 1]]
num_of_particles = 4000  # Więcej cząsteczek do testów
particles = []

for _ in range(num_of_particles):
    particles.append([random.randint(0, 149), random.randint(0, 799)])
p_m = []

for i in range(num_of_particles):
    p_m.append(streaming[random.randint(0, 3)].copy())

def wall_collision():
    for i in range(num_of_particles):
        particles[i][0] += p_m[i][0]
        particles[i][1] += p_m[i][1]

        # Kolizja ze ścianami przed sprawdzeniem kolizji między cząstkami
        if 145 <= particles[i][0] <= 154 and (particles[i][1] < 360 or particles[i][1] > 440):
            p_m[i][0] *= -1
            particles[i][0] += p_m[i][0]  # Cofnij ruch

        # Kolizja z krawędziami ekranu
        if particles[i][0] <= 5 or particles[i][0] >= 798:
            p_m[i][0] *= -1
        if particles[i][1] <= 5 or particles[i][1] >= 798:
            p_m[i][1] *= -1

# ściany
wall_1 = pygame.Surface((4, 360))
wall_2 = pygame.Surface((4, 360))
wall_1.fill('Red')
wall_2.fill('Red')

test_surface = pygame.Surface((3, 3))
test_surface.fill('Lime')

cell_size = 3
fps_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if fps_list:
                avg_fps = sum(fps_list) / len(fps_list)
                print(f"Average FPS: {avg_fps:.2f}")
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    # rysowanie ścian
    screen.blit(wall_1, (150, 0))
    screen.blit(wall_2, (150, 440))

    wall_collision()

    # kolizja cząstek
    collision(particles, p_m, cell_size)

    # wyświetlanie cząstek
    for i in range(num_of_particles):
        screen.blit(test_surface, (particles[i][0], particles[i][1]))

    pygame.display.update()
    fps = clock.get_fps()  # oblicz FPS
    fps_list.append(fps)  # zapisz FPS do listy
    ##print(f"Current FPS: {fps:.2f}")  # opcjonalne, pokazuje FPS w czasie rzeczywistym
    clock.tick(120)

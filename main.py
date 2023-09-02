import pygame
import sys
import random
import math


def generate_color_set():
    colors = [(255, 0, 0), (255, 255, 255), (255, 0, 255)]
    return random.choice(colors)


def create_circle(radius):
    x = random.randint(radius, screen_width - radius)
    y = random.randint(radius, screen_height - radius)
    color = generate_color_set()
    angle = random.uniform(5, 10)
    speed = random.uniform(1, 3)

    return {
        'position': (x, y),
        'radius': radius,
        'color': color,
        'angle': angle,
        'speed': speed
    }


def move_circles():
    for circle in circles:
        x, y = circle['position']
        angle = circle['angle']
        speed = circle['speed']
        x += speed * math.cos(angle)
        y += speed * math.sin(angle)
        circle['position'] = (x, y)

        if x + circle['radius'] >= screen_width or x - circle['radius'] <= 0:
            angle = math.pi - angle
        if y + circle['radius'] >= screen_height or y - circle['radius'] <= 0:
            angle = -angle
        circle['angle'] = angle


def detect_collisions():
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            circle1 = circles[i]
            circle2 = circles[j]
            distance = math.sqrt((circle1['position'][0] - circle2['position'][0]) ** 2 + (
                    circle1['position'][1] - circle2['position'][1]) ** 2)

            if distance < circle1['radius'] + circle2['radius']:
                color1 = circle1['color']
                color2 = circle2['color']

                match (color1, color2):
                    case (255, 0, 0), (255, 255, 255):
                        circle1['color'] = (255, 0, 0)
                        circle2['color'] = (255, 0, 0)
                    case (255, 255, 255), (255, 0, 0):
                        circle1['color'] = (255, 0, 0)
                        circle2['color'] = (255, 0, 0)
                    case (255, 255, 255), (255, 0, 255):
                        circle1['color'] = (255, 255, 255)
                        circle2['color'] = (255, 255, 255)
                    case (255, 0, 255), (255, 255, 255):
                        circle1['color'] = (255, 255, 255)
                        circle2['color'] = (255, 255, 255)
                    case (255, 0, 0), (255, 0, 255):
                        circle1['color'] = (255, 0, 0)
                        circle2['color'] = (255, 0, 0)
                    case (255, 0, 255), (255, 0, 0):
                        circle1['color'] = (255, 0, 0)
                        circle2['color'] = (255, 0, 0)
                    case _:
                        pass

                angle1 = math.atan2(circle1['position'][1] - circle2['position'][1],
                                    circle1['position'][0] - circle2['position'][0])
                angle2 = math.atan2(circle2['position'][1] - circle1['position'][1],
                                    circle2['position'][0] - circle1['position'][0])
                circle1['angle'] = angle1
                circle2['angle'] = angle2


def music_player(playerStatus):
    match playerStatus:
        case False:
            pygame.mixer.music.stop()
        case _:
            pygame.mixer.init()
            pygame.mixer.music.load("assets/song.mp3")
            pygame.mixer.music.play(-1)


pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
music_player(True)

print('Enter number of balls: ')
numberOfBalls = int(input())
circles = []

for _ in range(numberOfBalls):
    circles.append(create_circle(20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            music_player(False)
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    move_circles()
    detect_collisions()

    all_same_color = all(circle['color'] == circles[0]['color'] for circle in circles)

    if all_same_color:
        pygame.time.delay(2000)
        screen.fill(circles[0]['color'])
        pygame.display.flip()
        music_player(False)
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    for circle in circles:
        x, y = circle['position']
        radius = circle['radius']
        color = circle['color']
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)

    pygame.display.flip()
    clock.tick(60)

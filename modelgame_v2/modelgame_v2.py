import pygame
import random
import time

WIDTH = 960  # ширина игрового окна
HEIGHT = 840 # высота игрового окна
FPS = 30 # частота кадров в секунду


MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 255, 255)
DARKBLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

x1 = 125 
y1 = 125




class Rectangle():
    def __init__(self, screen, color, x_position, y_position, height, weight, max_random):
        self.max_random = max_random
        self.rand_movement = 0
        self.mov = 0
        self.gen = 1
        self.w0 = 0.25
        self.w1 = 0.25
        self.w2 = 0.25
        self.w3 = 0.25
        self.screen = screen
        self.color = color
        self.x_position = x_position
        self.y_position = y_position
        self.height = height
        self.weight = weight
        self.dist_for_gen = []

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x_position, self.y_position, self.height, self.weight])

    def change_position(self):
        if self.rand_movement == 0:
            self.x_position += -10 
            self.y_position += 0
        elif self.rand_movement == 1:
            self.x_position += 10
            self.y_position += 0
        elif self.rand_movement == 2:
            self.y_position += -10
            self.x_position += 0
        elif self.rand_movement == 3:
            self.y_position += 10
            self.x_position += 0

    def dist_gg_target(self):
        self.x_gg = self.x_position + 7
        self.y_gg = self.y_position + 7
        self.distance = ((self.x_gg - 365)**2 + (self.y_gg - 365)**2)**0.5
        return self.distance

    def is_hero_go_to_wall(self, x_position, y_position):
        if (x_position < 100):
            self.x_position += 10
        if (y_position < 100):
            self.y_position += 10
        if (x_position > 400):
            self.x_position -= 10
        if (y_position > 400):
            self.y_position -= 10

    def is_push_green(self):
        x2 = self.x_position + 15
        y2 = self.y_position + 15
        x_list = []
        y_list = []
        for i in range(self.x_position, x2+1):
            x_list.append(i)
        for i in range(self.y_position, y2+1):
            y_list.append(i)
        for x in x_list:
            if abs(x - 365) <= 5:
                for y in y_list:
                    if abs(y - 365) <= 5:
                        self.x_position = 125
                        self.y_position = 125
                        self.dist_for_gen.append(-11000)
                        return True

    def model(self):
        self.draw()
        self.mov += 1
        self.dist_for_gen.append(self.dist_gg_target())
        self.rand_movement = self.choice_of_w()
        self.is_hero_go_to_wall(self.x_position, self.y_position)
        self.is_push_green()
        self.change_position()
        if self.mov >= 1000:
            self.y_position = 125
            self.x_position = 125
            self.last_gen_loss = self.f_loss()
            print(f"generation: {self.gen} color {self.color} loss: {self.last_gen_loss}")
            self.gen += 1
            self.dist_for_gen = []
            self.mov = 0
            if self.last_gen_loss < 75:
                for i in range(100):
                    print(f'{self.color} wins  with score {self.last_gen_loss}')



    def choice_of_w(self):
        n = random.randint(1, 100)
        zero_w0 = []
        w0_w1 = []
        w1_w2 = []
        w2_w3 = []
        for i in range(1, int(self.w0*100+1)):
            zero_w0.append(i)
        for j in range(int(self.w0*100+1), int((self.w0+self.w1) * 100) + 1):
            w0_w1.append(j)
        for j in range(int((self.w0+self.w1) * 100) + 1, int((self.w0+self.w1+ self.w2) * 100) + 1):
            w1_w2.append(j)
        for j in range(int((self.w0+self.w1+ self.w2) * 100) + 1, int((self.w0+self.w1+self.w2+self.w3) * 100) + 1):
            w2_w3.append(j)
        if n in zero_w0:
            return 0
        elif n in w0_w1:
            return 1
        elif n in w1_w2:
            return 2
        elif n in w2_w3:
            return 3
    
    def mix_weights(self):
        random_w = [self.w0, self.w1, self.w2, self.w3]
        random.shuffle(random_w)
        first_change = random.randint(0, self.max_random)
        second_change = random.randint(0, self.max_random)
        random_w[0] = random_w[0] + (first_change * 0.01)
        random_w[1] = random_w[1] + (second_change * 0.01)
        random_w[2] = random_w[2] + (-(first_change) * 0.01)
        random_w[3] = random_w[3] + (-(second_change) * 0.01)
        print(random_w)
        self.w0 = random_w[0]
        self.w1 = random_w[1]
        self.w2 = random_w[2]
        self.w3 = random_w[3]


    def f_loss(self):
        self.loss = sum(self.dist_for_gen) / 1000
        if self.gen > 1:
            if self.last_gen_loss <= self.loss:
                self.w0 = self.w0_best
                self.w1 = self.w1_best
                self.w2 = self.w2_best
                self.w3 = self.w3_best
 #               print(self.best_gen_loss, 'last_gen_loss <= loss')
 #               print(self.w0, self.w1, self.w2, self.w3)
            elif self.last_gen_loss > self.loss and self.best_gen_loss > self.loss:
                self.best_gen_loss = self.loss

                self.w0_last = self.w0
                self.w1_last = self.w1
                self.w2_last = self.w2
                self.w3_last = self.w3
                           
                self.w0_best = self.w0
                self.w1_best = self.w1
                self.w2_best = self.w2
                self.w3_best = self.w3

                try:
                    self.mix_weights()
                except:
                    pass
#                print(self.best_gen_loss, '  last_gen_loss > loss and best_gen_loss > loss')
#                print(self.w0, self.w1, self.w2, self.w3)

            elif self.last_gen_loss > self.loss and self.best_gen_loss <= self.loss:
                try:
                    self.mix_weights()
                except:
                    pass
#                print(self.best_gen_loss, '  last_gen_loss > loss and best_gen_loss <= loss')

        if self.gen == 1:
            self.best_gen_loss = self.loss
        
            self.w0_last = self.w0
            self.w1_last = self.w1
            self.w2_last = self.w2
            self.w3_last = self.w3
            
            try:
                self.mix_weights()
            except:
                pass
 #           print(self.best_gen_loss)

            self.w0_best = self.w0
            self.w1_best = self.w1
            self.w2_best = self.w2
            self.w3_best = self.w3
 #           print(self.w0, self.w1, self.w2, self.w3)
        return self.loss



class Wall():
    def __init__(self, screen, color, start, finish, width):
        self.screen = screen
        self.color = color
        self.start = start
        self.finish = finish
        self.width = width

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.start, self.finish, self.width)



# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
screen.fill(WHITE)
pygame.display.flip()
clock = pygame.time.Clock()
# Цикл игры
running = True

wall1 = Wall(screen, RED, (100, 100), (100, 400), 5)
wall2 = Wall(screen, RED, (100, 100), (400, 100), 5)
wall3 = Wall(screen, RED, (100, 400), (400, 400), 5)
wall4 = Wall(screen, RED, (400, 400), (400, 100), 5)

rect1 = Rectangle(screen, BLACK, 125, 125, 15, 15, 1)
rect2 = Rectangle(screen, RED, 250, 250, 15, 15, 3)
rect3 = Rectangle(screen, BLUE, 125, 125, 15, 15, 7)
rect4 = Rectangle(screen, DARKBLUE, 250, 250, 15, 15, 12)
rect5 = Rectangle(screen, ORANGE, 125, 125, 15, 15, 20)
rect6 = Rectangle(screen, MAGENTA, 250, 250, 15, 15, 30)

while running:
   
    # Ввод процесса (события)
    # Обновление
    
    # Визуализация (сборка)
    for event in pygame.event.get():
    # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                x1 += -10 #
                y1 += 0
            elif event.key == pygame.K_RIGHT:
                x1 += 10
                y1 += 0
            elif event.key == pygame.K_UP:
                y1 += -10
                x1 += 0
            elif event.key == pygame.K_DOWN:
                y1 += 10
                x1 += 0
    
    screen.fill(WHITE)

    wall1.draw()
    wall2.draw()
    wall3.draw()
    wall4.draw()
    pygame.draw.rect(screen, GREEN, [360, 360, 10, 10])
    rect1.model()
    rect2.model()
    rect3.model()
    rect4.model()
    rect5.model()
    rect6.model()
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()

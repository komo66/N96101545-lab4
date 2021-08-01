import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center_x,self.center_y = center
        self.radius = radius

    def collide(self, enemy):
        #calculate the distance between the tower and the enemy
        ax,ay=self.center_x,self.center_y
        bx,by=enemy.get_pos()
        distance=math.sqrt((ax-bx)**2+(ay-by)**2)
        if distance<=self.radius:
            return True
        else:
            return False

        

    def draw_transparent(self, win):
        #use draw.circle to draw the range of the towers
        surface=pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA)
        pygame.draw.circle(surface,(128,128,128,100),(self.radius,self.radius),self.radius)
        win.blit(surface,(self.center_x-self.radius,self.center_y-self.radius))

class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        
        if self.cd_count <= self.cd_max_count :
             self.cd_count+=1
             return False
        else: 
            self.cd_count=0
            return True
    

    def attack(self, enemy_group):
        #judge whether it is cool down
        if self.is_cool_down()==False:
            return 0
        #determine if the enemy is within range   
        for enemy in enemy_group.get():
            if self.range_circle.collide(enemy):
                enemy.get_hurt(self.damage)
                return 0


    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        rect_x=self.rect.x
        rect_y=self.rect.y
        rect_width=self.rect.w
        rect_height=self.rect.h
        if rect_x<x<(rect_x+rect_width) and rect_y<y<(rect_y+rect_height):
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower


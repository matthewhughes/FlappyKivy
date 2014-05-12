from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scatter import Scatter
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint
import sys

class Obstacle(Widget):
    gap = NumericProperty(0)
    gap_height = NumericProperty(200)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    marked = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
    
    def update_position(self):
        self.gap = randint(self.gap_height, self.height)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Player(Widget):
    acceleration =  0.2
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def on_touch_down(self, touch):
        self.velocity_y = 5
    
    def update(self):
        if (self.velocity_y > -8):
            self.velocity_y -= self.acceleration
        self.pos = Vector(*self.velocity) + self.pos
            
class JumpGame(FloatLayout):
    player = ObjectProperty(None)
    obstacles = ListProperty([])
    points = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(JumpGame, self).__init__(**kwargs)
        self.player.velocity = [0, 0]
        
    def update(self, dt):    
        self.player.update()
        if self.player.y <= 0:
            self.reset()
        for obstacle in self.obstacles:
            if obstacle.x+25 < self.player.x+25 and not obstacle.marked:
                self.points +=1
                self.player.acceleration = self.player.acceleration + 0.01
                obstacle.marked = True
                if self.player.y < obstacle.gap - obstacle.gap_height or self.player.y > obstacle.gap-50:
                    self.reset()       
            if obstacle.x < 0:
                self.remove_obstacle()
            obstacle.move()
            
    def reset(self):
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        self.obstacles = []
        self.points = 0
        self.player.velocity_y = 10

    def remove_obstacle(self):
        self.remove_widget(self.obstacles[0])
        self.obstacles = self.obstacles[1:]

    def new_obstacle(self, remove = True):
        new_obstacle = Obstacle()
        new_obstacle.height = self.height
        new_obstacle.x = self.width
        new_obstacle.update_position()
        new_obstacle.velocity = [-3, 0]
        self.add_widget(new_obstacle)
        self.obstacles = self.obstacles + [new_obstacle]
        

class JumpApp(App):
    def build(self):
        game = JumpGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        Clock.schedule_interval(game.new_obstacle, 2)
        return game
    
if __name__ == '__main__':
    JumpApp().run()

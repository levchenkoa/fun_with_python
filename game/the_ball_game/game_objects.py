from .support import *
import math
from tkinter import PhotoImage

class GameObject(object):
    """Base class for all Game objects"""
    def __init__(self, canvas, cursor):
        self.canvas = canvas
        self.draw_figure()
       

    def __init_geometry_fields__(self):
        self.r = rnd_new_radius()
        self.x = rnd_new_center_x(self.canvas, self.r)
        self.y = rnd_new_center_y(self.canvas, self.r)
        self.color = rnd_color()
        self.angle = rnd_new_angel(0, 360)
        

    def draw_figure(self):
        self.figure = self.get_figure()
        self.canvas.tag_raise(self.figure)
    
    def get_figure(self):
        raise NotImplementedError()

class Star(GameObject):
    def __init__(self, canvas):
        self.cost = 10
        self.speed = 3
        GameObject.__init__(self, canvas, "heart")

    def get_figure(self):
        """Retrun a specific canvas object """
        return self.canvas.create_polygon((0, 0), outline='black', width=3)

    def draw_shadow(self, coords):
        """Return a shadow-stamp for click event"""
        return self.canvas.create_polygon(coords, fill='lightgrey', width=0)

    def calculate_figure_coords(self, angle=18):
        """Calculate the Star coords"""
        points = []
        for i in range(10):
            aRad = math.radians(angle)
            cos_a = math.cos(aRad)
            sin_a = math.sin(aRad)
            if i % 2 == 0:
                tmp_x = self.x + self.r*cos_a
                tmp_y = self.y - self.r*sin_a
            else:
                tmp_x = self.x + self.r/2*cos_a
                tmp_y = self.y - self.r/2*sin_a
            points.append(tmp_x)
            points.append(tmp_y)
            angle += 36
        return points
 
class Ball(GameObject):
    def __init__(self, canvas):
        self.cost = 5
        self.speed = 1
        GameObject.__init__(self, canvas, "cross")



    def get_figure(self):
        return self.canvas.create_oval(0, 0, 0, 0,width=4)

    def draw_shadow(self, coords):
        return self.canvas.create_oval(coords, fill='lightgrey', width=0)
    
    def calculate_figure_coords(self):
        return [self.x-self.r, self.y - self.r, self.x+self.r, self.y+self.r]

class Scope(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.scope_field = PhotoImage(
            file=os.path.join(get_location(), 'unicorn_on_field.png'))
        self.scope_on_target = PhotoImage(
            file=os.path.join(get_location(), 'unicorn_on_target.png'))
        self.x = -200
        self.y = -200
        self.on_target = False
        self.scope = self.canvas.create_image(self.x, self.y,anchor = 'nw')
        self.canvas.bind('<Motion>', lambda event: self.motion_handler(event))
        self.canvas.bind('<Button-1>', lambda event: self.click_handler(event))
        self.canvas.configure(cursor='none')

    def set_engine(self, engine):
        self.engine = engine

    def set_on_filed(self):
        self.on_target = False
        self.canvas.itemconfigure(self.scope, image=self.scope_field)

    def set_on_target(self):
        self.on_target = True
        self.canvas.itemconfigure(self.scope, image=self.scope_on_target)

    def motion_handler(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.coords(self.scope, self.x, self.y)
        

    def click_handler(self, event):
       self.engine.scope_click_handler()
import math
from random import randint as rnd
import  os

def get_location():
     return os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def rnd_color():
    r = rnd(0, 255)
    g = rnd(0, 255)
    b = rnd(0, 255)
    color = "#%02X%02X%02X" % (r, g, b)
    return color


def calculate_distance_from_point_to_point(from_x, from_y, to_x, to_y):

    return math.sqrt(
        (from_x-to_x)**2 + (from_y-to_y)**2)


def rnd_new_angel(min_angle=0, max_angle=360):
    """return random angle degree from 0 to 360"""
    return rnd(min_angle, max_angle)


def rnd_new_radius(min_radius=30, max_radius=50):
    """return random radius for game object"""
    return rnd(min_radius, max_radius)


def rnd_new_center_x(canvas, radius):
    """return random x coordinate value depends by canvas size"""
    return rnd(0+radius, canvas.winfo_width()-radius)


def rnd_new_center_y(canvas, radius):
    """return random y coordinate value depends by canvas size"""
    return rnd(0+radius, canvas.winfo_height()-radius)

def calculate_new_direction_point(game_object):
    aRad = math.radians(game_object.angle)
    x1 = game_object.x + game_object.r * math.cos(aRad)
    y1 = game_object.y - game_object.r * math.sin(aRad)
    return x1, y1

def get_center(game_obj):
    """return center of game object"""
    coords = game_obj.canvas.coords(game_obj.figure)
    x = 0
    y = 0 
    if len(coords)<=4:
        x = coords[0]+game_obj.r
        y = coords[1]+game_obj.r
        return x,y
    #TODO Fix it
    a_x = coords[0]
    a_y = coords[1]
    b_x = coords[10]
    b_y = coords[11]
    c_x = coords[2]
    c_y = coords[3]
    d_x = coords[12]
    d_y = coords[13]
    x=-((a_x*b_y-b_x*a_y)*(d_x-c_x)-(c_x*d_y-d_x*c_y)*(b_x-a_x))/((a_y-b_y)*(d_x-c_x)-(c_y-d_y)*(b_x-a_x))
    y=((c_y-d_y)*(-x)-(c_x*d_y-d_x*c_y))/(d_x-c_x)

    return x, y

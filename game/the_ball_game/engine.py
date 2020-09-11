from .support import *

class GameEngine(object):
    def __init__(self, canvas, scope, *game_objects):
        self.score = 0
        self.all_game_objects = game_objects
        self.scope = scope
        self.scope.set_engine(self)
        self.canvas = canvas
        self.try_to_put_objects_on_field()

    def get_qty_objects(self):
        qty = 0
        for game_objects_list in self.all_game_objects:
            qty+=len(game_objects_list)
        return qty

    def motion(self):
        self.scope.set_on_filed()
        for game_objects_list in self.all_game_objects:
            for game_object in game_objects_list:
                game_object_center = get_center(game_object)
                game_object_radius = game_object.r
                self.main_handler_scope(game_object_center,game_object_radius,game_object,game_objects_list)
                self.check_touch_figure(game_object_center,game_object_radius,game_object, game_objects_list)
                self.check_touch_wall(game_object_center,game_object_radius, game_object)
                self.canvas.move(
                    game_object.figure, ((game_object.direction_point[0]-game_object.x)/game_object_radius)*game_object.speed, ((game_object.direction_point[1]-game_object.y)/game_object_radius)*game_object.speed)
       

    def main_handler_scope(self,game_object_center,game_object_radius,game_object,game_objects_list):
        if calculate_distance_from_point_to_point(game_object_center[0], game_object_center[1], self.scope.x, self.scope.y) <= game_object_radius:
                    self.game_objects_list = game_objects_list
                    self.game_object = game_object
                    self.scope.set_on_target()   

    def scope_click_handler(self):
        if self.scope.on_target:
            self.click(self.game_object, self.game_objects_list)
        


    def try_to_put_objects_on_field(self):
        for game_objects_list in self.all_game_objects:
            for game_object in list(game_objects_list):
                game_object.__init_geometry_fields__()      
                if not self.check_figure_intersection((game_object.x,game_object.y),game_object.r, game_object, game_objects_list):
                    coords = game_object.calculate_figure_coords()
                    self.canvas.coords(game_object.figure, coords)
                    self.canvas.itemconfigure(game_object.figure, fill=game_object.color)
                    game_object.direction_point = calculate_new_direction_point(game_object)
                else:
                    self.canvas.delete(game_object.figure)
                    game_objects_list.remove(game_object)



    def check_figure_intersection(self, center_of_game_object, raidus_game_object,game_object, game_objects_list): # TODO Need to fix
        result = None
        for another_game_object in game_objects_list:
            if another_game_object is game_object:
                continue
            try:
                center_of_another_game_object = get_center(another_game_object)
            except:
                return result

            distance = calculate_distance_from_point_to_point(center_of_game_object[0], center_of_game_object[1],
                                                              center_of_another_game_object[0], center_of_another_game_object[1])
            if distance <= raidus_game_object+ another_game_object.r:  # TODO Need to fix
                result = another_game_object
        return result

   
    def click(self, game_object, game_objects_list):
        coords = self.canvas.coords(game_object.figure)
        shadow = game_object.draw_shadow(coords)
        self.canvas.tag_lower(shadow)
        self.canvas.delete(game_object.figure)
        self.score+=game_object.cost
        game_objects_list.remove(game_object)
        self.scope.set_on_filed()

    def check_touch_figure(self,game_object_center,game_object_radius, game_object, game_objects_list):
        another_game_object = self.check_figure_intersection(game_object_center,game_object_radius,
            game_object, game_objects_list)
        if another_game_object != None:
            self.figures_rebound(game_object, another_game_object)

    def figures_rebound(self, game_object, another_game_object):
        game_object.x, game_object.y = get_center(game_object)
        another_game_object.x, another_game_object.y = get_center(another_game_object)
        
        game_object.angle, another_game_object.angle = another_game_object.angle, game_object.angle
        game_object.direction_point = calculate_new_direction_point(
            game_object)
        another_game_object.direction_point = calculate_new_direction_point(
            another_game_object)

    def wall_bounce(self, angle, game_object):
        game_object.x, game_object.y = get_center(game_object)
        game_object.angle = rnd_new_angel(angle[0], angle[1])
        game_object.direction_point = calculate_new_direction_point(
            game_object)

    def check_touch_wall(self, center_point, radius,game_object):
        new_angle = None
        if self.is_touch_up(center_point[1]-radius, 0):
            new_angle = (180, 360)
        elif self.is_touch_right(center_point[0]+radius, self.canvas.winfo_width()):
            new_angle = (90, 270)
        elif self.is_touch_down(center_point[1]+radius, self.canvas.winfo_height()):
            new_angle = (0, 180)
        elif self.is_touch_left(center_point[0]-radius, 0):
            new_angle = (270, 450)
        if new_angle != None:
                self.wall_bounce(new_angle, game_object)
                

    def is_touch_up(self, y_obj, y_obstacle):
        return y_obj <= y_obstacle

    def is_touch_right(self, x_obj, x_obstacle):
        return x_obj >= x_obstacle

    def is_touch_left(self, x_obj, x_obstacle):
        return x_obj <= x_obstacle

    def is_touch_down(self, y_obj, y_obstacle):
        return y_obj >= y_obstacle

from .support import get_location
from tkinter import Tk, Frame, Canvas, messagebox, Label, Toplevel, Entry, Button
from tkinter.constants import *
from .game_objects import Ball, Star, Scope
from .engine import *
from random import choice
import csv


class InputNameDiaolog:
    """Enter name if the player scored the number of points needed to qualify for the Top"""
    def __init__(self, parent):
        color = rnd_color()
        top = self.top = Toplevel(parent)
        self.__set_geomtry(parent, top, 350, 150,
                           "*****You are TOP!*****", color)
        self.myLabel = Label(top, text='Enter your name!',
                             font='Arial 25', bg=color)
        self.myLabel.pack()
        self.myEntryBox = Entry(top, font='Arial 25', bg=color)
        self.myEntryBox.bind('<Return>', lambda event: self.send())
        self.myEntryBox.pack()
        self.mySubmitButton = Button(
            top, text='Ok', command=self.send, font='Arial 25', bg=color, width=6)
        self.mySubmitButton.pack()

    def __set_geomtry(self, parent, top, width, height, title, color):
        top.configure(bg=color)
        top.title(title)
        top.resizable(False, False)
        parent_hw, parent_x, parent_y = parent.geometry().split('+')
        parent_h, parent_w = (int(value) for value in parent_hw.split('x'))
        x = int(parent_x) + (parent_w+width)//2
        y = int(parent_y) + (height*2)
        top.geometry(f'{width}x{height}+{x}+{y}')
        top.focus_set()
        top.wait_visibility()
        top.grab_set()

    def send(self):
        self.username = self.myEntryBox.get()
        self.top.destroy()


class ScoreControl():
    """Score controller class for showing best players, save result to file and load results"""
    def __init__(self, filename, canvas):

        csv.register_dialect('players', delimiter=';')
        self.__filename = os.path.join(get_location(), filename)
        self.__canvas = canvas
        self.__players = self.__load_players(self.__filename)
        self.__show_top_players()

    def __sort_players(self):
        """Sort dictonary with players"""
        self.__players.sort(key=lambda i: int(i['score']))
        self.__players.reverse()
        self.__players = self.__players[:10]

    def __load_players(self, filename):
        """Load dictonary from csv file"""
        players = []
        try:
            with open(filename, "r", encoding='utf-8', newline="") as file:
                reader = csv.DictReader(file, dialect='players')
                for row in reader:
                    players.append(
                        {'name': row['name'], 'score': int(row['score'])})
        except:
            pass
        return players[:10]

    def __save_players(self, filename, players):
        """Save dictonary with players to csv file"""
        with open(filename,  "w", encoding='utf-8', newline="") as file:
            columns = ["name", "score"]
            writer = csv.DictWriter(
                file, fieldnames=columns, dialect='players')
            writer.writeheader()
            writer.writerows(players)

    def add_player(self, name, score):
        """Adding a new top player and save data"""
        self.__players.append({'name': name, 'score': score})
        self.__sort_players()
        self.__save_players(self.__filename, self.__players[:10])
        self.__show_top_players()

    def get_min_value(self):
        """Getting the minimum score from top playres"""
        self.__sort_players()
        min_score = 0
        if len(self.__players) == 0:
            return min_score
        return self.__players[-1]['score']

    def __show_top_players(self, x=10, y=10):
        """Show players at canvas"""
        self.__sort_players()
        self.__canvas.delete(ALL)
        scores_name = ''
        scores_value = ''

        for index in range(10):
            try:
                scores_name += f"{index+1:02}. {self.__players[index]['name']:<10}\n"
                scores_value += f"{self.__players[index]['score']:>4}\n"
            except:
                scores_name += f"{index+1:02}.-------------------\n"

        color = rnd_color()
        self.__canvas.create_text(x+15, y, text='TOP PLAYERS',
                                  fill=color, font='Arial 25', anchor='nw')
        self.__canvas.create_text(x, y+50, text=scores_name,
                                  fill=color, font='Arial 25', anchor='nw')
        self.__canvas.create_text(x+200, y+50, text=scores_value,
                                  fill=color, font='Arial 25', anchor='nw')


class UnicornGame(object):
    """Main game class"""
    def __init__(self):

        root = self.root = Tk()
        root.bell()
        root.geometry('1200x600')
        root.title('Crazy unicorn!')
        field_frame = self.field_frame = Frame(relief=RIDGE, borderwidth=2)
        scrore_frame = self.scrore_frame = Frame(relief=RIDGE, borderwidth=2)
        field_frame.pack(side=RIGHT, fill=BOTH, expand=1)
        scrore_frame.pack(side=LEFT, fill=BOTH)
        field_canvas = self.field_canvas = Canvas(
            field_frame, width=800, height=600, bg=rnd_color())
        field_canvas.pack(fill=BOTH, expand=1)
        field_canvas.update()
        score_canvas = self.score_canvas = Canvas(
            scrore_frame, width=300, height=450, bg=rnd_color())
        score_canvas.pack(fill=BOTH, expand=1)
        score_canvas.update()
        stats_canvas = self.stats_canvas = Canvas(
            scrore_frame, width=300, height=150, bg=rnd_color())
        stats_canvas.pack(fill=BOTH)
        stats_canvas.update()
        self.__round_text = stats_canvas.create_text(
            10, 10, fill=rnd_color(), font='Arial 24', anchor='nw')
        self.__timer_text = stats_canvas.create_text(
            10, 50, fill=rnd_color(), font='Arial 24', anchor='nw')
        self.__score_text = stats_canvas.create_text(
            10, 90, fill=rnd_color(), font='Arial 24', anchor='nw')
        self.__timer = 0
        self.__round_counter = 1
        self.score_controller = ScoreControl(
            "unicorn_players.csv", score_canvas)

    def start_game(self):
        """Main method to start game"""
        self.root.after(200, self.__ask_start)

        self.__mainloop()

    def __ask_start(self):
        answer = messagebox.askquestion(
            'Hello!', 'Welcome to the Crazy unicorn game!\nWould you like to play?', parent=self.field_frame)
        if answer == messagebox.YES:
            self.__new_game = self.__buld_game(self.field_canvas)
            self.__run()
        else:
            self.root.destroy()

    def __mainloop(self):
        self.root.mainloop()

    def __buld_game(self, canvas):
        game_object_types_one = [Star]
        game_object_types_two = [Ball]
        game_objects_list_one = []
        game_objects_list_two = []
        for x in range(rnd(1, 15)):
            game_objects_list_one.append(choice(game_object_types_one)(canvas))
            game_objects_list_two.append(choice(game_object_types_two)(canvas))
        scope = Scope(canvas)
        scope.set_on_filed()
        game_engine = GameEngine(
            canvas, scope, game_objects_list_one, game_objects_list_two)
        return game_engine

    def __run(self, idle=10):
        self.__new_game.motion()
        self.stats_canvas.itemconfig(
            self.__round_text, text=f'Round: {self.__round_counter}')
        self.stats_canvas.itemconfig(
            self.__score_text, text=f'Score: {self.__new_game.score}')
        if self.__game_continue(self.__new_game):
            self.__timer += idle
            self.stats_canvas.itemconfig(
                self.__timer_text, text=f'Timer: {round(self.__timer/1000, 1)} sec')
            self.root.after(idle, lambda: self.__run())

        else:
            self.root.destroy()

    def __game_continue(self, engine):
        result = True
        if engine.get_qty_objects() == 0:
            user_result = round(engine.score/(self.__timer/1000)*10)
            if user_result > self.score_controller.get_min_value():  # NEW IN TOP
                self.field_canvas.create_text(self.field_canvas.winfo_width()/2, 200,
                                              text="NEW RECORD!", fill=rnd_color(), font=('Mono', 82))
                self.field_canvas.create_text(self.field_canvas.winfo_width()/2+4, 204,
                                              text="NEW RECORD!", fill=rnd_color(), font=('Mono', 82))
                self.field_canvas.configure(cursor='arrow')
                self.__show_input_dialog_for_top_players(
                    user_result, self.score_controller)
            else:
                self.field_canvas.create_text(self.field_canvas.winfo_width()/2, 200,
                                              text="GAME OVER!", fill=rnd_color(), font=('Mono', 82))
                self.field_canvas.create_text(self.field_canvas.winfo_width()/2+4, 204,
                                              text="GAME OVER!", fill=rnd_color(), font=('Mono', 82))

            result = self.__ask_continue(user_result)
        return result

    def __ask_continue(self, score):
        answer = messagebox.askquestion(
            'Game over', f'Your result {score} points.\nDo you want to play again?', parent=self.root)
        if answer == messagebox.YES:
            self.field_canvas.delete(ALL)
            self.field_canvas.config(bg=rnd_color())
            self.score_canvas.config(bg=rnd_color())
            self.stats_canvas.itemconfig(self.__timer_text, fill=rnd_color())
            self.stats_canvas.itemconfig(self.__score_text, fill=rnd_color())
            self.stats_canvas.itemconfig(self.__round_text, fill=rnd_color())
            self.__new_game = self.__buld_game(self.field_canvas)
            self.__round_counter += 1
            self.__timer = 0
            return True
        return False

    def __show_input_dialog_for_top_players(self, score, score_conrol):
        inputDialog = InputNameDiaolog(self.root)
        self.root.wait_window(inputDialog.top)
        try:
            score_conrol.add_player(inputDialog.username[:8], score)
        except:
            pass

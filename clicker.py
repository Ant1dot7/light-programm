import time
import tkinter as tk
import pickle


class Clicker:

    def __init__(self, master):
        self.master = master
        self.master.title("Clicker")
        self.master.geometry("400x300")
        self.timer_id = None  # mark for stop timer
        try:
            with open('data.pickle', 'rb') as f:
                self.max_score = pickle.load(f)
        except FileNotFoundError:
            self.max_score = {5: 0, 10: 0, 60: 0, 120: 0}

        self.score = 0  # record for this game

        self.start_button = tk.Button(self.master, height=2, width=5, text="Start",
                                      command=self.start_game)  # create button start
        self.start_button.place(x=180, y=100)

        # label for record
        self.label_max_score = {}
        self.y = 50
        for i in self.max_score.keys():
            self.label_max_score[i] = tk.Label(self.master, text=f'Max score {i}: {self.max_score[i]}')
            self.label_max_score[i].place(x=3, y=self.y)
            self.y += 20

        # Chose time
        self.label_chose_time = tk.Label(self.master, text='Chose time:')  # label for choose time
        self.label_chose_time.place(x=3, y=150)
        self.selected_value = tk.IntVar(value=10)
        self.radio_time_buttons = {}
        self.y = 170
        for i in self.max_score.keys():  # button for choose time
            self.radio_time_buttons[i] = tk.Radiobutton(self.master, text=f'{i} second', variable=self.selected_value,
                                                        value=i)
            self.radio_time_buttons[i].place(x=3, y=self.y)
            self.y += 20

    def start_game(self):

        self.start_button.place_forget()  # hide the button Start

        self.timer_label = tk.Label(self.master, text='')  # label for timer
        self.timer_label.pack()

        self.click_button = tk.Button(self.master, height=2, width=5, text='Click',
                                      command=self.click)  # create button Click
        self.click_button.place(x=180, y=100)

        self.stop_button = tk.Button(self.master, text='Stop', command=self.stop_game)  # open button Stop
        self.stop_button.place(x=180, y=155)

        self.label_click = tk.Label(self.master, text=f'Score: {self.score}')  # create label for record this game
        self.label_click.pack()

        self.countdown(self.selected_value.get())  # start timer

    def countdown(self, time):
        if time <= 0:
            self.stop_game()
            return
        self.timer_label.configure(text=f'Remain: {time} second')
        self.timer_id = self.master.after(1000, self.countdown, time - 1)

    def click(self):
        self.score += 1
        self.label_click.configure(text=f'Score: {self.score}')

    def save_record_after_game(self):
        if self.max_score[self.selected_value.get()] <= self.score:
            self.max_score[self.selected_value.get()] = self.score
            self.label_max_score[self.selected_value.get()].configure(
                text=f'Max score {self.selected_value.get()}: {self.max_score[self.selected_value.get()]}')
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.max_score, f)

    def stop_game(self):
        self.save_record_after_game()
        self.score = 0  # reset the record this game

        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        self.stop_button.place_forget()  # hide the button Stop
        self.click_button.place_forget()  # hide the button Click
        self.label_click.pack_forget()  # hide the record this game
        self.timer_label.pack_forget()  # hide timer
        self.start_button.place(x=180, y=100)  # open the button     Start
        self.start_button.configure(state='disabled')
        self.master.after(1300, lambda: self.start_button.configure(state='normal'))


root = tk.Tk()
clicker = Clicker(root)
root.mainloop()

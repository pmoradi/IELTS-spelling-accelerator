from tkinter import *
import tkinter
from turtle import bgcolor
import pathlib
import time
from pygame import mixer
import os
import random
import pandas as pd
from tools.type_controller.validator import Validator
import pickle
import webbrowser
import voice_scrapper as vs
from tkinter.tix import *


current_path = pathlib.Path(__file__).parent.resolve()._str
# Define GUI class
class Spelling_APP:

    # Initialize function to prepare GUI
    def __init__(self, master):
        tool_tip = Balloon(master)
        master.geometry('%dx%d+%d+%d' % (350, 200, 50, 50))
        # master.bind("<Button-3>", print_text)
        self.word_list = pd.read_csv('./data/word_list.csv')
        self.word_list.columns = ['word']

        if os.path.exists('./data/index.pickle'):
            with open('./data/index.pickle', 'rb') as handle:
                self.index = pickle.load(handle)
        else:
            self.index = 1

        file = self.word_list.loc[self.index - 1, 'word']
        self.play_sound(f'./voices/{file}')

        self.master = master

        self.master.title("Spelling practice")
        self.master.bind('<Left>', self.prev_key)
        self.master.bind('<Right>',self.next_key)
        self.master.bind('<Return>',self.show_word_acton)
        self.master.bind('<o>',self.incorrect_action)

        
        row1 = 10
        column = 10
        self.previous = Button(text="<", font='Arial 9', command=self.prev_sound)
        self.previous.place(x=row1 + 60, y=column + 80)
        tool_tip.bind_widget(self.previous, balloonmsg="Click on '<' key") 

        self.next = Button(text=">", command=self.next_sound, font='Arial 9')
        self.next.place(x= row1 + 80, y=column + 80)
        tool_tip.bind_widget(self.next, balloonmsg="Click on '>' key") 

        self.incorrect = Button(text="✘", command=self.incorrect_action, font='Arial 9')
        self.incorrect.place(x=row1 + 235, y=column+80)
        tool_tip.bind_widget(self.incorrect, balloonmsg="Click on 'o' key") 

        self.show_btn = Button(text="show", command=self.show_word_acton, font='Arial 9')
        self.show_btn.place(x=row1 + 130, y=column+80)
        tool_tip.bind_widget(self.show_btn, balloonmsg="Click on 'Enter' key") 

        self.word_lbl = Text(height=1, borderwidth=0, width=-1)
        self.word_lbl.place(x=row1 + 120, y=column+120)
        self.word_lbl.place_forget()

        self.link = Label(root, text="see translation", fg="blue", cursor="hand2")
        self.link.place(x=row1 + 120, y=column+140)
        self.link.bind("<Button-1>", lambda e: self.callback("https://translate.google.com/?sl=en&tl=fa&text=&op=translate"))
        
        self.var = IntVar()
        self.checkbox = Checkbutton(self.master, text="review", variable=self.var, command=self.review_action)
        self.checkbox.place(x=row1, y=column)
        

        start_lbl = Label(text='start point:')
        start_lbl.place(x=row1 + 110, y=column )
        self.start_point = Entry(width=10)
        self.start_point.place(x=row1 + 180, y=column)

        self.go_btn = Button(text="Go", command=self.go_action, font='Arial 7')
        self.go_btn.place(x=row1 + 250, y=column)

        self.start_lbl = Label(text=f'{self.index}/{len(self.word_list)}')
        self.start_lbl.place(x=row1 + 130, y=column + 30)
    
    def print_text(self):
        print('ok')

    def callback(self, url):
        webbrowser.open_new(url)
                        
    def review_action(self):
        value = self.var.get()

        if value == 1:
            self.word_list = pd.read_csv('./data/mistakes.csv')
            self.word_list.columns = ['word']
            self.index = 1
            self.prev_key()
        else:
            self.word_list = pd.read_csv('./data/word_list.csv')
            self.word_list.columns = ['word']
            if os.path.exists('./data/index.pickle'):
                with open('./data/index.pickle', 'rb') as handle:
                    self.index = pickle.load(handle)
            else:
                self.index = 1
            self.go_action(self.index)
    def play_sound(self, file_path):
        if '.mp3' not in file_path and '.wav' not in file_path:
            file_path += '.mp3'
        if not os.path.exists(file_path):
            print('File does not exist. We are going to download it ... ')
            voice = file_path.split('/')[-1]
            vs.save_voice(voice)
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(.1)

    def update_status(self):  
        self.insert_text('')
        self.word_lbl.place_forget()     
        self.master.focus()
        self.start_lbl['text'] = f'{self.index}/{len(self.word_list)}'
        
        if self.var.get() != 1:
            with open('./data/index.pickle', 'wb') as handle:
                pickle.dump(self.index, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def next_sound(self):
        if len(self.word_list) == 0:
            tkinter.messagebox.showerror("INPUT ERROR", "List is empty")
            return
        
        if self.index != len(self.word_list):
            self.index += 1
        self.start_lbl['text'] = f'{self.index}/{len(self.word_list)}'
        
        file = self.word_list.loc[self.index - 1, 'word']
        self.play_sound(f'./voices/{file}')
        self.update_status()

    def prev_sound(self):
        if len(self.word_list) == 0:
            tkinter.messagebox.showerror("INPUT ERROR", "List is empty")
            return
        
        if self.index != 1:
            self.index -= 1
        self.start_lbl['text'] = f'{self.index}/{len(self.word_list)}'
        
        file = self.word_list.loc[self.index - 1, 'word']
        self.play_sound(f'./voices/{file}')
        self.update_status()

    def correct_action():
        pass
    
    def get_mistakes_dic(self):
        self.mistakes = {}

        if not os.path.exists('./data/mistakes.csv'):
            with open('./data/mistakes.csv','a') as fd:
                fd.write('word\n')
            
        with open('./data/mistakes.csv') as file:
            lines = file.readlines()
        for l in lines:
            l = l.replace('\n', '')
            if '.' not in l:
                continue
            self.mistakes[l] = True
        return self.mistakes
    
    def incorrect_action(self, e=None):
        review = self.var.get()
        if review == 0:
            self.mistakes = self.get_mistakes_dic()
            file = self.word_list.loc[self.index - 1, 'word']
            
            if file not in self.mistakes:
                with open('./data/mistakes.csv','a') as fd:
                        fd.write(f'{file}\n')
            self.mistakes[file] = True
            self.play_sound('./data/mistake.wav')
            self.next_sound()
        else:
            if len(self.word_list) == 0:
                tkinter.messagebox.showerror("INPUT ERROR", "List is empty")
                return
            self.word_list = self.word_list.drop(self.index - 1, axis=0)
            self.index = min(self.index+1, len(self.word_list))
            self.word_list.index = list(range(0, len(self.word_list)))
            self.word_list.to_csv('./data/mistakes.csv', index=False)
            self.play_sound('./data/mistake.wav')
            self.prev_sound()
            # if len(self.word_list) > 0:
            #     file = self.word_list.loc[self.index - 1, 'word']
            #     self.play_sound(f'./voices/{file}')
            self.update_status()

    def next_key(self, e=None):
        self.next_sound()
    
    def prev_key(self, e=None):
        self.prev_sound()

    def insert_text(self, text):
        self.word_lbl.place(x=130, y=130)       
        self.word_lbl.configure(state='normal')
        self.word_lbl.configure(width=len(text))
        self.word_lbl.delete(1.0, "end")
        self.word_lbl.insert(1.0, text) 
        self.word_lbl.configure(state="disabled")
        self.link.bind("<Button-1>", lambda e: self.callback(f"https://translate.google.com/?sl=en&tl=fa&text={text}&op=translate"))
    
    def show_word_acton(self, e=None):
        file = self.word_list.loc[self.index - 1, 'word']
        # self.word_lbl.insert(1.0, file[:-4])

        self.insert_text(file)

        self.play_sound(f'./voices/{file}')

    def go_action(self, index=None):
        if not index:
            value = self.start_point.get()
            res = Validator(value).is_numeric().in_range((1, len(self.word_list))).get()
            if res['status'] != 'SUCCESS':
                tkinter.messagebox.showerror("INPUT ERROR", res['error_message'])
                return
            self.index = res['value']
        else:
            self.index = index
        self.start_lbl['text'] = f'{self.index}/{len(self.word_list)}'
        
        file = self.word_list.loc[self.index - 1, 'word']
        self.play_sound(f'./voices/{file}') 
        self.update_status()
        
        

root = Tk()
root.resizable(0, 0)
my_gui = Spelling_APP(root)
root.mainloop()

# 400
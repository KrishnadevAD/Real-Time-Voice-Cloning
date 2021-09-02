from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import simpleaudio as sa
import interface as i
from  tkinter import  messagebox,ttk
import time
import wave
import contextlib
import math
import threading
from PIL import Image, ImageTk
from itertools import count, cycle
from  wave_form import targeted_mel


def output_page(win,given_text,f_path):

    # root widget
    win.resizable(0, 0)
    win.title("Nepali AI Anchor")
    # Window size
    appWidth = 852
    appHeight = 480
    font = "Times New Roman"

    #option
    option=["05 sec","10 sec", "20 sec ", "30 sec", "60 sec"]
    global file_path,button_play,button_stop
    screenWidth = win.winfo_screenwidth()
    screenHeight = win.winfo_screenheight()


    x = int((screenWidth / 2) - (appWidth / 2))
    y = int((screenHeight / 2) - (appHeight / 2))

    # window pops up on center of the screen
    win.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

    #destroy this page
    def call_page(root):
        for widget in root.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        i.hd(root,given_text,f_path)




    text = Label( text=("Targeted Mel Spectogram:"))
    text.place(relx=0.03, rely=0.02)
    text = Label(text=("Predicted Mel Spectogram:"))
    text.place(relx=0.5, rely=0.02)

    #targeted mel spectrogram canvas
    canvas = Canvas(win, width = 377, height = 120,highlightthickness=1, highlightbackground="black")
    canvas.place(relx=0.028, rely=0.078)
    targeted_mel(win)
    # predicted mel spectrogram canvas
    canvas1 = Canvas(win, width = 400, height = 120,highlightthickness=1, highlightbackground="black",bg="white")
    canvas1.place(relx=0.5, rely=0.08)
    canvas1.create_image(0,0, anchor=NW)

    #back button
    originalImg1 = Image.open("back_button1.png")
    resized1 = originalImg1.resize((40, 40), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(resized1)
    button_back = Button(win,image=img2, command=lambda:call_page(win) ,highlightthickness = 0, bd = 0)
    button_back.place(relx=0.0, rely=0.905)

    #audio play canvas
    canvas2 = Canvas(win, width=800, height=45, highlightthickness=0, bg="light cyan")
    canvas2.place(relx=0.05, rely=0.9)

    # audio play button
    global s_audio,duration,duration1,temp_duration,play_obj,after_id
    s_audio = 0
    duration1="00"
    fname = 'demo_output_00.wav'
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        temp_duration = frames / float(rate)
        temp_duration = math.ceil(temp_duration)
        duration = temp_duration % 60
        if temp_duration>59:
            duration1=str(int(temp_duration/60))
            if int(duration1)<10:
                duration1="0"+duration1




    def set_status(value):
        global s_audio
        s_audio = value


    def stop_audio(img4, img3,play_temp):
        global button_play, button_stop, s_audio,after_id
        s_audio=1
        win.after_cancel(after_id)
        play_temp.stop()
        button_stop.destroy()
        pb['value'] = 0
        T_text1.config(text=("00:00"))
        button_play = Button(win, image=img3, command=lambda: play_audio(img4, img3), highlightthickness=0, bd=0,
                             bg="light cyan")
        button_play.place(relx=0.07, rely=0.905)



    #play audio
    def play_audio(img4,img3):
        global button_play, button_stop,play_obj
        button_play.destroy()
        def run1():
            global s_audio,play_obj
            s_audio=0
            wave_obj = sa.WaveObject.from_wave_file("demo_output_00.wav")
            play_obj = wave_obj.play()
            while True:
                if play_obj.is_playing()!=True:
                    stop_audio(img4,img3,play_obj)
                    break
        def run():
            global s_audio,temp_duration
            count_sec=0
            count_min="00"
            while pb['value'] <= 100 and s_audio==0 :
                    count_sec+=1
                    pb['value'] += (100 / temp_duration)
                    if count_sec>=10:
                        if count_sec==60:
                            count_sec=0
                            count_min=str(int(count_min)+1)
                        T_text1.config(text=(count_min+":"+str(count_sec)))
                    else:
                        T_text1.config(text=(count_min + ":0"+str(count_sec)))
                    time.sleep(1)

        #animation canvas

        class ImageLabel(tk.Label):
            """
            A Label that displays images, and plays them if they are gifs
            :im: A PIL Image instance or a string filename
            """

            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                frames = []

                try:
                    for i in count(1):
                        frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass
                self.frames = cycle(frames)

                try:
                    self.delay = im.info['duration']
                except:
                    self.delay = 100

                if len(frames) == 1:
                    self.config(image=next(self.frames))
                else:
                    self.next_frame()

            def unload(self):
                self.config(image=None)
                self.frames = None

            def next_frame(self):
                global after_id,s_audio
                if self.frames:
                    self.config(image=next(self.frames))
                    if s_audio==1:
                        stop_audio(img3,img3,play_obj)
                    after_id=self.after(self.delay, self.next_frame)

        lbl = ImageLabel(win)
        lbl.place(relx=0.03, rely=0.35)
        lbl.load('anchor.gif')

        # demo :
        button_stop = Button(win, image=img4, command=lambda: stop_audio(img4, img3, play_obj), highlightthickness=0,
                             bd=0,
                             bg="light cyan")
        button_stop.place(relx=0.07, rely=0.905)

        p = threading.Thread(target=run1)
        p.daemon = True
        p.start()
        p1 = threading.Thread(target=run)
        p1.daemon = True
        p1.start()

        # stop audio
    originalImg1 = Image.open("play_button.png")
    resized1 = originalImg1.resize((40, 40), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(resized1)
    originalImg2 = Image.open("stop_button.png")
    resized2 = originalImg2.resize((40, 40), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(resized2)
    button_play = Button(win, image=img3, command=lambda: play_audio(img4,img3), highlightthickness=0, bd=0,bg="light cyan")
    button_play.place(relx=0.07, rely=0.905)

      #progress_bar
    pb = ttk.Progressbar(
        win,
        orient='horizontal',
        mode='determinate',
        length=600,

    )
    # place the progressbar
    pb.place(relx=0.17, rely=0.93)


    T_text1 = Label(text=("00:00" ),bg="light cyan")
    T_text1.place(relx=0.12, rely=0.925)
    if duration<10:
        T_text2 = Label(text=(duration1+":0"+str(duration) ),bg="light cyan")
        T_text2.place(relx=0.88, rely=0.925)
    else:
        T_text2 = Label(text=(duration1+":" + str(duration)), bg="light cyan")
        T_text2.place(relx=0.88, rely=0.925)

    # video canvas
    canvas5 = Canvas(win, width=496, height=235, highlightthickness=1, highlightbackground="black")
    canvas5.place(relx=0.03, rely=0.35)
    originalImg5 = Image.open("anchor.gif")
    resized5= originalImg5.resize((496, 235), Image.ANTIALIAS)
    img5 = ImageTk.PhotoImage(resized5)
    canvas5.create_image(0, 0, anchor=NW, image=img5)

    win.mainloop()

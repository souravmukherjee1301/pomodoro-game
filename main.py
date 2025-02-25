import os
from tkinter import *
import math
import winsound  # For Windows
import pygame    # For Mac & Linux

pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
BLUE = "#3674B5"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
timer = None
reps = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Break", fg=BLUE)
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    min = math.floor(count / 60)
    sec = count % 60
    if sec < 10:
        sec = f"0{sec}"

    if min < 10:
        min = f"0{min}"

    canvas.itemconfig(timer_text, text=f"{min}:{sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # 🛎️ Play a sound when a session ends
        try:
            if os.name == "nt":  # Windows
                winsound.Beep(1000, 500)  # Frequency = 1000 Hz, Duration = 500ms
            else:  # Mac & Linux
                pygame.mixer.music.load("alarm.mp3")  # Use an MP3 file
                pygame.mixer.music.play()
        except Exception as e:
            print("Error playing sound:", e)

        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 24, "bold"), bg=YELLOW)
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", bg=GREEN, font=(FONT_NAME, 12, "bold"), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", bg=RED, font=(FONT_NAME, 12, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14))
check_marks.grid(column=1, row=3)

window.mainloop()

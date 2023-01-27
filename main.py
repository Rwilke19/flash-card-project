# 101 Words
BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random

card = {}
to_learn = {}


def next_card():
    global card, flip_timer
    window.after_cancel(flip_timer)
    card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=card["French"], fill="black")
    canvas.itemconfig(imagev, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(imagev, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=card["English"], fill="white")


def is_known():
    to_learn.remove(card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Make a window
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
flip_timer = window.after(3000, func=flip_card)
# Put data into lists
try:
    db = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original = pandas.read_csv("data/french_words.csv")
    to_learn = original.to_dict(orient="records")
else:
    to_learn = db.to_dict(orient="records")

# Make a canvas
canvas = Canvas(height=526, width=800)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
imagev = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text=f'', font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=1, columnspan=2)

# Buttons
correct = PhotoImage(file="./images/right.png")
incorrect = PhotoImage(file="./images/wrong.png")
right = Button(image=correct, highlightthickness=0, command=is_known)
wrong = Button(image=incorrect, highlightthickness=0, command=next_card)
right.grid(row=2, column=2)
wrong.grid(row=2, column=1)

next_card()

window.mainloop()

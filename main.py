from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


def know_it():
    global current_card
    to_learn.remove(current_card)
    new_to_learn = pandas.DataFrame(to_learn)
    new_to_learn.to_csv("data/word_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Images
canvas = Canvas(bg=BACKGROUND_COLOR, width=850, height=530, highlightthickness=0)
# card front
card_front = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(425, 275, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# remaining images
card_back = PhotoImage(file="./images/card_back.png")
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")


# Buttons
known_button = Button(image=right, highlightthickness=0, command=know_it)
known_button.grid(column=1, row=1)
unknown_button = Button(image=wrong, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()




window.mainloop()

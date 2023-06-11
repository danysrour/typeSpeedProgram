from tkinter import *
from tkinter import messagebox
from wonderwords import RandomWord
import time

# initialize an empty list / this is generated with each game restart
words_list = []
# the game start at word with index 0 and with char at index 0
# First word and First char
current_word = 0
current_char = 0
# Start with 0 correct words
correct_words = 0
# checker for current word if it's type correctly / set to True by default changed on each word when typed wrong
current_word_correct = True
# game time is 1 minute
seconds = 60
countdown_started = False
# level
level = "Medium"


def highlight_word(word_index, text_widget, color):
    text_widget.tag_remove("highlight_tag", "1.0", "end")
    # Get the current text content
    content = text_widget.get("1.0", "end")

    # Split the content into words
    words = content.split()

    # Check if the word_index is within the valid range
    if word_index < 0 or word_index >= len(words):
        return

    # Calculate the start and end indices of the word
    start_index = "1.0"
    for i in range(word_index):
        start_index = text_widget.search(words[i], start_index, stopindex="end")
        if not start_index:
            break
        start_index = f"{start_index} + {len(words[i])}c"  # Update start_index to the end_index of the previous word

    end_index = text_widget.search(words[word_index], start_index, stopindex="end")
    if not end_index:
        return
    end_index = f"{end_index} + {len(words[word_index])}c"

    # Configure a new tag with the desired color
    tag_name = "highlight_tag"
    text_widget.tag_configure(tag_name, background=color)

    # Apply the new tag to the specified word
    text_widget.tag_add(tag_name, start_index, end_index)


def generate_text():
    """
    Generates a random text and use it in our game
    :return:
    """
    global words_list, level

    # delete the current text words
    text.delete('1.0', 'end')
    level = choice.get()

    # Generate 100 random words using wonderwords library
    r = RandomWord()
    if level == "Very Hard":
        words_list = r.random_words(100, word_max_length=20, word_min_length=15, return_less_if_necessary=True)
    if level == "Hard":
        words_list = r.random_words(100, word_max_length=15, word_min_length=8, return_less_if_necessary=True)
    if level == "Medium":
        words_list = r.random_words(100, word_max_length=8, word_min_length=5)
    if level == "Easy":
        words_list = r.random_words(100, word_max_length=5, word_min_length=3)
    if level == "Very Easy":
        words_list = r.random_words(100, word_max_length=3, word_min_length=2)

    # set the text to the generated words
    text.insert('1.0', ' '.join(words_list))

    # highlight the first word
    highlight_word(0, text, 'yellow')


def on_key_press(event):
    global countdown_started
    """
    Event checker for user input
    :param event:
    :return:
    """

    # Get the keycode of the pressed key
    keycode = event.keycode

    # set the list of keys we would like to exclude
    pass_keys = ['Tab', 'Caps_Lock', 'Shift_L', 'BackSpace', 'Control_L', 'Win_L', 'Return', 'Shift_R', 'Control_R', 'Alt_R', 'Alt_L']

    # if pressed key is from the excluded do nothing
    if event.keysym in pass_keys:
        pass
    # if pressed key is space go to next word
    elif event.keysym == "space":
        next_word()
    else:
        # if first word and character we start the countdown
        if current_char == 0 and current_word == 0 and not countdown_started:
            countdown_started = True
            countdown()
        # we check each character sent by the user
        check_character(event.char)


def next_word():
    """
    Logic for getting to next word
    :return:
    """
    global current_word, current_char, current_word_correct, correct_words, seconds

    try:
        # check if the user have all the current word written right and that all character are typed for this word
        if current_word_correct and current_char == len(words_list[current_word]):
            # increase the score
            correct_words += 1
            # set the current score
            cpm_label_text.config(text=correct_words)

        # move index to next word
        current_word = current_word + 1
        # next word starts at char 0
        current_char = 0
        # assume user starts with a correct word
        current_word_correct = True
        # delete the user input entry
        typing_entry.delete(0, END)
        # highlight the next word
        highlight_word(current_word, text, 'yellow')
    except IndexError as err:
        seconds = 0

def check_character(char):
    """
    Logic for checking the user input per each key press
    :param char:
    :return:
    """
    global current_char, current_word_correct

    # check if the user input is correct
    try:
        if char == words_list[current_word][current_char]:
            # if so change the letter color to blue
            change_color(current_word + 1, current_char + 1, text, "blue")
        else:
            # if not change it to red
            change_color(current_word + 1, current_char + 1, text, "red")
            # if user missed let the program now
            current_word_correct = False
        # move to next char in the word
        current_char = current_char + 1
    except IndexError as err:
        pass

def change_color(word_num, char_num, text_widget, color):
    # Subtract 1 from word_num and char_num to get the correct indices
    # I like to keep it like this to keep indexes starting at 0 not 1
    word_index = word_num - 1
    char_index = char_num - 1

    # Get the current text content
    content = text_widget.get("1.0", "end")

    # Split the content into words
    words = content.split()

    # Calculate the character index
    total_char_index = 0
    for i in range(word_index):
        total_char_index += len(words[i]) + 1  # Add 1 for the space between words

    total_char_index += char_index

    # Configure a new tag with the desired color
    tag_name = f"color_tag_{word_num}_{char_num}"
    text_widget.tag_configure(tag_name, foreground=color)

    # Apply the new tag to the specified character
    start_index = f"1.0 + {total_char_index}c"
    end_index = f"1.0 + {total_char_index + 1}c"
    text_widget.tag_add(tag_name, start_index, end_index)


def change_color_word(word_num, text_widget, color):
    # Subtract 1 from word_num to get the correct index
    word_index = word_num - 1

    # Get the current text content
    content = text_widget.get("1.0", "end")

    # Split the content into words
    words = content.split()

    # Calculate the character index
    start_index = f"1.0 + {' + '.join(str(len(words[i])) for i in range(word_index))}c"
    end_index = f"1.0 + {' + '.join(str(len(words[i])) for i in range(word_index + 1))}c"

    # Configure a new tag with the desired color
    tag_name = f"word_color_tag_{word_num}"
    text_widget.tag_configure(tag_name, foreground=color)

    # Apply the new tag to the specified word
    text_widget.tag_add(tag_name, start_index, end_index)


def start_over():
    """
    Restart game logic
    :return:
    """
    global current_word, current_char, seconds, correct_words, countdown_started

    countdown_started = False

    # Generate new text
    generate_text()

    # Rest everything
    current_char = 0
    current_word = 0
    correct_words = 0
    seconds = 60
    cpm_label_text.config(text="0")
    with open('score.txt') as file:
        wpm_label_text.config(text=file.read())
    typing_entry.delete(0, END)


def countdown():
    global seconds
    if seconds >= 0:
        time_label_text.config(text=seconds)
        seconds -= 1
        # make sure the program keeps working while countdown
        if countdown_started:
            tk.after(1000, countdown)
    else:
        # When time is over we check the score and compare to old score and update
        with open('score.txt', mode="r") as file:
            high_score = int(file.read())
            if correct_words > high_score:
                text.delete('1.0', 'end')
                text.insert('1.0', f"Time's up! You have a new high score {correct_words}")
                wpm_label_text.config(text=correct_words)
                with open('score.txt', mode="w") as file2:
                    file2.write(str(correct_words))
            else:
                text.delete('1.0', 'end')
                text.insert('1.0', f"Time's up! Your score is {correct_words}")
        tk.after(1000, reset_countdown)


def reset_countdown():
    global seconds, countdown_started
    seconds = 60
    time_label_text.config(text=str(seconds))
    countdown_started = False

# New Tkinter window
tk = Tk()

# set window title
tk.title("Writing speed test | Check your typing speed")

# set window to full screen
tk.wm_state('zoomed')

# add padding to window edge
tk.config(padx=50, pady=50, background="#C4DFDF")

# create main frame
frame = Frame(tk)
frame.config(width=600, height=450)
frame.pack()

# create top frame holder of statistics with all elements
frame1 = Frame(frame)
frame1.config(background="#E3F4F4", width=600, height=50)
frame1.grid(row=0, column=0)

cpm_label = Label(frame1, text="Correct Words:", font=('Arial', 12))
cpm_label.grid(row=0, column=0)

cpm_label_text = Label(frame1, text="0", font=('Arial', 12))
cpm_label_text.grid(row=0, column=1)
cpm_label_text.config(background="white", width=5, padx=1, pady=1)

wpm_label = Label(frame1, text="Best Score:", font=('Arial', 12))
wpm_label.grid(row=0, column=2)

wpm_label_text = Label(frame1, text="?", font=('Arial', 12))
wpm_label_text.grid(row=0, column=3)
wpm_label_text.config(background="white", width=5)
with open('score.txt') as file:
    wpm_label_text.config(text=file.read())

time_label = Label(frame1, text="Time Left:", font=('Arial', 12))
time_label.grid(row=0, column=4)

time_label_text = Label(frame1, text="60", font=('Arial', 12))
time_label_text.grid(row=0, column=5)
time_label_text.config(background="white", width=5)

# create middle frame holder of text with all elements
frame2 = Frame(frame)
frame2.config(background="#D2E9E9", width=600, height=300)
frame2.grid(row=1, column=0)

# Create a Text widget with vertical scrollbars
text = Text(frame2, wrap='word', font=('Arial', 15), height=10, pady=20, padx=20)
text.pack(fill='both', expand=False)
scrollbar = Scrollbar(tk, command=text.yview)
scrollbar.pack(side='right', fill='y')
text.config(yscrollcommand=scrollbar.set)
# Configure line spacing
text.tag_configure("line_spacing", spacing2=10)
# Apply line spacing to entire text
text.tag_add("line_spacing", "1.0", "end")


text.tag_configure("line_height", spacing1=10, spacing3=10)
text.tag_add("line_height", "1.0", "end")

# create third frame holder of user input with all elements
frame3 = Frame(frame)
frame3.config(background="#E3F4F4", width=600, height=50)
frame3.grid(row=2, column=0, pady=30)

typing_entry = Entry(frame3, width=43, justify='center', font=('Arial', 20))
typing_entry.grid(row=0, column=0)
typing_entry.focus()
typing_entry.bind("<Key>", on_key_press)

# create bottom frame holder of reset button with all elements
frame4 = Frame(frame)
frame4.config(width=600, height=50)
frame4.grid(row=3, column=0)

choice = StringVar()
choice.set("Medium")

radio_button = Radiobutton(frame4, text="Very Easy", variable=choice, value="Very Easy", font=('Arial', 12))
radio_button.grid(column=0, row=0)

radio_button = Radiobutton(frame4, text="Easy", variable=choice, value="Easy", font=('Arial', 12))
radio_button.grid(column=1, row=0)


radio_button = Radiobutton(frame4, text="Medium", variable=choice, value="Medium", font=('Arial', 12))
radio_button.grid(column=2, row=0)

radio_button = Radiobutton(frame4, text="Hard", variable=choice, value="Hard", font=('Arial', 12))
radio_button.grid(column=3, row=0)

radio_button = Radiobutton(frame4, text="Very Hard", variable=choice, value="Very Hard", font=('Arial', 12))
radio_button.grid(column=4, row=0)


reset_button = Button(frame4, text="Restart", width=13, command=start_over, font=('Arial', 12))
reset_button.grid(column=5, row=0, pady=20)

generate_text()

tk.mainloop()


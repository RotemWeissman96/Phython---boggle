import sys
import pygame
from tkinter import messagebox
import tkinter as tki

BOARD_SIZE = 4
TIME_UP = "TIME'S UP"
REGULAR_COLOR = 'white'
CORRECT_HEADER = "Correct words list"
WRONG_HEADER = "Wrong words list"
INSTRUCTION_TITLE = "BOGGLE GAME INSTRUCTION"
GAME_INSTRUCTION = "THIS GAME WAS PROGRAMMED BY HADAR AND ROTEM.\n" \
                   "THE GAME IS PLAYED WITH 4X4 BOARD OF LETTERS.\n " \
                   "THE OBJECTIVE IS TO FORM AS MANY WORDS AS POSSIBLE \n " \
                   "BY CLICKING ON THE WANTED LETTERS ON THE BOARD.\n " \
                   "*** RULES: ***A LETTER CAN'T BE SELECTED TWICE- " \
                   "YOU CAN ONLY SELECT ADJACENT LETTERS \n" \
                   "AFTER 3 MINUTES THE GAME IS OVER!!\n" \
                   "HOPE YOU ENJOY IT :)"
INITIAL_SECOND = 0
INITIAL_MINUTES_DISPLAY = 3
GAME_TIME_MINUTES = 3
INITIAL_SCORE = 0
INITIAL_TIME_DISPLAY = str(INITIAL_MINUTES_DISPLAY) + " : " + str(
    INITIAL_SECOND) * 2


class Game:
    """
    This class is responsible for running a Boogle game.
    The game is set so that the board is 4x4 in size,
    the user will have to find as many words as possible,
    that the distance between each letter in the board will be at most 1.
    After three minutes, the player will be asked whether he wants to play a
    new game or not.
    """

    def __init__(self):
        """
        For convenience we have defined each of the initials under a note
        describing what it is responsible for.
        An object from this class- Game, has many features,
        which define the game board, the buttons in them, the current player's
        score and the amount of time that has elapsed since the start of the
        current game.
        """

        # ############# init main_frame ##############
        self.root = tki.Tk()
        self.root.title("BOGGLE")
        self.root.resizable(0, 0)
        self.main_window = self.root
        self.root.configure(bg="white")
        self.root.geometry("750x580")
        self.img = tki.PhotoImage(file="boogle.png")
        self.label_img = tki.Label(self.root, image=self.img,
                                   borderwidth=0,
                                   compound="center", highlightthickness=0,
                                   padx=0,
                                   pady=0)
        self.label_img.place(relx=0, rely=0)

        # ############ init_time #####################
        self.minutes = GAME_TIME_MINUTES
        self.seconds = INITIAL_SECOND
        self.clock = tki.Label(self.root, bg="white", height=2, width=11,
                               relief=tki.RAISED,
                               text=INITIAL_TIME_DISPLAY,
                               font=("Calibri", 16))
        self.clock.place(relx=0.81, rely=0.005)

        # ############# init_board ####################
        self.board_frame = tki.Frame(self.root, bg="white",
                                     highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5, borderwidth=1)
        self.board_frame.place(relx=0, rely=0.20, relwidth=0.65,
                               relheight=0.65)
        self.buttons = self.create_buttons()

        # ############ init_score #########################
        self.score = tki.Label(self.root, bg="white", height=2, width=15,
                               relief=tki.RAISED,
                               text="your score is: \n " + str(
                                   INITIAL_SCORE), font=("Calibri", 16))
        self.score.place(relx=0.55, rely=0.005)

        # ############# init_instructions ##################
        self.instructions = tki.Button(self.root, bg="white", height=1,
                                       width=12,
                                       relief=tki.RAISED,
                                       command=self.instructions_pop,
                                       text="INSTRUCTIONS",
                                       font=("Calibri", 16))
        self.instructions.place(relx=0.555, rely=0.89)

        # ############# start&pause ####################
        self.is_paused = False
        self.freeze = tki.Button(self.root, text="PAUSE", bg="white",
                                 relief=tki.RAISED,
                                 height=1,
                                 width=8, font=("Calibri", 16),
                                 command=self.stop, state=tki.DISABLED)
        self.freeze.place(relx=0.86, rely=0.89)
        self.start_btn = tki.Button(self.root, text="START", bg="white",
                                    relief=tki.RAISED,
                                    height=1,
                                    width=6, font=("Calibri", 16))
        self.start_btn.place(relx=0.75, rely=0.89)
        self.pause_block = tki.Frame(self.root, bg="#7DFFAA",
                                     highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5, borderwidth=1)

        # ############ init_restart ######################
        self.timeup_frame = tki.Frame(self.root, borderwidth=1, bg="black")
        self.restart_yes = tki.Button(self.timeup_frame, text="YES",
                                      relief=tki.RAISED, height=1,
                                      width=7, font=("Calibri", 16))
        self.restart_yes.place(relx=0.10, rely=0.60, relwidth=0.30,
                               relheight=0.30)
        self.restart_no = tki.Button(self.timeup_frame, text="NO ",
                                     relief=tki.RAISED, height=1,
                                     width=7, font=("Calibri", 16))
        self.restart_no.place(relx=0.60, rely=0.60, relwidth=0.30,
                              relheight=0.30)
        self.restart_label = tki.Label(self.timeup_frame,
                                       text="TIME UP!! " + self.score['text'] +
                                            " points, WANT TO RESTART?")
        self.restart_label.place(relx=0.05, rely=0.10, relwidth=0.90,
                                 relheight=0.20)

        # ########### initial_scroll_bar_words #########
        self.correct_listbox = tki.Listbox(self.root)
        self.correct_listbox.place(relx=0.8, rely=0.175, relwidth=0.4,
                                   relheight=0.3)
        self.correct_scroll = tki.Scrollbar(self.root)
        self.correct_scroll.place(relx=0.97, rely=0.175, relwidth=0.03,
                                  relheight=0.3)
        self.correct_head = tki.Label(self.root, font=("Calibri", 14),
                                      bg="green",
                                      text=CORRECT_HEADER, relief=tki.RAISED)
        self.correct_head.place(relx=0.8, rely=0.12, relwidth=0.2,
                                relheight=0.05)
        self.wrong_listbox = tki.Listbox(self.root)
        self.wrong_listbox.place(relx=0.8, rely=0.58, relwidth=0.4,
                                 relheight=0.3)
        self.wrong_scroll = tki.Scrollbar(self.root)
        self.wrong_scroll.place(relx=0.97, rely=0.58, relwidth=0.03,
                                relheight=0.3)
        self.wrong_header = tki.Label(self.root, font=("Calibri", 14),
                                      bg="red",
                                      text=WRONG_HEADER, relief=tki.RAISED)
        self.wrong_header.place(relx=0.8, rely=0.52, relwidth=0.2,
                                relheight=0.05)

        # ############### init_answer_option##############
        self.create_words_lists()
        self.answer = tki.Label(self.root, bg="#7DFFAA", height=2,
                                relief=tki.RAISED,
                                width=27, text=" ", font=("Calibri", 16))
        self.answer.place(relx=0.01, rely=0.88)
        self.insert_btn = tki.Button(self.root, text="INSERT", bg="white",
                                     relief=tki.RAISED, height=1,
                                     width=7, font=("Calibri", 16))
        self.insert_btn.place(relx=0.43, rely=0.89)

        self.pause_block.place(relx=0, rely=0.20, relwidth=0.65,
                               relheight=0.65)
        self.insert_btn["state"] = tki.DISABLED

    # ##################

    def instructions_pop(self):
        """
        When the user clicks on an instruction button, a screen pops up
        showing the game instructions, accompanied by music
        """
        pygame.mixer.music.load("disco_dancing.wav")
        pygame.mixer.music.play(loops=1)
        answer = tki.messagebox.showinfo(INSTRUCTION_TITLE, GAME_INSTRUCTION)

    pygame.mixer.init()

    def stop(self):
        """
        This method is responsible for stopping the game when the user
        selects the dedicated button. In this case, time will stop,
        the board will be hidden from the user,
        and the user will not be able to perform any action other than to
        return the game or to read the instructions.
        """
        if not self.is_paused:
            self.is_paused = True
            self.freeze["text"] = "CONTINUE"
            self.freeze["state"] = tki.DISABLED
            self.start_btn["text"] = " "
            self.start_btn["state"] = tki.DISABLED
            self.insert_btn["text"] = " "
            self.insert_btn["state"] = tki.DISABLED
            self.clock["text"] = " "
            self.pause_block.place(relx=0, rely=0.20, relwidth=0.65,
                                   relheight=0.65)
            self.wrong_listbox["state"] = tki.DISABLED
            self.correct_listbox["state"] = tki.DISABLED
            self.pause_block.update()
            self.root.update_idletasks()
            self.freeze.after(1000, self.freeze.config(state=tki.NORMAL))

        elif self.is_paused:
            self.is_paused = False
            self.freeze["text"] = "PAUSE"
            self.wrong_listbox["state"] = tki.NORMAL
            self.correct_listbox["state"] = tki.NORMAL
            self.insert_btn["text"] = "INSERT"
            self.freeze["state"] = tki.NORMAL
            self.insert_btn["state"] = tki.NORMAL
            self.start_btn["text"] = "QUIT"
            self.start_btn["state"] = tki.NORMAL
            self.pause_block.place_forget()
            self.timer()

    def basic_actions(self):
        """
        This method is responsible for starting and exiting the game via the
        "start_btn" button. When the user clicks the Exit button - The game
        will give user an option to reboot the game. If he chooses not to boot,
        a screen will pop up in front of him making sure that he is indeed
        interested in ending the game.
        """
        if self.start_btn["text"] == "START":
            self.start_btn["text"] = "QUIT"
            self.insert_btn["state"] = tki.NORMAL
            self.start_game()
            self.pause_block.place_forget()
        elif self.start_btn["text"] == "QUIT":
            answer2 = tki.messagebox.askquestion("RESTART?",
                                                 "DO YOU WANT "
                                                 "TO RESTART THE GAME?")
            if answer2 == "yes":
                return True
            answer = tki.messagebox.askquestion("QUIT",
                                                "ARE YOU SURE YOU WANT "
                                                "TO END THE GAME?")
            if answer == "yes":
                sys.exit()
            return False

    def timer(self):
        """
        This method is accountable for the clock time displayed.
        It runs from 3:00 minutes to 0:00.
        When the time is up, a screen pops up asking the user if they want to
        start the game again.
        """
        if not self.is_paused:
            if self.seconds == 0 and self.minutes > 0:
                self.minutes -= 1
                self.seconds = 59
            else:
                self.seconds -= 1
            if self.seconds < 10:
                # we want the clock to display the seconds by two digits
                current_time = str(self.minutes) + " : 0" + str(self.seconds)
            else:
                current_time = str(self.minutes) + " : " + str(self.seconds)
            if self.clock["state"] != tki.DISABLED:
                self.clock.config(text=current_time)
                self.clock.after(1000, self.timer)
            if self.minutes == 0 and self.seconds == 0:
                self.clock.configure(text=INITIAL_TIME_DISPLAY,
                                     state=tki.DISABLED)
                self.restart_label.config(
                    text="TIME UP!! " + self.score['text'] +
                         " points, WANT TO RESTART?")
                self.timeup_frame.place(relx=0.20, rely=0.30, relwidth=0.40,
                                        relheight=0.30)

    def start_game(self):
        """
        Initializes the clock according to the initial time,
        ie three minutes, initializes a score to zero and calls the timer method
        that accountable for the clock's function
        """
        self.minutes = GAME_TIME_MINUTES
        self.seconds = INITIAL_SECOND
        self.clock["state"] = tki.NORMAL
        self.freeze["state"] = tki.NORMAL
        self.timer()

    def run_game(self):
        """
        Responsible for running a game
        """
        self.root.mainloop()

    def assign_buttons(self, board):
        """
        This method is responsible for the letters appearing on the board
        table
        """
        counter = 0
        for right in range(len(board)):
            for down in range(len(board[right])):
                letter = board[down][right]
                self.buttons[down][right].config(text=letter)
                counter += 1

    def create_buttons(self):
        """
        Realizes the function button_helper which initializes the game's board
        """

        def button_helper(down: int, right: int) -> tki.Button:
            """
            Responsible for creating all the buttons on the game board that
            represent the letters from which the user composes words
            """
            button = tki.Button(self.board_frame, padx=52, pady=25,
                                bg="#7DFFAA", font=("Calibri", 19), width=1)
            button.grid(row=down, column=right)
            return button

        return [
            [button_helper(down, right) for right in range(BOARD_SIZE)]
            for down in range(BOARD_SIZE)
        ]

    def create_words_lists(self):
        """
        Responsible for the scroll bar where the wrong words and the correct
        words that the user has selected appear
        """

        self.correct_listbox.config(yscrollcommand=self.correct_scroll.set)
        self.correct_scroll.config(command=self.correct_listbox.yview)
        self.correct_listbox.config(fg="green", font=("Calibri", 16))

        self.wrong_listbox.config(yscrollcommand=self.wrong_scroll.set)
        self.wrong_scroll.config(command=self.wrong_listbox.yview)
        self.wrong_listbox.config(fg="red", font=("Calibri", 16))

    def update_score(self, new_score):
        """
        This method updates the current player score
        """
        self.score.config(text="your score is: \n " + str(new_score))

    def update_word(self, new_word):
        """
        updates chosen word on answer label
        """
        self.answer.config(text=new_word)

    def update_correct(self, new_word):
        """
        Updates correct words in correct_listbox which is represented by
        the correct words' scroll bar
        """
        self.answer["text"] = " "
        self.correct_listbox.insert(tki.END, new_word)

    def update_wrong(self, new_word):
        """
        Updates wrong words in wrong_listbox which is represented by
        the wrong words' scroll bar
        """
        self.answer["text"] = " "
        self.wrong_listbox.insert(tki.END, new_word)

    def update_answer_label(self):
        """
        updates the answer label to be empty when user presses the insert
        button
        """
        self.answer["text"] = " "

    def reset_clock(self):
        """
        when user start a new game, the clock should reset, this function is
        accountable for that
        """
        self.is_paused = False
        self.clock.configure(text=INITIAL_TIME_DISPLAY,
                             state=tki.ACTIVE)
        if self.seconds == -1 and self.minutes == 0:
            self.minutes = GAME_TIME_MINUTES
            self.seconds = INITIAL_SECOND
            self.timer()
        self.minutes = GAME_TIME_MINUTES
        self.seconds = INITIAL_SECOND

    def reset_screen(self, new_board):
        """
        when user starts a new game, the board should be reset.
        This function is accountable for that
        """
        self.assign_buttons(new_board)
        self.update_word(" ")
        self.update_score(INITIAL_SCORE)
        self.correct_listbox.delete(0, tki.END)
        self.wrong_listbox.delete(0, tki.END)
        self.reset_clock()
        self.timeup_frame.place_forget()

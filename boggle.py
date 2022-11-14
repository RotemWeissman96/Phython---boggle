from gui import *
from gamemodel import *


class Controller:
    """
    controller class, connect the model and the gui classes, mainly
    assigning functions to buttons
    """
    def __init__(self):
        self.gui = Game()
        self.model = GameModel()
        self.init_board_buttons()
        self.init_insert_button()
        self.start_quit()
        self.time_restart_buttons()

    def init_board_buttons(self):
        """
        assign functions to all buttons on board
        """
        self.gui.assign_buttons(self.model.get_board())
        for down in range(4):  # run through all rows of buttons
            for right in range(4):  # run through all buttons in the row
                def helper(f, down_f, right_f):
                    """
                    generates and returns the function to assign to a button,
                    get the correct function and the index of the button
                    """
                    def g(_):
                        """
                        the function for the button to be returned by helper
                        """
                        f((down_f, right_f))
                        self.gui.update_word(self.model.get_current_word())
                    return g

                fun = helper(self.model.do_cube_clicked, down, right)
                self.gui.buttons[down][right].bind('<Button-1>', fun)

    def init_insert_button(self):
        """
        assign a function to the insert word button
        """
        def fun():
            """
            calls the ENTER function which check if the current word is
            valid. update the game data and the screen according to the answer
            """
            found = self.model.do_enter()
            if found == True:  # if a word is found
                self.gui.update_score(self.model.get_score())
                self.gui.update_correct(self.model.get_correct_words()[-1])
            elif found == False:  # if a word is not found
                if not self.model.get_wrong_words() or \
                        self.model.get_wrong_words()[-1] != \
                        self.gui.wrong_listbox.get(-1):
                    self.gui.update_wrong(self.model.get_wrong_words()[-1])
            else:  # if a word is already been entered
                self.gui.update_answer_label()

        self.gui.insert_btn.config(command=fun)

    def start_quit(self):
        """
        assign the correct function to the start/quit button
        """
        def fun():
            """
            if start, starts the game. if quit, asks the palyer if he want
            to restart, if not asks the player if he surely wants to quit.
            update the game data and screen according to answeres
            """
            restart = self.gui.basic_actions()
            if restart:
                self.model.do_reset()
                self.gui.reset_screen(self.model.get_board())
                self.gui.timeup_frame.place_forget()
        self.gui.start_btn.config(command=fun)

    def time_restart_buttons(self):
        """
        assign the time ending possibilities to the yes and no buttons
        """
        def yes():
            """
            if the player wants to restart, update the game data and screen
            according to answeres
            """
            self.model.do_reset()
            self.gui.reset_screen(self.model.get_board())

        def no():
            """
            if the player wants to quit, shuts the program
            """
            sys.exit()
        self.gui.restart_yes.config(command=yes)
        self.gui.restart_no.config(command=no)

    def run(self):
        """
        starts the game
        """
        self.gui.run_game()


if __name__ == '__main__':
    controller = Controller()
    controller.run()

from boggle_board_randomizer import randomize_board
from sys import exit


class GameModel:
    """
    model class is responsible for manipulating the "behind the scene" data
    """
    __board: list  # of lists
    __correct_words: list
    __wrong_words: list
    __cur_word: str
    __score: int
    __last_clicked: tuple
    __words_list: list
    __cur_path: list  # of tuples

    def __init__(self) -> None:
        self.do_reset()

    def do_reset(self) -> None:
        """
        restart the game data, in order to start a new game
        """
        self.__board = randomize_board()
        self.__correct_words = []
        self.__wrong_words = []
        self.__cur_word = ""
        self.__score = 0
        self.__last_clicked = ()
        self.create_sorted_words()
        self.__cur_path = []

    def create_sorted_words(self):
        """
        sorts the word list in the first opening of the game, in order to
        improve the run time by enabling the binary search
        """
        try:
            with open("boggle_dict.txt", "r") as f:
                self.__words_list = f.read().split()
                self.__words_list.sort()
        except FileNotFoundError:
            exit()

    def reset_word(self):
        """
        reset the current word, current path and last clicked possession
        """
        self.__cur_word = ""
        self.__cur_path = []
        self.__last_clicked = ()

    def do_cube_clicked(self, location: (int, int)) -> None:
        """
        update the game data according to the cube clicked, the position of
        the cube and the letter. checks if the cube position is valid
        """
        if self.next_location_valid(location):  # if the position is valid
            self.__last_clicked = location
            down, right = location
            self.__cur_word += self.__board[down][right]
            self.__cur_path.append(location)
        else:
            self.reset_word()

    def next_location_valid(self, location):
        """
        checks if the next location is valid or not by the game rules.
        return true it its valid or false
        """
        down, right = location
        if self.__last_clicked:  # if its not the first cube for current word
            if max(abs(self.__last_clicked[0] - down),
                   abs(self.__last_clicked[1] - right)) > 1:
                # if the distance from last cube is more then 1 in x or y
                return False
            if location in self.__cur_path:  # if cube has already been picked
                return False
        return True

    def do_enter(self):
        """
        check if current word is in word list. if it is, return True and add it
        to the correct words list, removing it from word list. if not, return
        false and adding it to the wronf list. checking if word has already
        been chosen
        """
        if self.__cur_word in self.__wrong_words or self.__cur_word in\
                self.__correct_words:
            # if word ha already been checked
            return
        if self.__cur_word and self.binary_search():
            # if the word is not empty and in wordlist
            self.__correct_words.append(self.__cur_word)
            self.__words_list.remove(self.__cur_word)
            self.add_points()
            self.reset_word()
            return True
        else:
            self.__wrong_words.append(self.__cur_word)
            self.reset_word()
            return False

    def binary_search(self):
        """
        recursively searches for the current word in the words list
        return the word if found and None if not found
        """
        start = 0
        end = len(self.__words_list) - 1

        while start <= end:  # search in the entire "current" list
            middle = int((start + end) / 2)
            midpoint = self.__words_list[middle]
            if midpoint > self.__cur_word:  # if the word is in the lower part
                end = middle - 1
            elif midpoint < self.__cur_word: # if word is in higher part
                start = middle + 1
            else:
                return midpoint

    def add_points(self):
        """
        adds point based on the path length power by 2
        """
        self.__score += len(self.__cur_path) ** 2

    def get_score(self):
        """
        get the current score
        """
        return self.__score

    def get_correct_words(self):
        """
        get the current correct words list
        """
        return self.__correct_words

    def get_current_word(self):
        """
        get the current word
        """
        return self.__cur_word

    def get_wrong_words(self):
        """
        get the wrong words list
        """
        return self.__wrong_words

    def get_board(self):
        """
        get the board game (list if lists)
        """
        return self.__board

    def get_path(self):
        """
        get the current path
        """
        return self.__cur_path

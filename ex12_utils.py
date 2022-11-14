
BOARD_SIZE = 4


def is_valid_path(board, path, words):
    """
    check if a path is valid and lead to a valid word.
    return True if it is or False if it is not
    """
    current_word = ""
    visited = []
    for i in range(len(path)):  # going through all path
        down, right = path[i]
        if not type(down) == int or not type(right) == int:
            return
        if visited:  # if its not the first step
            if path[i] in visited:  # if this block is already visited
                return
            if max(abs(visited[-1][0]-down), abs(visited[-1][1]-right)) > 1:
                # if the block is too far from the last block
                return
        if down < 0 or right < 0 or down>BOARD_SIZE-1 or right > BOARD_SIZE-1:
            # if block is out of bounds
            return
        visited.append(path[i])
        current_word += board[down][right]
    if current_word in words:  # if the word is in words list
        return current_word
    return


def all_paths_to_word(board, word):
    """
    searches for a word in the board
    param board: a game board
    param word: a word to search
    return a list of lists, the first sub list contain all 1 length paths,
    the second all two length paths list and so on
    """
    final_paths = []
    for possible_list_length in range(len(word)):
        # create empty lists in final_paths as the word length
        final_paths.append([])
    for starting in get_coordinates(len(board)):
        # going through all starting cubes
        curr_data = board[starting[0]][starting[1]]
        if word[0:len(curr_data)] == curr_data:
            word_paths_helper(board, word, final_paths, [starting],
                                     curr_data)  # recursive function
    return final_paths


def word_paths_helper(board, word, paths_lst, current_path,
                             current_word):
    """
    search recursively starting from a certain cube all the paths to a given
    word.
    param board: the game board
    param word: the word to search
    param paths_lst: saves all the found paths list
    param current_path: sthe current path
    param current_word: the current word
    return a list of lists, the first sub list contain all 1 length paths,
    the second all two length paths list and so on
    """
    if len(current_word) == len(word):  # base case (for len 1)
        if current_word == word:  # if word is current word
            paths_lst[len(current_path) - 1].append(current_path[:])
        return
    down, right = current_path[-1]
    my_neighbors = get_all_neighbors(board, down, right)
    for neighbor_data in my_neighbors:
        subword = current_word + neighbor_data
        if len(word) >= len(subword):
            if subword == word[0:len(subword)]:
                for neighbor in my_neighbors[neighbor_data]:
                    # go through all char positions
                    if neighbor in current_path:  # if already been there
                        continue
                    next_down, next_right = neighbor
                    current_path.append((next_down, next_right))
                    word_paths_helper(board, word, paths_lst, current_path,
                                      current_word + neighbor_data)
                    # recursive call, backtracking in current word
                    current_path.pop()  # back tracking


def get_all_neighbors(board, down, left):
    """
    get all the neighboring cubes position and content
    return a dictionary with key - letter, values - positions of letter
    """
    neighbors = {}
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:  # don't return yourself
                continue
            if down + j-1 < 0 or left + i - 1 < 0:  # if out of bounds -
                continue
            if down + j-1 >= BOARD_SIZE or left + i - 1 >= BOARD_SIZE:
                # if out of bounds +
                continue
            letter = board[down-1+j][left-1+i]
            if letter in neighbors:
                neighbors[letter].append((down-1+j, left-1+i))
            else:
                neighbors[letter] = [(down-1+j, left-1+i)]
    return neighbors


def get_coordinates(size):
    """
    return a list of all board coordinates
    """
    lst = []
    for i in range(size):
        for j in range(size):
            lst.append((j, i))
    return lst


def find_length_n_paths(n, board, words):
    """The function returns a list of all the n length, valid paths, which lead
    to the words in "words" """
    n_length_paths = []
    for word in words:
        if len(word) >= n:
            n_length_paths += all_paths_to_word(board, word)[n-1]
    return n_length_paths


def find_length_n_words(n, board, words):
    """The function returns a list of all the valid paths to n length words
     in "words" list."""
    all_words_paths = []
    for word in set(words):
        if len(word) == n:
            word_paths = all_paths_to_word(board, word)
            all_words_paths += unpack_lists_of_lists(word_paths)
    return all_words_paths


def unpack_lists_of_lists(lst):
    """Receives a list of lists, of lists, and returns a list with
     all the lists, when there are no more lists within another one"""
    list_unpacked=[]
    for paths_in_the_same_length in lst:
        for path in paths_in_the_same_length:
            list_unpacked.append(path)
    return list_unpacked


def max_score_paths(board, words):
    """
    finds the longest path for each word in words list that can be found in
    board.
    return a list of all the longest paths found for each word
    """
    winning_paths = []
    for word in set(words):
        path_list = all_paths_to_word(board, word)
        for i in range(len(path_list)-1, -1, -1):
            if path_list[i]:
                winning_paths.append(path_list[i][0])
                break
    return winning_paths


import random

class WorldeGameEngine(object):

    def __init__(self, all_words, max_num_guesses=None):
        self.all_words = set(all_words)
        self.secret_word = None
        self.max_num_guesses = max_num_guesses
        self.guesses_so_far = list()

    def set_word_to_guess(self, word=None):
        if word is None:
            self.secret_word = random.choice(list(self.all_words))
        else:
            if word not in self.words:
                pass
            self.secret_word = word

        self.guesses_so_far = list()


    def guess(self, word):
        if word not in self.all_words:
            pass

        if self.max_num_guesses is not None and self.max_num_guesses >= len(self.guesses_so_far):
            pass

        response_list = len(word)* ['b']
        remaining_letters = list(self.secret_word)
        for index, letter in enumerate(word):
            if letter in self.secret_word:
                response_list[index] = 'y'
                remaining_letters.remove(letter)
        for index, letter in enumerate(word):
            if letter == self.secret_word[index]:
                response_list[index] = 'g'

        response_string = "".join(response_list)
        self.guesses_so_far.append((word, response_string))
        return response_string

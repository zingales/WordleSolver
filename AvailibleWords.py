import random

first_26_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

def convert_letter_to_prime(letter):
    return first_26_primes[ord(letter)-97]


def convert_word_to_value(word):
    value = 1
    for letter in word:
        value*=convert_letter_to_prime(letter)
    return value

def generate_numbers_to_words_map(words):
    numbers_to_words_map = dict()

    anagrams = dict()
    for word in words:
        value = convert_word_to_value(word)
        if value in numbers_to_words_map:
            anagram_words = anagrams.get(value, set())
            anagram_words.add(word)
            anagram_words.add(numbers_to_words_map[value])
            anagrams[value]=anagram_words
        numbers_to_words_map[value]=word

    return numbers_to_words_map, anagrams


def word_guess_to_value(word, hints):
    correct_guesses = ''
    for i in range(0,len(hints)):
        if hints[i] == 'y':
            correct_guesses+=word[i]
        if hints[i] == 'g':
            correct_guesses+=word[i]
    return convert_word_to_value(correct_guesses)


def word_guess_to_non_values(word, hints):
    incorrect_guesses = ''
    incorrect_values = set()
    for i in range(0,len(hints)):
        if hints[i] == 'b':
            incorrect_guesses+=word[i]
            incorrect_values.add(convert_letter_to_prime(word[i]))

    return incorrect_values

def generate_string_location_map(all_availible_words):
    # create object so filling it is simple
    letter_spot_value_map = dict()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        index_to_set = dict()
        for index in range(0, len(next(iter(all_availible_words)))):
            index_to_set[index]=set()
        letter_spot_value_map[letter] = index_to_set

    for word in all_availible_words:
        value = convert_word_to_value(word)
        for index, letter in enumerate(word):
            letter_spot_value_map[letter][index].add(value)

    return letter_spot_value_map

def get_green_and_yellow_tuples(word, hints):
    yellows = list()
    greens = list()
    for i in range(0,len(hints)):
        if hints[i] == 'y':
            yellows.append((word[i], i))
        if hints[i] == 'g':
            greens.append((word[i], i))
    return greens, yellows

class AvailibleWords(object):


    def __init__(self, all_words):
        self.all_words_value_to_word_map, self.availible_anagrams = generate_numbers_to_words_map(all_words)
        self.letter_spot_value_map = generate_string_location_map(all_words)

        self.availible_word_values = set(self.all_words_value_to_word_map.keys())

    def words(self):
        words = set()
        for value in self.availible_word_values:
            if value in self.availible_anagrams:
                words.update(self.availible_anagrams[value])
            else:
                words.add(self.all_words_value_to_word_map[value])

        return words

    def get_next_guess(self):
        if len(self) == 0:
            # throw error
            pass

        return random.choice(list(self.words()))


    def __len__(self):
        count = len(self.availible_word_values)

        for value, anagrams in self.availible_anagrams.items():
            #the subraction is for not double counting since
            # 1 word in the list was already including in the
            # availible words values length
            count += len(anagrams)-1
        return count

    def filter_guess(self, guess, response):

        incorrect_values = word_guess_to_non_values(guess, response)
        correct_value = word_guess_to_value(guess, response)

        # handling single letter being in word but not a repitition
        for incorrect_value in set(incorrect_values):
            if correct_value % incorrect_value == 0:
                # correct value contains at least 1 of incorrect value.
                incorrect_values.remove(incorrect_value)
                value = incorrect_value**2
                # handle scenarios where there are n instances of the letter but not n+1
                while correct_value % value == 0:
                    value*=incorrect_value
                incorrect_values.add(value)

        for word_value in set(self.availible_word_values):
            if word_value % correct_value != 0:
                self.availible_word_values.remove(word_value)
                self.availible_anagrams.pop(word_value, None)
            for incorrect_value in incorrect_values:
                if word_value not in self.availible_word_values:
                    break
                if word_value % incorrect_value == 0:
                    self.availible_word_values.remove(word_value)
                    self.availible_anagrams.pop(word_value, None)

        greens, yellows = get_green_and_yellow_tuples(guess, response)

        for letter, index in greens:
            self.availible_word_values = self.availible_word_values.intersection(self.letter_spot_value_map[letter][index])

        for letter,index in yellows:
            values_with_anagrams = set(self.letter_spot_value_map[letter][index])
            # don't remove any values with anagrams (for now)
            values = values_with_anagrams.difference(self.availible_anagrams.keys())
            self.availible_word_values = self.availible_word_values.difference(values)

        #deal with the anagrams
        if correct_value in self.availible_anagrams:
            if len(greens) > 0:
                anagrams = self.availible_anagrams[correct_value]
                for word in list(anagrams):
                    for letter, index in greens:
                        if word[index] != letter:
                            anagrams.remove(word)
                            break

            if len(yellows) > 0:
                anagrams = self.availible_anagrams[correct_value]
                for word in list(anagrams):
                    for letter, index in yellows:
                        if word[index] == letter:
                            anagrams.remove(word)
                            break
